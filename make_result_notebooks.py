"""Rezultatų sąsiuviniai; --execute išsaugo grafikus ir lenteles be naujo mokymo."""
import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil
import nbformat as nbf

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.matplotlib'))
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
METHODS = {'svm': 'SVM su RBF branduoliu', 'mlp': 'Daugiasluoksnis perceptronas MLP', 'rbf': 'RBF tinklas'}
SETUP = '''%matplotlib inline
from src.notebook_report import (
    load_results, table, key_metrics, comparison_plot, class_analysis,
    error_examples, robustness_analysis, ablations, interpretation, hypothesis)
# Skaitomi baigto eksperimento CSV. Modeliai čia nemokomi.
data = load_results()
print('Patikrinti rezultatai: 50 išorinių skaidinių, 7 variantai, 846 įrašai.')
'''
PROTOCOL = '''846 įrašai, 18 požymių, keturios klasės. Visiems metodams naudoti tie patys **5 × 10 stratifikuoti išoriniai skaidiniai**. Parametrai parinkti atskira **5 dalių vidine CV** pagal Macro-F1. Medianų pildymas ir standartizavimas išmokti mokymo dalyse. Išorinis testas nenaudotas parinkimui.

**SD** yra skaidinių rezultatų standartinis nuokrypis, ne pasikliautinasis intervalas. Skaidiniai priklausomi. Klasių metrikose ir painiavos matricoje kiekvienas įrašas pasirodo penkis kartus – iš viso 4 230 prognozių vienam modeliui. Klasių metrikos skaičiuotos iš sujungtų prognozių, pagrindinis Macro-F1 – kaip 50 skaidinių vidurkis.

Tinklelių sumažinimas dėl biudžeto aprašytas [plano_patikslinimai.md](plano_patikslinimai.md). Rezultatai galioja mažam keturių modelių rinkiniui; realaus eismo ir naujų fizinių modelių veikimas nepatikrintas.'''
FORMULAS = {
 'svm': r'''$K(z,z')=\exp(-\gamma\|z-z'\|^2)$, kur $z$ – mokymo dalyje standartizuoti požymiai, $\gamma$ valdo branduolio plotį. `src/models.py::build_pipeline` sukuria `SVC(kernel="rbf", decision_function_shape="ovo")`; `grid_for` perduoda `C` ir `gamma` vidinei paieškai. `C` valdo minkšto tarpo klaidų baudą. Keturioms klasėms gaunami šeši poriniai klasifikatoriai. Diagnostiniai balai nėra tikimybės; balsų lygybę sprendžia bibliotekos numatytoji taisyklė.''',
 'mlp': r'''Paslėpto sluoksnio taisyklė: $h=\max(0,zW+b)$ (ReLU). `src/models.py::EncodedMLP.fit` naudoja `MLPClassifier(activation="relu", solver="adam", early_stopping=True)`. `hidden_layer_sizes` nurodo sluoksnius, `alpha` – reguliarizaciją, `learning_rate_init` – pradinį mokymosi žingsnį. Tekstinės klasės viduje užkoduojamos skaičiais ir prognozuojant atkuriamos.''',
 'rbf': r'''$\phi_j(z)=\exp(-\gamma\|z-c_j\|^2)$; $c_j$ – mokymo dalyje KMeans išmoktas centras. Kode $\gamma=1/(2w^2m)$, kur $w$ – pločio daugiklis, $m$ – teigiamų centrų porinių atstumų kvadratų mediana. `src/models.py::RBFNetwork.fit` skaičiuoja aktyvacijas ir mokosi Ridge išvestį; `predict` parenka didžiausios išvesties klasę.'''
}
TRAINING = '''RUN_TRAINING = False
if RUN_TRAINING:
    from pathlib import Path
    import pandas as pd
    import yaml
    from src.data import load_vehicle
    from run_experiment import make_outer_splits, fit_model, metrics
    cfg = yaml.safe_load(Path('configs/main.yaml').read_text(encoding='utf-8'))
    X, y, metadata = load_vehicle(Path('data'))
    rows = []
    for split, (repeat, fold, train, test) in enumerate(make_outer_splits(X, y, cfg)):
        model, params = fit_model(method, X.iloc[train], y.iloc[train], cfg,
                                  cfg['seed'] + repeat * 100 + fold, jobs=1)
        rows.append({'split': split, 'repeat': repeat, 'fold': fold,
                     **metrics(y.iloc[test], model.predict(X.iloc[test])), 'params': str(params)})
    results = pd.DataFrame(rows)
    results.to_csv(f'results/notebook_{method}.csv', index=False)
    display(results[['macro_f1', 'balanced_accuracy']].agg(['mean', 'std']))
else:
    print('Mokymas nepaleistas. Rodomi pilno išsaugoto eksperimento rezultatai.')
'''


# Sudaro vieno metodo notebooko langelius: rezultatus, paaiškinimus ir pasirenkamą mokymą.
def method_notebook(method, title):
    source = {'svm': 'build_pipeline', 'mlp': 'EncodedMLP.fit', 'rbf': 'RBFNetwork.fit'}[method]
    cells = [md(f'# {title}: rezultatai ir paaiškinimas\n\nMetrikos, grafikai ir klaidos pateikti čia. **Run → Run All Cells** atnaujina apžvalgą iš CSV; mokymas pagal nutylėjimą išjungtas.\n\n[Bendra santrauka](00_REZULTATU_SANTRAUKA.ipynb) · [Pilna ataskaita](results/main/report.md)'),
             code(SETUP + f"\nmethod = '{method}'")]
    sections = [
        ('Pagrindinės šio metodo metrikos', 'key_metrics(data, method)\ninterpretation(data, method)'),
        ('Palyginimas su abiem baseline\n\nMokymo laikas apima ir vidinę parametrų paiešką.', "table(data, [method, 'knn', 'centroid'])\ncomparison_plot(data, [method, 'knn', 'centroid'])"),
        ('Klasių metrikos ir painiavos matrica\n\nKiekvienas objektas teste pasirodo penkis kartus. Čia pateiktos sujungtų išorinių prognozių metrikos.', 'class_analysis(data, method)'),
        ('Dešimt klaidų pavyzdžių\n\nRodomi skirtingi įrašai ir dažniausia jų klaidinga klasė; vienodi dažniai sprendžiami pagal klasių tvarką. Tai klaidų pasikartojimo, ne užtikrintumo reitingas. Pradinių siluetų vaizdų faile nėra.', 'error_examples(data, method)'),
        ('Atsparumas triukšmui ir trūkstamiems požymiams\n\nTrikdžiai taikyti tik išoriniam testui: trys triukšmo lygiai, 5 % ir 10 % trūkstamų langelių, po 20 realizacijų. Visi metodai gavo tuos pačius trikdžius. Lentelėje – šis metodas, grafike – ir baseline.', 'robustness_analysis(data, method)'),
        ('Eksperimento abliacija ir požymių jautrumas\n\nŠi užduoties dalis atlikta pagrindiniam **SVM**. MLP ir RBF sąsiuviniuose tai bendro eksperimento kontekstas, ne šių alternatyvų abliacija. Permutacija ir vieno požymio visiškas trūkumas yra atskiri trikdžiai.', 'ablations(data)'),
        ('Formulė ir konkreti kodo vieta\n\n' + FORMULAS[method], f'import inspect\nfrom src.models import build_pipeline, EncodedMLP, RBFNetwork\n# Tikras naudojamos realizacijos kodas.\nprint(inspect.getsource({source}))')]
    for title, body in sections:
        cells.extend([md('## ' + title), code(body)])
    cells += [md('## Vertinimo protokolas ir ribos\n\n' + PROTOCOL),
              md('## Neprivalomas mokymo pakartojimas\n\nNustatykite `RUN_TRAINING = True` tik norėdami mokyti iš naujo. Tai trunka kelias minutes ir išsaugo atskirą `results/notebook_<metodas>.csv`. Visas eksperimentas: `python run_experiment.py --config configs/main.yaml`.'), code(TRAINING)]
    return nbf.v4.new_notebook(cells=cells)


# Sudaro bendros rezultatų santraukos langelius, grafikus ir egzamino įrodymų lentelę.
def overview():
    cells = [md('# Egzamino rezultatų santrauka\n\nKirilas Šeršniovas, PEPfm-26. Pagrindinės metrikos, palyginimas, hipotezė, abliacijos ir reikalavimų įrodymai. **Mokymo paleisti nereikia.**\n\nAtskirai: [SVM](svm_alternatyva.ipynb) · [MLP](mlp_alternatyva.ipynb) · [RBF](rbf_alternatyva.ipynb).'), code(SETUP + '\nfrom src.summary_plots import class_comparison, vehicle_groups, paired_comparison, all_robustness\n')]
    for title, body in [
        ('Penkių pagrindinių metodų palyginimas\n\nPirminė metrika – Macro-F1, antrinė – balanced accuracy. SD yra sklaida, ne intervalas.', 'table(data)\ncomparison_plot(data)'),
        ('Kurias klases lengviausia atpažinti?\n\nVisi penki metodai lyginami pagal tas pačias išorines prognozes. Kiekvienas įrašas kartojasi penkis kartus; F1 ir jautrumas skaičiuojami sujungus prognozes, o ne vidurkinant skaidinių metrikas.', 'class_comparison(data)'),
        ('Lengvieji automobiliai, furgonai ir autobusai\n\nOpel ir Saab sujungiami į lengvųjų automobilių grupę tiek tikrosiose žymėse, tiek prognozėse. Modeliai nepermokomi. Grupės skirtingo dydžio, todėl palyginimui naudojamos dalys ir F1, ne vien klaidų skaičius. Sujungtos metrikos nepakeičia pagrindinio keturių klasių vertinimo.', 'vehicle_groups(data)'),
        ('Ar pagrindinis SVM laimėjo?', "interpretation(data, 'svm')\nhypothesis(data)"),
        ('Ar pranašumas kartojasi tuose pačiuose skaidiniuose?\n\nTeigiamas skirtumas reiškia SVM pranašumą. Paskutinės dvi eilutės parodo branduolio ir standartizavimo abliacijas. Dėžutė apima kvartilius, linija žymi medianą; taškai – visi skaidiniai. 50 priklausomų skaidinių nėra 50 nepriklausomų eksperimentų, o pergalių skaičius nėra statistinio reikšmingumo įrodymas.', 'paired_comparison(data)'),
        ('Abliacija ir požymių jautrumas', 'ablations(data)'),
        ('Visų penkių metodų atsparumas ir rezultatų kritimas\n\nTrikdžiai taikyti tik išoriniam testui, visiems metodams vienodi. Triukšmo mastas remiasi mokymo dalies požymių standartiniais nuokrypiais; trūkstami langeliai užpildomi mokymo medianomis.', 'all_robustness(data)'),
        ('Pagrindinio SVM klaidos\n\nČia 4 230 susijusių prognozių: kiekvienas iš 846 įrašų vertintas penkis kartus.', "class_analysis(data, 'svm')\nerror_examples(data, 'svm')")]:
        cells.extend([md('## ' + title), code(body)])
    cells += [md('## Protokolas ir ribos\n\n' + PROTOCOL), md('''## Kur įrodyta kiekviena egzamino dalis?

| Reikalavimas | Įrodymas |
|---|---|
| Grandinė, baseline ir bent du intelektualieji metodai | `src/data.py`, `src/models.py`: medianos, standartizavimas, 5-NN, centroidas, SVM, MLP, RBF |
| Formulės ryšys su konkrečiu kodu | Kiekvieno metodo sąsiuvinio skyrius „Formulė ir konkreti kodo vieta“ |
| Tie patys skaidiniai ir metrikos, testas nenaudojamas derinimui | `run_experiment.py`, `results/main/run_config.yaml`, `inner_search/`, `verification.json` |
| Abliacija ir atsparumas | Šios santraukos grafikai ir lentelės, išsamūs CSV `results/main/` |
| Rezultatai, klaidos ir paaiškinimas | Ši santrauka, trys modelių sąsiuviniai, [pilna ataskaita](results/main/report.md) |
| Instrukcija, priklausomybės, sėklos, viena komanda | [README.md](README.md), `requirements.txt`, `configs/main.yaml`; `python run_experiment.py --config configs/main.yaml` |
| AI naudojimo auditas | [ai_log.md](ai_log.md): užklausos, priimti ir atmesti pasiūlymai, klaidos ir patikros |
| Gyvas gynimas | **Dar neatliktas.** Studentas paaiškina formulę, paleidžia dėstytojo įrašą per `predict.py` ir padaro mažą pakeitimą. Instrukcija README. |

Koliokviumo planas ir galutinis kodas nėra pažodžiui identiški: tinklelių ir versijų registravimo patikslinimai atskleisti [plano_patikslinimai.md](plano_patikslinimai.md). AI žurnalas nepakeičia studento gebėjimo paaiškinti savo darbą.'''),
        md('## Vykdymo patikra ir ištekliai'), code("import json\nfrom IPython.display import display\nfor name in ['verification.json', 'resources.json']:\n    print(name)\n    display(json.loads((data['root'] / name).read_text(encoding='utf-8')))")]
    return nbf.v4.new_notebook(cells=cells)


# Pagal CLI parinktis sugeneruoja notebookus, pasirinktinai įvykdo ir išsaugo su atsarginėmis kopijomis.
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--overview-only', action='store_true', help='Atnaujinti tik bendrą santrauką')
    args = parser.parse_args()
    notebooks = {f'{m}_alternatyva.ipynb': method_notebook(m, title) for m, title in METHODS.items()}
    if args.overview_only:
        notebooks = {}
    notebooks['00_REZULTATU_SANTRAUKA.ipynb'] = overview()
    backup = ROOT / 'results/notebook_backups' / datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    for filename, notebook in notebooks.items():
        notebook.metadata['kernelspec'] = {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
        notebook.metadata['language_info'] = {'name': 'python'}
        if args.execute:
            from nbclient import NotebookClient
            NotebookClient(notebook, timeout=180, kernel_name='python3',
                           resources={'metadata': {'path': str(ROOT)}}).execute()
        nbf.validate(notebook)
        target = ROOT / filename
        if target.exists():
            backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup / filename)
        nbf.write(notebook, target)
        print(filename, 'saved', flush=True)


if __name__ == '__main__':
    main()
