"""Verify checkpointed outer predictions and write descriptive comparisons."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support

from run_experiment import corrected_ci
from src.data import CLASSES, load_vehicle

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results" / "further_20260928"
PRIOR = ROOT / "results" / "wide_svm_20260928" / "out_of_fold_predictions.csv"


def main():
    X, y, _ = load_vehicle(ROOT / "data")
    baseline = pd.read_csv(PRIOR)
    all_summaries = {}
    for model_dir in sorted(OUT.iterdir()):
        if not model_dir.is_dir():
            continue
        files = sorted((model_dir / "splits").glob("[0-9][0-9].json"))
        if not files:
            continue
        rows = []
        folds = []
        params = []
        for path in files:
            data = json.loads(path.read_text(encoding="utf-8"))
            split = int(data["split"])
            if path.stem != f"{split:02d}" or len(data["test_indices"]) != len(data["true"]):
                raise AssertionError(f"Invalid checkpoint: {path}")
            old = baseline[baseline.split == split].set_index("row_index").loc[data["test_indices"]]
            if old.true.tolist() != data["true"]:
                raise AssertionError(f"Test labels or order changed: {path}")
            if f1_score(data["true"], data["predicted"], labels=CLASSES,
                        average="macro") != data["test_macro_f1"]:
                raise AssertionError(f"Stored metric does not match predictions: {path}")
            for index, truth, new, original, wide in zip(
                    data["test_indices"], data["true"], data["predicted"],
                    old.original.tolist(), old.wide_svm.tolist()):
                rows.append({"split": split, "repeat": data["repeat"],
                             "fold": data["fold"], "row_index": index,
                             "true": truth, "new": new, "original": original,
                             "wide_svm": wide})
            for name, predictions in [
                (model_dir.name, data["predicted"]),
                ("original", old.original.tolist()),
                ("wide_svm", old.wide_svm.tolist()),
            ]:
                car_f1 = f1_score(data["true"], predictions,
                                  labels=["opel", "saab"], average=None,
                                  zero_division=0)
                folds.append({"split": split, "repeat": data["repeat"],
                              "fold": data["fold"], "model": name,
                              "macro_f1": f1_score(data["true"], predictions,
                                                   labels=CLASSES, average="macro"),
                              "opel_f1": float(car_f1[0]),
                              "saab_f1": float(car_f1[1]),
                              "car_f1_mean": float(np.mean(car_f1))})
            params.append(json.dumps(data["params"], sort_keys=True))
        preds = pd.DataFrame(rows).sort_values(["split", "row_index"])
        metrics = pd.DataFrame(folds).sort_values(["split", "model"])
        preds.to_csv(model_dir / "paired_predictions.csv", index=False)
        metrics.to_csv(model_dir / "paired_fold_metrics.csv", index=False)
        summary = {"model": model_dir.name, "completed_splits": len(files),
                   "total_test_predictions": len(preds), "distinct_records": int(preds.row_index.nunique()),
                   "outer_splits_exploratory": True,
                   "parameter_counts": dict(Counter(params))}
        for name, col in [(model_dir.name, "new"), ("original", "original"),
                          ("wide_svm", "wide_svm")]:
            f = metrics[metrics.model == name]
            pr, re, f1, support = precision_recall_fscore_support(
                preds.true, preds[col], labels=CLASSES, zero_division=0)
            summary[name] = {
                "mean_outer_fold_macro_f1": float(f.macro_f1.mean()),
                "per_class_pooled": {label: {"precision": float(pr[i]),
                                            "recall": float(re[i]), "f1": float(f1[i]),
                                            "repeated_support": int(support[i])}
                                     for i, label in enumerate(CLASSES)},
                "opel_saab_cross_errors": int(((preds.true == "opel") & (preds[col] == "saab")).sum()
                                               + ((preds.true == "saab") & (preds[col] == "opel")).sum()),
            }
            cm = confusion_matrix(preds.true, preds[col], labels=CLASSES)
            pd.DataFrame(cm, index=CLASSES, columns=CLASSES).to_csv(
                model_dir / f"confusion_{name}.csv")
        pivot = metrics.pivot(index="split", columns="model", values="macro_f1")
        diff = pivot[model_dir.name] - pivot.wide_svm
        car_pivot = metrics.pivot(index="split", columns="model", values="car_f1_mean")
        car_diff = car_pivot[model_dir.name] - car_pivot.wide_svm
        summary["versus_wide_svm"] = {
            "mean_paired_difference": float(diff.mean()),
            "mean_paired_car_f1_difference": float(car_diff.mean()),
            "better_splits": int((diff > 0).sum()),
            "equal_splits": int((diff == 0).sum()),
            "worse_splits": int((diff < 0).sum()),
            "corrected_95pct_interval_descriptive": (
                corrected_ci(diff, 84.6, 761.4) if len(files) == 50 else None),
            "corrected_95pct_car_interval_descriptive": (
                corrected_ci(car_diff, 84.6, 761.4) if len(files) == 50 else None),
        }
        (model_dir / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        all_summaries[model_dir.name] = summary
        print(model_dir.name, json.dumps({
            "folds": len(files),
            "macro_f1": summary[model_dir.name]["mean_outer_fold_macro_f1"],
            "opel_f1": summary[model_dir.name]["per_class_pooled"]["opel"]["f1"],
            "saab_f1": summary[model_dir.name]["per_class_pooled"]["saab"]["f1"],
            "vs_wide": summary["versus_wide_svm"]["mean_paired_difference"],
        }), flush=True)
    (OUT / "all_summaries.json").write_text(
        json.dumps(all_summaries, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
