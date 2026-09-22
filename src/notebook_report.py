"""Sąsiuvinių lentelės ir grafikai iš užbaigto eksperimento, be naujo mokymo."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import Markdown, display
from sklearn.metrics import classification_report, confusion_matrix

from src.data import CLASSES

LABELS = {'svm': 'SVM RBF', 'mlp': 'MLP', 'rbf': 'RBF tinklas',
          'knn': '5-NN', 'centroid': 'Artimiausias centroidas',
          'svm_linear': 'Tiesinis SVM', 'svm_unscaled': 'SVM be standartizavimo'}
PRIMARY = ['svm', 'mlp', 'rbf', 'knn', 'centroid']


# Nuskaito baigto eksperimento failus ir sutikrina dydžius bei metrikų vidurkius.
# Grąžina duomenų žodyną kitoms notebooko funkcijoms; mokymo nepaleidžia.
def load_results():
    root = Path('results/main')
    summary = pd.read_csv(root / 'results_summary.csv', index_col=0)
    folds = pd.read_csv(root / 'fold_metrics.csv')
    predictions = pd.read_csv(root / 'out_of_fold_predictions.csv')
    robustness = pd.read_csv(root / 'robustness.csv')
    if len(folds) != 350 or len(predictions) != 29610:
        raise ValueError('Reikia baigto 50 skaidinių eksperimento results/main aplanke.')
    verification = json.loads((root / 'verification.json').read_text(encoding='utf-8'))
    assert verification['status'] == 'passed'
    # Suvestinės reikšmės papildomai sutikrinamos su skaidinių CSV.
    means = folds.groupby('method')[['macro_f1', 'balanced_accuracy']].mean()
    assert np.allclose(summary.macro_f1_mean, means.loc[summary.index, 'macro_f1'])
    assert np.allclose(summary.balanced_accuracy_mean, means.loc[summary.index, 'balanced_accuracy'])
    return {'root': root, 'summary': summary, 'folds': folds,
            'predictions': predictions, 'robustness': robustness}


# Parodo pasirinktų metodų metrikų ir mokymo laiko lentelę, surikiuotą pagal Macro-F1.
def table(data, methods=None):
    summary = data['summary']
    methods = methods or PRIMARY
    rows = []
    for name in summary.loc[methods].sort_values('macro_f1_mean', ascending=False).index:
        row = summary.loc[name]
        rows.append({'Metodas': LABELS[name],
                     'Macro-F1 ± SD': f'{row.macro_f1_mean:.3f} ± {row.macro_f1_sd:.3f}',
                     'Balanced accuracy ± SD': f'{row.balanced_accuracy_mean:.3f} ± {row.balanced_accuracy_sd:.3f}',
                     'Mokymas su paieška, s': round(row.train_seconds_mean, 3)})
    display(pd.DataFrame(rows).set_index('Metodas'))


# Parodo vieno metodo vidurkius, sklaidą, skirtumą nuo geresnio baseline ir prognozavimo laiką.
def key_metrics(data, method):
    row = data['summary'].loc[method]
    baseline = data['summary'].loc[['knn', 'centroid'], 'macro_f1_mean'].idxmax()
    folds = data['folds'].query('method == @method')
    display(pd.DataFrame({'Rodiklis': ['Macro-F1 vidurkis', 'Macro-F1 SD',
        'Balanced accuracy vidurkis', 'Balanced accuracy SD',
        f'Macro-F1 skirtumas nuo {LABELS[baseline]}', 'Išorinių skaidinių skaičius',
        'Vidutinė prognozė 84–85 įrašų paketui, ms'],
        'Reikšmė': [round(row.macro_f1_mean, 4), round(row.macro_f1_sd, 4),
        round(row.balanced_accuracy_mean, 4), round(row.balanced_accuracy_sd, 4),
        round(row.macro_f1_mean-data['summary'].loc[baseline, 'macro_f1_mean'], 4),
        len(folds), round(folds.predict_seconds.mean()*1000, 3)]}).set_index('Rodiklis'))


# Parodo Macro-F1 pasiskirstymą per 50 skaidinių. Tai rezultatų, ne porinių skirtumų dėžutės.
def comparison_plot(data, methods=None):
    methods = methods or PRIMARY
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.boxplot([data['folds'].loc[data['folds'].method == m, 'macro_f1'] for m in methods],
               tick_labels=[LABELS[m] for m in methods])
    ax.set(ylabel='Macro-F1', title='Rezultatų sklaida per tuos pačius 50 išorinių skaidinių')
    ax.grid(axis='y', alpha=.25)
    fig.tight_layout()
    plt.show()
    plt.close(fig)


# Iš sujungtų prognozių apskaičiuoja klasių metrikas ir dvi painiavos matricas.
# Normalizuotoje matricoje kiekvienos tikrosios klasės eilutė sudaro 100 %.
def class_analysis(data, method):
    rows = data['predictions'].query('method == @method')
    report = pd.DataFrame(classification_report(rows.true, rows.predicted, labels=CLASSES,
                                               output_dict=True, zero_division=0)).T.loc[CLASSES]
    display(report.rename(columns={'precision': 'Preciziškumas', 'recall': 'Jautrumas',
                                   'f1-score': 'F1', 'support': 'Prognozių skaičius'}).round(3))
    cm = confusion_matrix(rows.true, rows.predicted, labels=CLASSES)
    normalized = cm / cm.sum(axis=1, keepdims=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, values, title, percentage in zip(axes, [cm, normalized],
            ['Absoliutūs skaičiai', 'Dalis pagal tikrąją klasę'], [False, True]):
        ax.imshow(values, cmap='Blues')
        for i in range(4):
            for j in range(4):
                ax.text(j, i, f'{values[i,j]:.1%}' if percentage else str(values[i,j]),
                        ha='center', va='center', color='white' if values[i,j] > values.max()/2 else 'black')
        ax.set(xticks=range(4), yticks=range(4), xticklabels=CLASSES, yticklabels=CLASSES,
               xlabel='Prognozuota klasė', ylabel='Tikroji klasė', title=title)
    fig.suptitle(LABELS[method] + ' painiavos matrica')
    fig.tight_layout()
    plt.show()
    plt.close(fig)


# Atrenka iki dešimties skirtingų klaidingų įrašų ir parodo klaidų kartojimąsi.
# Tas pats objektas gali būti klaidingas nuo 0 iki 5 kartų.
def error_examples(data, method):
    rows = data['predictions'].query('method == @method').copy()
    rows['error'] = rows.true != rows.predicted
    frequency = rows.groupby('row_index').error.sum()
    errors = rows[rows.error].groupby(['row_index', 'true', 'predicted']).size().rename('pair_count').reset_index()
    errors = errors.sort_values(['pair_count', 'row_index'], ascending=[False, True]).drop_duplicates('row_index').head(10)
    errors['errors_in_5'] = errors.row_index.map(frequency)
    display(errors.rename(columns={'row_index': 'Įrašo indeksas', 'true': 'Tikroji klasė',
        'predicted': 'Dažniausia klaidinga klasė', 'pair_count': 'Šios klaidos kartai',
        'errors_in_5': 'Visos klaidos iš 5'}).set_index('Įrašo indeksas'))
    counts = frequency.value_counts().reindex(range(6), fill_value=0)
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(counts.index, counts.values, color='#3576a8')
    ax.set(xlabel='Klaidų skaičius per 5 pakartojimus', ylabel='Skirtingų įrašų skaičius',
           title=LABELS[method] + ': klaidų pasikartojimas', xticks=range(6))
    fig.tight_layout()
    plt.show()
    plt.close(fig)


# Parodo pasirinkto metodo trikdžių lentelę ir jo atsparumą kartu su abiem baseline.
def robustness_analysis(data, method):
    selected = data['robustness'].query('method == @method')
    table_rows = selected.groupby(['kind', 'level'])[['macro_f1', 'balanced_accuracy']].mean()
    table_rows['macro_f1_drop'] = data['summary'].loc[method, 'macro_f1_mean'] - table_rows.macro_f1
    display(table_rows.rename(columns={'macro_f1': 'Macro-F1', 'balanced_accuracy': 'Balanced accuracy',
                                      'macro_f1_drop': 'Macro-F1 kritimas'}).round(4))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, kind, title in zip(axes, ['noise', 'missing'], ['Gauso triukšmas (σ)', 'Trūkstamų langelių dalis']):
        for name in [method, 'knn', 'centroid']:
            scores = data['robustness'].query('method == @name and kind == @kind').groupby('level').macro_f1.mean()
            ax.plot([0, *scores.index], [data['summary'].loc[name, 'macro_f1_mean'], *scores],
                    marker='o', label=LABELS[name])
        ax.set(xlabel=title, ylabel='Macro-F1', ylim=(0, 1))
        ax.grid(alpha=.25)
        ax.legend(fontsize=8)
    fig.suptitle('Atsparumas: kiekvieno trikdžio lygio 20 realizacijų kiekviename skaidinyje')
    fig.tight_layout()
    plt.show()
    plt.close(fig)


# Parodo SVM variantų lentelę ir po penkis jautriausius požymius dviejose diagnostikose.
def ablations(data):
    table(data, ['svm', 'svm_linear', 'svm_unscaled'])
    root = data['root']
    importance = pd.read_csv(root / 'feature_importance_summary.csv', index_col=0).iloc[:, 0]
    missing = pd.read_csv(root / 'missing_feature_summary.csv', index_col=0).f1_drop_mean
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, values, title in zip(axes, [importance, missing], ['SVM permutacijų jautrumas', 'SVM požymio trūkumo jautrumas']):
        values.sort_values(ascending=False).head(5).sort_values().plot.barh(ax=ax)
        ax.set(title=title, xlabel='Vidutinis Macro-F1 kritimas')
    fig.tight_layout()
    plt.show()
    plt.close(fig)


# Iš realių metrikų suformuoja laimėjimo ar pralaimėjimo paaiškinimą notebookui.
def interpretation(data, method):
    summary = data['summary']
    winner = summary.loc[PRIMARY].macro_f1_mean.idxmax()
    baseline = summary.loc[['knn', 'centroid']].macro_f1_mean.idxmax()
    difference = summary.loc[method, 'macro_f1_mean'] - summary.loc[baseline, 'macro_f1_mean']
    text = f'**{LABELS[method]}** vidutinis Macro-F1 yra **{summary.loc[method, "macro_f1_mean"]:.3f}**, skirtumas nuo geresnio baseline ({LABELS[baseline]}) **{difference:+.3f}**. '
    if method == winner:
        text += 'Šis metodas laimėjo pagal iš anksto pasirinktą pirminę metriką. '
    else:
        text += f'Šis metodas nelaimėjo: {LABELS[winner]} Macro-F1 buvo {summary.loc[winner, "macro_f1_mean"]:.3f}. '
    if method == 'svm':
        text += 'Geresni rezultatai nei tiesinio SVM ir SVM be standartizavimo dera su netiesinės ribos bei požymių mastelio svarbos paaiškinimu. Abliacijos neįrodo vienintelės priežasties.'
    elif method == 'mlp':
        text += 'Mažoje imtyje rezultatą gali veikti svorių inicializacija, reguliarizacija ir ankstyvasis stabdymas. Šių veiksnių priežastinis poveikis atskirai nepatikrintas; MLP pralaimėjimas nustatytas pagal rezultatus, o ne prielaidą apie tinklo sudėtingumą.'
    else:
        text += 'Išvada galioja išbandytam KMeans centrų, Gauso aktyvacijų ir Ridge išvesties variantui bei jo tinkleliui. Kitų centrų ar pločių veikimas nepatikrintas.'
    display(Markdown(text))


# Parodo išsaugotą SVM hipotezės patikrą ir pataisytą intervalą, neskaičiuodama naujo testo.
def hypothesis(data):
    h = json.loads((data['root'] / 'hypothesis.json').read_text(encoding='utf-8'))
    lo, hi = h['corrected_95pct_ci']
    display(Markdown(f"SVM skirtumas nuo geresnio baseline: **{h['mean_difference']:+.3f}**; pataisytas 95 % intervalas **[{lo:+.3f}; {hi:+.3f}]**; teigiami pakartojimai **{h['positive_repeats']}/5**. Hipotezė pagal nustatytą kriterijų: **{'patvirtinta' if h['confirmed'] else 'nepatvirtinta'}**."))
