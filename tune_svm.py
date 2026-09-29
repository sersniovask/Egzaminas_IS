"""Exploratory wider RBF SVM search with train-only feature selection."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, f1_score, precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from run_experiment import corrected_ci, make_outer_splits
from src.data import CLASSES, load_vehicle

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results" / "wide_svm_20260928"
BASE = ROOT / "results" / "main"


def build_search(seed):
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("select", SelectKBest(score_func=f_classif)),
        ("model", SVC(kernel="rbf", random_state=seed)),
    ])
    grid = {"select__k": [12, 18], "model__C": [10, 100, 1000],
            "model__gamma": [0.003, 0.01, 0.03, "scale"]}
    return GridSearchCV(model, grid, scoring="f1_macro",
                        cv=StratifiedKFold(5, shuffle=True, random_state=seed),
                        n_jobs=1, refit=True, error_score="raise")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    X, y, _ = load_vehicle(ROOT / "data")
    cfg = yaml.safe_load((ROOT / "configs" / "main.yaml").read_text(encoding="utf-8"))
    old = pd.read_csv(BASE / "out_of_fold_predictions.csv")
    old = old[old.method == "svm"]
    rows, folds, searches = [], [], []
    for split, (repeat, fold, train, test) in enumerate(make_outer_splits(X, y, cfg)):
        prior = old[old.split == split].set_index("row_index").loc[test]
        assert np.array_equal(prior.true.to_numpy(), y.iloc[test].to_numpy())
        seed = int(cfg["seed"] + repeat * 100 + fold)
        search = build_search(seed).fit(X.iloc[train], y.iloc[train])
        newer = search.predict(X.iloc[test])
        previous = prior.predicted.to_numpy()
        searches.append({"split": split, "inner_macro_f1": float(search.best_score_),
                         **search.best_params_,
                         "features": list(X.columns[search.best_estimator_.named_steps["select"].get_support()])})
        for name, pred in [("original", previous), ("wide_svm", newer)]:
            folds.append({"split": split, "repeat": repeat, "fold": fold, "method": name,
                          "macro_f1": f1_score(y.iloc[test], pred, labels=CLASSES, average="macro"),
                          "balanced_accuracy": balanced_accuracy_score(y.iloc[test], pred)})
        rows.extend({"split": split, "repeat": repeat, "fold": fold, "row_index": int(i),
                     "true": truth, "original": a, "wide_svm": b}
                    for i, truth, a, b in zip(test, y.iloc[test], previous, newer))
        print(f"{split + 1}/50: {folds[-2]['macro_f1']:.3f} -> {folds[-1]['macro_f1']:.3f}; {search.best_params_}", flush=True)
    pd.DataFrame(rows).to_csv(OUT / "out_of_fold_predictions.csv", index=False)
    pd.DataFrame(folds).to_csv(OUT / "fold_metrics.csv", index=False)
    pd.DataFrame(searches).to_json(OUT / "inner_winners.json", orient="records", force_ascii=False, indent=2)
    predictions = pd.DataFrame(rows)
    frame = pd.DataFrame(folds)
    pair = frame.pivot(index="split", columns="method", values="macro_f1")
    diff = pair.wide_svm - pair.original
    detail = {}
    for name in ["original", "wide_svm"]:
        pr, re, f1, supp = precision_recall_fscore_support(
            predictions.true, predictions[name], labels=CLASSES, zero_division=0)
        detail[name] = {"macro_f1_fold_mean": float(frame[frame.method == name].macro_f1.mean()),
                        "balanced_accuracy_fold_mean": float(frame[frame.method == name].balanced_accuracy.mean()),
                        "class_metrics": {label: {"precision": float(pr[i]), "recall": float(re[i]),
                                                  "f1": float(f1[i]), "support": int(supp[i])}
                                          for i, label in enumerate(CLASSES)}}
        cm = confusion_matrix(predictions.true, predictions[name], labels=CLASSES)
        pd.DataFrame(cm, index=CLASSES, columns=CLASSES).to_csv(OUT / f"confusion_{name}.csv")
    detail["paired_difference"] = float(diff.mean())
    detail["corrected_95pct_interval"] = corrected_ci(diff, 84.6, 761.4)
    detail["better_folds"] = int((diff > 0).sum())
    detail["worse_folds"] = int((diff < 0).sum())
    detail["extra_fits_estimate"] = 50 * (24 * 5 + 1) + 121
    (OUT / "summary.json").write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(detail, ensure_ascii=False, indent=2), flush=True)
    final = build_search(cfg["seed"]).fit(X, y)
    joblib.dump({"pipeline": final.best_estimator_, "feature_names": list(X.columns),
                 "classes": CLASSES, "params": final.best_params_}, OUT / "final_wide_svm.joblib")


if __name__ == "__main__":
    main()
