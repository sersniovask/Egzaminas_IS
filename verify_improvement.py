"""Independent checks for the two post-feedback experiments."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

from src.data import CLASSES, load_vehicle

ROOT = Path(__file__).resolve().parent
X, y, _ = load_vehicle(ROOT / "data")
original = pd.read_csv(ROOT / "results/main/out_of_fold_predictions.csv")
original = original[original.method == "svm"]

for variant, name in [("improvement_20260928", "improved"),
                      ("wide_svm_20260928", "wide_svm")]:
    folder = ROOT / "results" / variant
    current = pd.read_csv(folder / "out_of_fold_predictions.csv")
    folds = pd.read_csv(folder / "fold_metrics.csv")
    assert len(current) == 5 * len(X) == 4230
    assert len(folds) == 100
    assert not current[["split", "row_index"]].duplicated().any()
    for split in range(50):
        new = current[current.split == split].sort_values("row_index")
        old = original[original.split == split].sort_values("row_index")
        assert np.array_equal(new.row_index.to_numpy(), old.row_index.to_numpy())
        assert np.array_equal(new.true.to_numpy(), y.iloc[new.row_index].to_numpy())
        assert np.array_equal(new.original.to_numpy(), old.predicted.to_numpy())
        for method, col in [("original", "original"), (name, name)]:
            expected = f1_score(new.true, new[col], labels=CLASSES, average="macro")
            saved = folds[(folds.split == split) & (folds.method == method)].iloc[0].macro_f1
            assert np.isclose(expected, saved)
    info = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
    assert np.isclose(info[name]["macro_f1_fold_mean"], folds[folds.method == name].macro_f1.mean())
    assert np.isclose(info["original"]["macro_f1_fold_mean"], folds[folds.method == "original"].macro_f1.mean())
    print(f"Verified {variant}: 50 common test splits, 4,230 matching rows, independent F1 recalculation")

artifact = joblib.load(ROOT / "results/wide_svm_20260928/final_wide_svm.joblib")
assert artifact["feature_names"] == list(X.columns)
assert len(artifact["pipeline"].predict(X.iloc[:2])) == 2
print("Verified updated operational model loads and predicts")
