"""Exploratory car-pair specialist, evaluated on the original 50 outer test splits.

The feature-selection step is a small, reproducible adaptation of the feature
subset question in Yang et al. (2024), not an implementation of their whale
optimizer. No external examples or test labels are added to training.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from run_experiment import corrected_ci, make_outer_splits
from src.data import CLASSES, load_vehicle


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results" / "improvement_20260928"
BASE = ROOT / "results" / "main"
CAR = {"opel", "saab"}


def specialist(seed: int):
    chain = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("select", SelectKBest(score_func=f_classif)),
        ("model", SVC(kernel="rbf", random_state=seed)),
    ])
    # Feature selection, scaling and imputation are refit within each inner fold.
    grid = {
        "select__k": [6, 12, 18],
        "model__C": [1, 10],
        "model__gamma": ["scale", 0.01],
    }
    return GridSearchCV(chain, grid, scoring="f1_macro",
                        cv=StratifiedKFold(5, shuffle=True, random_state=seed),
                        n_jobs=1, refit=True, error_score="raise")


def summarize(preds, fitted):
    p = pd.DataFrame(preds)
    p.to_csv(OUT / "out_of_fold_predictions.csv", index=False)
    f = pd.DataFrame(fitted)
    f.to_csv(OUT / "fold_metrics.csv", index=False)
    matrix = confusion_matrix(p.true, p.improved, labels=CLASSES)
    pd.DataFrame(matrix, index=CLASSES, columns=CLASSES).to_csv(OUT / "confusion_improved.csv")
    metrics = {}
    for name in ["original", "improved"]:
        precision, recall, score, support = precision_recall_fscore_support(
            p.true, p[name], labels=CLASSES, zero_division=0)
        metrics[name] = {
            "macro_f1_fold_mean": float(f[f.method == name].macro_f1.mean()),
            "opel_saab_f1_mean": float(np.mean(score[1:3])),
            "per_class": {label: {"precision": float(precision[i]), "recall": float(recall[i]),
                                  "f1": float(score[i]), "support": int(support[i])}
                          for i, label in enumerate(CLASSES)},
        }
    pair = f.pivot(index="split", columns="method", values="macro_f1")
    diff = pair.improved - pair.original
    metrics["paired_macro_f1_difference"] = float(diff.mean())
    metrics["corrected_95pct_interval"] = corrected_ci(diff, 84.6, 761.4)
    metrics["improved_folds"] = int((diff > 0).sum())
    metrics["worse_folds"] = int((diff < 0).sum())
    metrics["fits_estimate"] = 50 * (12 * 5 + 1)
    (OUT / "summary.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=2), flush=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    X, y, _ = load_vehicle(ROOT / "data")
    cfg = __import__("yaml").safe_load((ROOT / "configs" / "main.yaml").read_text(encoding="utf-8"))
    old = pd.read_csv(BASE / "out_of_fold_predictions.csv")
    old = old[old.method == "svm"]
    rows, folds = [], []
    for split, (repeat, fold, train, test) in enumerate(make_outer_splits(X, y, cfg)):
        saved = old[old.split == split].set_index("row_index").loc[test]
        assert np.array_equal(saved.true.to_numpy(), y.iloc[test].to_numpy())
        assert not (set(train) & set(test))
        car_train = [i for i in train if y.iloc[i] in CAR]
        seed = int(cfg["seed"] + repeat * 100 + fold)
        start = time.perf_counter()
        search = specialist(seed).fit(X.iloc[car_train], y.iloc[car_train])
        elapsed = time.perf_counter() - start
        selected = list(X.columns[search.best_estimator_.named_steps["select"].get_support()])
        original = saved.predicted.to_numpy().astype(str)
        improved = original.copy()
        car_mask = np.isin(original, list(CAR))
        improved[car_mask] = search.predict(X.iloc[test].iloc[car_mask])
        for method, guess in [("original", original), ("improved", improved)]:
            folds.append({"split": split, "repeat": repeat, "fold": fold, "method": method,
                          "macro_f1": f1_score(y.iloc[test], guess, labels=CLASSES,
                                               average="macro", zero_division=0)})
        rows.extend({"split": split, "repeat": repeat, "fold": fold, "row_index": int(i),
                     "true": truth, "original": a, "improved": b}
                    for i, truth, a, b in zip(test, y.iloc[test], original, improved))
        with (OUT / "search_log.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"split": split, "params": search.best_params_,
                                     "inner_macro_f1": search.best_score_,
                                     "features": selected, "fit_seconds": elapsed}, ensure_ascii=False) + "\n")
        print(f"{split + 1}/50: {folds[-1]['macro_f1']:.3f}; {search.best_params_}", flush=True)
        summarize(rows, folds)
    # Training the operational specialist uses all 846 labels, after evaluation.
    full = specialist(int(cfg["seed"])).fit(X[y.isin(CAR)], y[y.isin(CAR)])
    joblib.dump({"base": joblib.load(BASE / "final_svm.joblib"), "specialist": full.best_estimator_,
                 "features": list(X.columns), "specialist_params": full.best_params_},
                OUT / "final_hybrid.joblib")


if __name__ == "__main__":
    main()
