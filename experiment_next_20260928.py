"""Checkpointed exploratory comparisons on the original outer splits.

These tests reuse outer folds whose earlier results were inspected. They are
descriptive follow-up experiments, not independent confirmation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
import yaml
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import balanced_accuracy_score, f1_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.data import CLASSES, load_vehicle

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results" / "further_20260928"
VERSION = 1


def make_outer_splits(X, y, cfg):
    """Same fixed stratified folds as run_experiment.py, without extra imports."""
    for repeat, seed in enumerate(cfg["outer_seeds"]):
        splitter = StratifiedKFold(n_splits=cfg["outer_folds"], shuffle=True,
                                   random_state=seed)
        for fold, (train, test) in enumerate(splitter.split(X, y)):
            yield repeat, fold, train, test


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def split_hash(train: np.ndarray, test: np.ndarray) -> str:
    h = hashlib.sha256()
    h.update(np.asarray(train, dtype="<i8").tobytes())
    h.update(b"|")
    h.update(np.asarray(test, dtype="<i8").tobytes())
    return h.hexdigest()


def build_search(name: str, seed: int):
    if name == "svm_extended":
        chain = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", SVC(kernel="rbf")),
        ])
        grid = {
            "model__C": [100, 1000, 10000],
            "model__gamma": [0.003, 0.01, 0.03, "scale"],
        }
    elif name == "extra_trees":
        chain = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", ExtraTreesClassifier(n_estimators=150, random_state=seed,
                                            n_jobs=1)),
        ])
        grid = {
            "model__max_features": ["sqrt", 1.0],
            "model__min_samples_leaf": [1, 2, 4],
        }
    else:
        raise ValueError(name)
    cv = StratifiedKFold(5, shuffle=True, random_state=seed)
    return GridSearchCV(chain, grid, scoring="f1_macro", cv=cv,
                        n_jobs=1, refit=True, error_score="raise")


def fit_tabpfn(X_train, y_train, seed: int):
    from tabpfn import TabPFNClassifier

    # Original features contain no missing cells. The pretrained model is
    # fitted exclusively on this outer training fold.
    model = TabPFNClassifier(device="cpu", n_estimators=4, random_state=seed)
    model.fit(X_train, y_train)
    return model, {"n_estimators": 4}, None


def run(name: str, max_splits: int, resume: bool) -> None:
    X, y, metadata = load_vehicle(ROOT / "data")
    cfg = yaml.safe_load((ROOT / "configs" / "main.yaml").read_text(encoding="utf-8"))
    model_dir = OUT / name
    model_dir.mkdir(parents=True, exist_ok=True)
    atomic_json(model_dir / "run_metadata.json", {
        "version": VERSION, "model": name, "rows": len(X),
        "data_md5": metadata["md5"], "outer_seeds": cfg["outer_seeds"],
        "outer_folds": cfg["outer_folds"], "inner_folds": 5,
        "scoring": "f1_macro", "python": sys.version,
        "sklearn": sklearn.__version__, "platform": platform.platform(),
        "exploratory": True,
        "reason": "The same outer test folds were inspected during earlier model development.",
    })
    for split, (repeat, fold, train, test) in enumerate(make_outer_splits(X, y, cfg)):
        if split >= max_splits:
            break
        path = model_dir / "splits" / f"{split:02d}.json"
        digest = split_hash(train, test)
        if path.exists() and resume:
            saved = json.loads(path.read_text(encoding="utf-8"))
            if saved["split_hash"] != digest or saved["test_indices"] != test.tolist():
                raise ValueError(f"Saved split {split} does not match current data")
            print(f"{name} {split + 1}/{max_splits}: saved", flush=True)
            continue
        if set(train).intersection(test):
            raise AssertionError("Outer train/test overlap")
        seed = int(cfg["seed"] + repeat * 100 + fold)
        start = time.perf_counter()
        if name == "tabpfn_v2":
            model, params, inner_score = fit_tabpfn(X.iloc[train], y.iloc[train], seed)
        else:
            search = build_search(name, seed).fit(X.iloc[train], y.iloc[train])
            model, params, inner_score = search.best_estimator_, search.best_params_, search.best_score_
        pred = model.predict(X.iloc[test]).tolist()
        if not set(pred).issubset(CLASSES):
            raise AssertionError("Unexpected predicted label")
        actual = y.iloc[test].tolist()
        record = {
            "version": VERSION, "model": name, "split": split,
            "repeat": repeat, "fold": fold, "split_hash": digest,
            "train_size": len(train), "test_indices": test.tolist(),
            "true": actual, "predicted": pred, "seed": seed,
            "params": params, "inner_macro_f1": inner_score,
            "test_macro_f1": f1_score(actual, pred, labels=CLASSES, average="macro"),
            "test_balanced_accuracy": balanced_accuracy_score(actual, pred),
            "elapsed_seconds": time.perf_counter() - start,
        }
        atomic_json(path, record)
        print(f"{name} {split + 1}/{max_splits}: Macro-F1={record['test_macro_f1']:.3f} "
              f"{record['elapsed_seconds']:.1f}s {params}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=["svm_extended", "extra_trees", "tabpfn_v2"])
    parser.add_argument("--max-splits", type=int, default=50)
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.max_splits <= 50:
        parser.error("--max-splits must be 1..50")
    run(args.model, args.max_splits, not args.no_resume)


if __name__ == "__main__":
    main()
