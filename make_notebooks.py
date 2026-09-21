"""Sukuria tris atskirus, tą pačią vertinimo tvarką naudojančius sąsiuvinius."""
from pathlib import Path

import nbformat as nbf

METHODS = {
    "svm": ("SVM su RBF branduoliu", "SVC minkšto tarpo optimizavimas; K(z,z')=exp(-gamma ||z-z'||²)."),
    "mlp": ("Daugiasluoksnis perceptronas", "Vienas ar du ReLU paslėpti sluoksniai, Adam ir ankstyvasis stabdymas."),
    "rbf": ("RBF tinklas", "KMeans centrai, Gauso radialinės aktyvacijos ir Ridge išvestis."),
}

for method, (title, description) in METHODS.items():
    notebook = nbf.v4.new_notebook()
    notebook.cells = [
        nbf.v4.new_markdown_cell(f"# {title}\n\n{description}\n\nŠis sąsiuvinis naudoja bendrus `src` modulius ir tą pačią kolokviume numatytą įdėtinę 5 × 10 CV. Galutinė visų metodų palyginimo ataskaita kuriama viena `run_experiment.py` komanda. Paleisti projekto šakniniame kataloge."),
        nbf.v4.new_code_cell("from pathlib import Path\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport yaml\nfrom src.data import load_vehicle\nfrom run_experiment import make_outer_splits, fit_model, metrics\n\ncfg = yaml.safe_load(Path('configs/main.yaml').read_text(encoding='utf-8'))\nX, y, metadata = load_vehicle(Path('data'))\nprint(metadata)"),
        nbf.v4.new_code_cell(f"method = '{method}'\nrows = []\nfor split, (repeat, fold, train, test) in enumerate(make_outer_splits(X, y, cfg)):\n    model, params = fit_model(method, X.iloc[train], y.iloc[train], cfg, cfg['seed'] + repeat * 100 + fold, jobs=1)\n    score = metrics(y.iloc[test], model.predict(X.iloc[test]))\n    rows.append({{'split': split, 'repeat': repeat, 'fold': fold, **score, 'params': str(params)}})\nresults = pd.DataFrame(rows)\nresults.head()"),
        nbf.v4.new_code_cell("display(results[['macro_f1', 'balanced_accuracy']].agg(['mean', 'std']))\nPath('results').mkdir(exist_ok=True)\nresults.to_csv(f'results/notebook_{method}.csv', index=False)\nresults.boxplot(column=['macro_f1', 'balanced_accuracy'])\nplt.title(f'{method}: 50 išorinių bandymų')\nplt.show()"),
        nbf.v4.new_markdown_cell("Metrikų skirtumus su baseline, abliacijas, atsparumą ir painiavos matricą pateikia pagrindinis eksperimentas. Šio sąsiuvinio rezultatai neturi būti atrenkami pagal išorinį bandymą hiperparametrams keisti."),
    ]
    notebook.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    notebook.metadata["language_info"] = {"name": "python"}
    out = Path(f"{method}_alternatyva.ipynb")
    nbf.write(notebook, out)
    print(out)
