"""Aprašomoji klaidų analizė iš išorinių prognozių; nekeičia modelio."""
import matplotlib.pyplot as plt
import pandas as pd


# Sujungia prognozes su požymiais, išsaugo klaidų diagnostikos lenteles ir grafiką.
# Grąžina Markdown eilučių sąrašą pagrindinei ataskaitai; tai aprašomoji analizė.
def extend_report(root, X, predictions, importance):
    records = predictions.copy()
    records['error'] = records.true != records.predicted
    records = records.join(X, on='row_index')
    quantiles = []
    for feature in X.columns:
        for is_error, group in records.groupby('error'):
            q = group[feature].quantile([0, .05, .25, .5, .75, .95, 1])
            quantiles.append({'feature': feature, 'error': is_error, 'prediction_count': len(group),
                              **{f'q{int(k*100):02d}': float(v) for k, v in q.items()}})
    pd.DataFrame(quantiles).to_csv(root / 'error_feature_distributions.csv', index=False)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, feature in zip(axes, importance.head(3).index):
        ax.boxplot([records.loc[~records.error, feature], records.loc[records.error, feature]],
                   tick_labels=['Teisingos', 'Klaidingos'], showfliers=True)
        ax.set_title(feature, fontsize=9)
        ax.set_ylabel('Pradinė požymio reikšmė')
    fig.suptitle('Svarbiausių požymių skirstiniai pagal išorinio bandymo prognozes')
    fig.tight_layout()
    fig.savefig(root / 'error_feature_distributions.png', dpi=160)
    plt.close(fig)

    # Kraštai apibrėžti tik kiekvieno išorinio mokymo 5 ir 95 procentiliais.
    edges = pd.read_csv(root / 'error_edges.csv')
    edges['region'] = edges.edge_features.map(lambda n: 'Bent vienas kraštinis požymis' if n else 'Visi požymiai tarp 5 ir 95 procentilių')
    edge_summary = edges.groupby('region').agg(predictions=('error', 'size'), errors=('error', 'sum'), error_rate=('error', 'mean'))
    edge_summary.to_csv(root / 'error_edge_summary.csv')
    repeat_summary = edges.groupby('repeat').agg(predictions=('error', 'size'), errors=('error', 'sum'), error_rate=('error', 'mean'))
    repeat_summary.to_csv(root / 'error_by_repeat.csv')

    pairs = []
    for true in sorted(records.true.unique()):
        total = (records.true == true).sum()
        for predicted in sorted(records.true.unique()):
            if true != predicted:
                count = ((records.true == true) & (records.predicted == predicted)).sum()
                pairs.append({'true': true, 'predicted': predicted, 'errors': int(count),
                              'fraction_of_true_class': count / total,
                              'fraction_of_all_errors': count / records.error.sum()})
    pd.DataFrame(pairs).to_csv(root / 'class_pair_errors.csv', index=False)
    missing = pd.read_csv(root / 'missing_feature_sensitivity.csv')
    sensitivity = missing.groupby('feature').agg(f1_drop_mean=('f1_drop', 'mean'), f1_drop_sd=('f1_drop', 'std'),
                                                macro_f1_mean=('macro_f1', 'mean'), balanced_accuracy_mean=('balanced_accuracy', 'mean')).sort_values('f1_drop_mean', ascending=False)
    sensitivity.to_csv(root / 'missing_feature_summary.csv')
    lines = ['', '## Papildoma plano klaidų analizė', '',
             'Visų 18 požymių teisingų ir klaidingų prognozių minimumai, 5, 25, 50, 75, 95 procentiliai ir maksimumai pateikti `error_feature_distributions.csv`. '
             'Grafike parodyti trys pagal permutaciją svarbiausi požymiai. Kiekvienas įrašas vertintas penkis kartus, todėl tai aprašomieji susijusių prognozių skirstiniai, o ne nepriklausomų stebėjimų statistinis testas.', '',
             '![Požymių skirstiniai](error_feature_distributions.png)', '',
             'Klaidų dalis prie mokymo skirstinių kraštų:', '']
    for region, row in edge_summary.iterrows():
        lines.append(f'- {region}: {int(row.errors)}/{int(row.predictions)} ({row.error_rate:.1%}).')
    lines += ['', 'Kraštai nustatyti pagal atitinkamos mokymo dalies 5 ir 95 procentilius, nenaudojant testo riboms parinkti. '
              'Dėl 18 požymių bent vienas kraštinis požymis gali pasitaikyti dažnai; vien šis požymis neįrodo anomalijos.', '',
              'Klaidų pasiskirstymas pagal pakartojimą:', '']
    for repeat, row in repeat_summary.iterrows():
        lines.append(f'- Pakartojimas {int(repeat)+1}: {int(row.errors)}/{int(row.predictions)} ({row.error_rate:.1%}).')
    lines += ['', 'Visų kryptinių klasių porų klaidų skaičiai ir dalys pateikti `class_pair_errors.csv`. '
              'Po 10 skirtingų įrašų su didžiausiu diagnostiniu tarpu klaidų ir mažiausiu tarpu teisingų prognozių pateikti atitinkamuose CSV.', '',
              'Požymių trūkumo jautrumas: kiekviename išoriniame teste vienas požymis visiškai paslepiamas, o jo reikšmės užpildomos mokymo medianomis. '
              'Tai papildomas diagnostinis bandymas, atskiras nuo atsitiktinių 5 % ir 10 % langelių trūkumo; jo rezultatai nenaudoti modelio atrankai.', '']
    for name, row in sensitivity.head(5).iterrows():
        lines.append(f'- `{name}`: vidutinis Macro-F1 kritimas {row.f1_drop_mean:.3f} ± {row.f1_drop_sd:.3f}.')
    lines += ['', 'Požymių permutacija ir trūkumas yra skirtingi trikdžiai, todėl jų reitingai nebūtinai sutampa. '
              'Koreliuoti požymiai ir klasių sudėties skirtumai riboja priežastines interpretacijas.']
    return lines
