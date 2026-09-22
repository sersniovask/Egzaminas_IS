"""Nepriklausomas išsaugotų rezultatų, indeksų ir modelio auditas."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml
from scipy import stats
from sklearn.model_selection import StratifiedKFold

from src.data import CLASSES, OPENML_MD5, load_vehicle
from src.provenance import peak_rss_bytes
from src.source_audit import verify_training_source

METHODS = {"centroid", "knn", "svm", "mlp", "rbf", "svm_linear", "svm_unscaled"}


# Atskirai suskaičiuoja TP, FP ir FN kiekvienai klasei ir grąžina Macro-F1 bei jautrumų vidurkį.
def manual_scores(true, predicted):
    """Metrikos iš TP, FP ir FN, nenaudojant eksperimentinio metrikų kodo."""
    true = np.asarray(true)
    predicted = np.asarray(predicted)
    recalls, f1_values = [], []
    for label in CLASSES:
        # TP – teisingai aptikta ši klasė; FP – klaidingai priskirta; FN – nepastebėta.
        tp = int(np.sum((true == label) & (predicted == label)))
        fp = int(np.sum((true != label) & (predicted == label)))
        fn = int(np.sum((true == label) & (predicted != label)))
        recalls.append(tp / (tp + fn))
        f1_values.append(2 * tp / (2 * tp + fp + fn))
    return float(np.mean(f1_values)), float(np.mean(recalls))


# Nepriklausomai atkuria tikėtinus skaidinių indeksus iš išsaugotos konfigūracijos.
def expected_splits(X, y, cfg):
    for repeat, seed in enumerate(cfg["outer_seeds"]):
        cv = StratifiedKFold(n_splits=cfg["outer_folds"], shuffle=True, random_state=seed)
        for fold, (train, test) in enumerate(cv.split(X, y)):
            yield repeat, fold, train, test


# Sutikrina duomenų tapatybę, prognozes, metrikas, skaidinius, modelį ir paieškos biudžetą.
# Tik visoms patikroms praėjus įrašo verification.json su statusu passed.
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", default="results/main")
    parser.add_argument("--cache", default="data")
    args = parser.parse_args()
    root = Path(args.results)
    cfg = yaml.safe_load((root / "run_config.yaml").read_text(encoding="utf-8"))
    X, y, actual_metadata = load_vehicle(Path(args.cache))
    saved_metadata = json.loads((root / "data_metadata.json").read_text(encoding="utf-8"))
    assert saved_metadata["md5"] == OPENML_MD5 == hashlib.md5((Path(args.cache) / "vehicle.arff").read_bytes()).hexdigest()
    assert saved_metadata["class_counts"] == actual_metadata["class_counts"]
    folds = pd.read_csv(root / "fold_metrics.csv")
    preds = pd.read_csv(root / "out_of_fold_predictions.csv")
    assert len(folds) == 50 * len(METHODS)
    assert len(preds) == len(METHODS) * len(X) * len(cfg["outer_seeds"])
    assert set(folds.method) == METHODS == set(preds.method)
    assert not folds[["split", "method"]].duplicated().any()
    assert preds[["split", "method", "row_index"]].duplicated().sum() == 0
    assert set(preds.true) <= set(CLASSES) and set(preds.predicted) <= set(CLASSES)

    split_list = list(expected_splits(X, y, cfg))
    assert len(split_list) == 50
    for split_id, (repeat, fold, train, test) in enumerate(split_list):
        # Mokymo ir testo indeksų sankirta turi būti tuščia – objektas negali būti abiejose dalyse.
        assert not set(train) & set(test)
        for method in METHODS:
            rows = preds[(preds.split == split_id) & (preds.method == method)].sort_values("row_index")
            record = folds[(folds.split == split_id) & (folds.method == method)].iloc[0]
            assert record["repeat"] == repeat and record["fold"] == fold
            assert np.array_equal(rows.row_index.to_numpy(), np.sort(test))
            assert np.array_equal(rows.true.to_numpy(), y.iloc[rows.row_index].to_numpy())
            f1, ba = manual_scores(rows.true, rows.predicted)
            assert np.isclose(record.macro_f1, f1, atol=1e-12)
            assert np.isclose(record.balanced_accuracy, ba, atol=1e-12)

    # Kiekvienas objektas kiekviename pakartojime vertintas lygiai vieną kartą.
    for method in METHODS:
        for repeat in range(5):
            indexes = preds[(preds.method == method) & (preds.repeat == repeat)].row_index
            assert sorted(indexes.tolist()) == list(range(len(X)))
        matrix = pd.read_csv(root / f"confusion_{method}.csv", index_col=0)
        subset = preds[preds.method == method]
        independent = pd.crosstab(subset.true, subset.predicted).reindex(index=CLASSES, columns=CLASSES, fill_value=0)
        assert np.array_equal(matrix.to_numpy(), independent.to_numpy())

    summary = pd.read_csv(root / "results_summary.csv", index_col=0)
    for method in METHODS:
        subset = folds[folds.method == method]
        assert np.isclose(summary.loc[method, "macro_f1_mean"], subset.macro_f1.mean())
        assert np.isclose(summary.loc[method, "macro_f1_sd"], subset.macro_f1.std(ddof=1))
        assert np.isclose(summary.loc[method, "balanced_accuracy_mean"], subset.balanced_accuracy.mean())

    baseline = summary.loc[["centroid", "knn"], "macro_f1_mean"].idxmax()
    paired = folds.pivot(index="split", columns="method", values="macro_f1")
    diff = paired.svm - paired[baseline]
    ratio = (len(X) / 10) / (len(X) - len(X) / 10)
    se = np.sqrt((1 / 50 + ratio) * diff.var(ddof=1))
    radius = stats.t.ppf(.975, 49) * se
    hypothesis = json.loads((root / "hypothesis.json").read_text(encoding="utf-8"))
    assert hypothesis["baseline"] == baseline
    assert np.isclose(hypothesis["mean_difference"], diff.mean())
    assert np.allclose(hypothesis["corrected_95pct_ci"], [diff.mean() - radius, diff.mean() + radius])

    robust = pd.read_csv(root / "robustness.csv")
    assert len(robust) == 50 * 5 * 5 * cfg["robustness_repeats"]
    assert not robust[["split", "method", "kind", "level", "realization"]].duplicated().any()
    importance = pd.read_csv(root / "feature_permutation.csv")
    assert len(importance) == 50 * 18

    final = joblib.load(root / "final_svm.joblib")
    assert final["feature_names"] == list(X.columns)
    assert final["openml_md5"] == OPENML_MD5
    # Funkcinė modelio įkėlimo patikra; šie įrašai nėra naujas nepriklausomas tikslumo testas.
    sample_predictions = final["pipeline"].predict(X.iloc[:3])
    assert len(sample_predictions) == 3 and set(sample_predictions) <= set(CLASSES)
    assert final["pipeline"].decision_function(X.iloc[:3]).shape == (3, 6)

    resources = json.loads((root / "resources.json").read_text(encoding="utf-8"))
    assert resources['model_fits'] <= 20000
    assert resources['within_fit_budget'] and resources['within_memory_budget'] and resources['within_time_budget']
    assert (folds.predict_seconds >= 0).all()
    assert final['model_version'] and len(final['code_sha256']) == 64
    missing_features = pd.read_csv(root / 'missing_feature_sensitivity.csv')
    assert len(missing_features) == 900 and not missing_features[['split', 'feature']].duplicated().any()
    edge_records = pd.read_csv(root / 'error_edges.csv')
    assert len(edge_records) == 4230
    svm_rows = preds[preds.method == 'svm'].set_index(['split', 'row_index'])
    joined = edge_records.set_index(['split', 'row_index']).join(svm_rows[['true', 'predicted']])
    assert (joined.error == (joined.true != joined.predicted)).all()
    assert joined.edge_features.between(0, 18).all()
    clean_scores = folds[folds.method == 'svm'].set_index('split').macro_f1
    assert np.allclose(missing_features.f1_drop, missing_features['split'].map(clean_scores) - missing_features.macro_f1)
    assert missing_features.macro_f1.between(0, 1).all()
    provenance = json.loads((root / 'provenance.json').read_text(encoding='utf-8'))
    assert final['code_sha256'] == provenance['code_sha256']
    project = Path(__file__).resolve().parent
    for relative in ['run_experiment.py', 'src/data.py', 'src/models.py', 'configs/main.yaml']:
        key = next(k for k in provenance['file_sha256'] if k.replace('\\', '/') == relative)
        # Originalus manifestas išlieka nepakeistas; dokumentuoti failai tikrinami prieš archyvą.
        verify_training_source(project, relative, provenance['file_sha256'][key])
    fit_count = 100
    for split in range(50):
        for method, expected_candidates in [('svm',20), ('mlp',12), ('rbf',18), ('svm_linear',4), ('svm_unscaled',20)]:
            search = pd.read_csv(root / 'inner_search' / f'{split:02d}_{method}.csv')
            assert len(search) == expected_candidates
            assert search.mean_test_score.notna().all()
            fit_count += 5 * len(search) + 1
    final_search = pd.read_csv(root / 'inner_search' / 'final_svm.csv')
    fit_count += 5 * len(final_search) + 1
    assert fit_count == resources['model_fits']
    evidence = {"status": "passed", "verification_peak_rss_bytes": peak_rss_bytes(), "fit_budget_checked": True, "inner_search_tables": 251,
                "model_fits": fit_count, "runtime_and_memory_checked": True, "outer_splits": 50, "model_variants": 7,
                "fold_records": len(folds), "prediction_records": len(preds),
                "robustness_records": len(robust), "permutation_records": len(importance),
                "data_md5": OPENML_MD5, "manual_metric_recalculation": True,
                "same_test_indices_for_all_models": True, "final_model_predicts": True}
    (root / "verification.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print("Verification passed: 50 splits, 7 models, predictions, metrics and final model.")


if __name__ == "__main__":
    main()
