"""Papildoma aprašomoji diagnostika iš išsaugotų išorinių prognozių."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Markdown, display
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from src.notebook_report import PRIMARY, LABELS

CLASSES = ['opel', 'saab', 'van', 'bus']
NAMES = ['Opel', 'Saab', 'Furgonai', 'Autobusai']
GROUPS = ['car', 'van', 'bus']
GROUP_NAMES = ['Lengvieji\nautomobiliai', 'Furgonai', 'Autobusai']
GROUP_MAP = {'opel': 'car', 'saab': 'car', 'van': 'van', 'bus': 'bus'}
COLORS = ['#2166ac', '#d95f02', '#1b9e77', '#7570b3', '#666666']


# Sutvarko grafiko tarpus, parodo jį notebooke ir uždaro figūrą, kad nesikauptų atmintyje.
def finish(fig):
    fig.tight_layout()
    plt.show()
    plt.close(fig)


# Penkiems metodams parodo keturių originalių klasių F1 ir jautrumą.
# Skaičiuoja iš sujungtų išorinių prognozių, ne iš skaidinių metrikų vidurkio.
def class_comparison(data):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    scores = {}
    for k, method in enumerate(PRIMARY):
        rows = data['predictions'].query('method == @method')
        _, recall, f1, support = precision_recall_fscore_support(
            rows.true, rows.predicted, labels=CLASSES, zero_division=0)
        scores[method] = (recall, f1)
        for ax, values in zip(axes, [f1, recall]):
            ax.bar(np.arange(4) + (k-2)*.15, values, width=.15,
                   label=LABELS[method], color=COLORS[k])
    for ax, title in zip(axes, ['F1 pagal originalią klasę', 'Jautrumas: kiek tikrų objektų atpažinta']):
        ax.set(xticks=range(4), xticklabels=NAMES, ylim=(0, 1.08), ylabel='Metrikos reikšmė', title=title)
        ax.grid(axis='y', alpha=.2)
    axes[0].legend(fontsize=8, loc='lower left')
    finish(fig)
    display(pd.DataFrame({LABELS[m]: scores[m][1] for m in PRIMARY}, index=NAMES).rename_axis('Klasės F1').round(3))
    weakest = int(np.argmin(scores['svm'][1]))
    display(Markdown(f"SVM silpniausia originali klasė pagal F1 – **{NAMES[weakest]}** ({scores['svm'][1][weakest]:.3f}). "
        'F1 apima preciziškumą ir jautrumą; jautrumas rodo, kokia tikrosios klasės dalis aptikta.'))


# Opel ir Saab sujungia į automobilių grupę tik rezultatų interpretavimui.
# Parodo grupių jautrumą, F1 ir SVM painiavos matricas; modeliai nepermokomi.
def vehicle_groups(data):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.6))
    summary = []
    for k, method in enumerate(PRIMARY):
        rows = data['predictions'].query('method == @method')
        # Tas pats grupavimas taikomas tikrosioms ir prognozuotoms žymėms.
        truth, pred = rows.true.map(GROUP_MAP), rows.predicted.map(GROUP_MAP)
        assert truth.notna().all() and pred.notna().all()
        _, recall, f1, support = precision_recall_fscore_support(truth, pred, labels=GROUPS, zero_division=0)
        axes[0].bar(np.arange(3)+(k-2)*.15, recall, width=.15, color=COLORS[k], label=LABELS[method])
        summary.append({'Metodas': LABELS[method], **dict(zip(['Automobilių F1', 'Furgonų F1', 'Autobusų F1'], f1))})
        if method == 'svm':
            cm = confusion_matrix(truth, pred, labels=GROUPS)
            # Dalijama iš eilutės sumos: procentai skaičiuojami tikrosios grupės viduje.
            norm = cm/cm.sum(axis=1, keepdims=True)
            for ax, values, title in zip(axes[1:], [cm, norm], ['SVM: prognozių skaičius', 'SVM: tikrosios grupės dalis']):
                ax.imshow(norm, cmap='Blues', vmin=0, vmax=1)
                for i in range(3):
                    for j in range(3):
                        label = str(int(values[i,j])) if ax is axes[1] else f'{values[i,j]:.1%}'
                        ax.text(j, i, label, ha='center', va='center', color='white' if norm[i,j]>.5 else 'black')
                ax.set(xticks=range(3), yticks=range(3), xticklabels=GROUP_NAMES, yticklabels=GROUP_NAMES,
                       title=title, xlabel='Prognozuota grupė', ylabel='Tikroji grupė')
            car = rows.true.isin(['opel', 'saab'])
            original_correct = (rows.loc[car, 'true'] == rows.loc[car, 'predicted']).mean()
            grouped_correct = (truth[car] == pred[car]).mean()
            internal = (car & rows.predicted.isin(['opel', 'saab']) & (rows.true != rows.predicted)).sum()
    axes[0].set(xticks=range(3), xticklabels=GROUP_NAMES, ylim=(0, 1.08), ylabel='Jautrumas', title='Trijų grupių atpažinimas')
    axes[0].legend(fontsize=8, loc='lower left')
    axes[0].grid(axis='y', alpha=.2)
    finish(fig)
    display(pd.DataFrame(summary).set_index('Metodas').round(3))
    display(Markdown(f'**SVM lengvųjų automobilių atveju:** tikslus Opel / Saab modelis atpažintas '
        f'**{original_correct:.1%}**, o bendra automobilių grupė – **{grouped_correct:.1%}**. '
        f'Sujungus klases, **{internal}** Opel ↔ Saab klaidų tampa teisingais grupės atsakymais. '
        'Tai lengvesnė trijų grupių interpretacija, o ne naujai išmokytas modelis ar pagerėjusi keturių klasių metrika.'))


# Kiekviename tame pačiame skaidinyje atima kito metodo Macro-F1 iš SVM Macro-F1.
# Parodo skirtumų dėžutes, visus taškus ir pergalių lentelę; teigiama reikšmė palanki SVM.
def paired_comparison(data):
    # Eilutė – skaidinys, stulpelis – metodas; taip poruojamas tas pats bandymas.
    wide = data['folds'].pivot(index='split', columns='method', values='macro_f1')
    assert wide.notna().all().all()
    others = ['mlp', 'rbf', 'knn', 'centroid', 'svm_linear', 'svm_unscaled']
    # Pvz., 0,85−0,75=+0,10: SVM šiame skaidinyje turi 0,10 didesnį Macro-F1.
    diffs = [wide.svm - wide[m] for m in others]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.boxplot(diffs, orientation='horizontal', tick_labels=[LABELS[m] for m in others], showfliers=False)
    for i, values in enumerate(diffs, 1):
        ax.scatter(values, np.full(len(values), i), s=9, alpha=.3, color='#2166ac')
    ax.axvline(0, color='#b2182b', linestyle='--')
    ax.set(xlabel='SVM Macro-F1 − kito varianto Macro-F1 (tame pačiame skaidinyje)',
           title='Porinis SVM pranašumas ir abliacijos: 50 tų pačių skaidinių')
    ax.grid(axis='x', alpha=.2)
    finish(fig)
    display(pd.DataFrame({'Palyginimas su': [LABELS[m] for m in others],
        'Vidutinis skirtumas': [v.mean() for v in diffs],
        'SVM geresnis, skaidinių': [(v>0).sum() for v in diffs],
        'Lygiosios': [np.isclose(v, 0, atol=1e-12, rtol=0).sum() for v in diffs]}).set_index('Palyginimas su').round(3))


# Penkiems metodams parodo Macro-F1 ir jo kritimą nuo švaraus testo.
# Kritimas dauginamas iš 100 ir pateikiamas procentiniais punktais, ne santykiniais procentais.
def all_robustness(data):
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5), sharex='col')
    for col, (kind, xlabel) in enumerate([('noise', 'Triukšmo σ / mokymo požymio SD'), ('missing', 'Trūkstamų langelių dalis')]):
        for k, method in enumerate(PRIMARY):
            scores = data['robustness'].query('method == @method and kind == @kind').groupby('level').macro_f1.mean()
            clean = data['summary'].loc[method, 'macro_f1_mean']
            x, y = [0, *scores.index], np.array([clean, *scores.values])
            axes[0,col].plot(x, y, 'o-', color=COLORS[k], label=LABELS[method])
            axes[1,col].plot(x, 100*(clean-y), 'o-', color=COLORS[k])
        axes[0,col].set(ylim=(0,1), ylabel='Macro-F1', title='Triukšmas' if kind=='noise' else 'Trūkstami požymiai')
        axes[1,col].set(xlabel=xlabel, ylabel='Macro-F1 kritimas, proc. punktai')
        axes[1,col].axhline(0, color='grey', linewidth=.7)
        for ax in axes[:,col]:
            ax.grid(alpha=.2)
    axes[0,0].legend(fontsize=8)
    finish(fig)
    display(Markdown('Viršuje matomas likęs atpažinimo lygis, apačioje – kritimas nuo kiekvieno metodo švaraus testo. '
        'Didžiausias kritimas savaime nereiškia prasčiausio galutinio rezultato. Taškai yra 50 skaidinių ir po 20 trikdžio realizacijų vidurkiai; '
        'nulinis lygis paimtas iš švaraus testo. Tai aprašomasis palyginimas, ne nepriklausomų imčių reikšmingumo testas.'))
