"""Recompute fold identity and all new outer-test metrics from saved predictions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold

from experiment_next_20260928 import OUT, ROOT, split_hash
from src.data import CLASSES, load_vehicle


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--read-only", action="store_true",
                        help="Patikrinti rezultatus neperrašant verification.json")
    args = parser.parse_args()
    X, y, metadata = load_vehicle(ROOT / "data")
    cfg = yaml.safe_load((ROOT / "configs" / "main.yaml").read_text(encoding="utf-8"))
    old = pd.read_csv(ROOT / "results" / "wide_svm_20260928" /
                      "out_of_fold_predictions.csv")
    report = {"data_md5": metadata["md5"], "models": {}}
    for name in ["svm_extended", "extra_trees", "tabpfn_v2"]:
        directory = OUT / name / "splits"
        checked = 0
        predictions = 0
        scores = []
        for repeat, seed in enumerate(cfg["outer_seeds"]):
            splitter = StratifiedKFold(n_splits=cfg["outer_folds"],
                                       shuffle=True, random_state=seed)
            for fold, (train, test) in enumerate(splitter.split(X, y)):
                split = repeat * cfg["outer_folds"] + fold
                path = directory / f"{split:02d}.json"
                if not path.exists():
                    continue
                row = json.loads(path.read_text(encoding="utf-8"))
                assert row["model"] == name and row["split"] == split
                assert row["repeat"] == repeat and row["fold"] == fold
                assert row["split_hash"] == split_hash(train, test)
                assert row["train_size"] == len(train)
                assert row["test_indices"] == test.tolist()
                assert not set(train).intersection(test)
                assert row["true"] == y.iloc[test].tolist()
                saved_old = old[old.split == split].set_index("row_index").loc[test]
                assert saved_old.true.tolist() == row["true"]
                actual_f1 = f1_score(row["true"], row["predicted"],
                                     labels=CLASSES, average="macro")
                assert np.isclose(actual_f1, row["test_macro_f1"], atol=1e-12)
                scores.append(actual_f1)
                checked += 1
                predictions += len(test)
        report["models"][name] = {"verified_splits": checked,
                                  "verified_predictions": predictions,
                                  "mean_outer_macro_f1": float(np.mean(scores)) if scores else None}
    if not args.read_only:
        (OUT / "verification.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if any(value["verified_splits"] != 50 for value in report["models"].values()):
        raise SystemExit("At least one model is still incomplete")


if __name__ == "__main__":
    main()
