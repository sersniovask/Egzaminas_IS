"""Fit the exploratory TabPFN candidate on all 846 rows after CV evaluation."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import numpy as np
import sklearn
import tabpfn
import torch
from tabpfn import TabPFNClassifier

from src.data import CLASSES, load_vehicle

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results" / "further_20260928" / "tabpfn_v2"


def main():
    summary = json.loads((OUT / "summary.json").read_text(encoding="utf-8"))
    if summary["completed_splits"] != 50:
        raise RuntimeError("First finish all 50 outer tests and their summary")
    X, y, data = load_vehicle(ROOT / "data")
    estimator = TabPFNClassifier(device="cpu", n_estimators=4, random_state=2026)
    estimator.fit(X, y)
    OUT.mkdir(parents=True, exist_ok=True)
    model_path = OUT / "final_tabpfn_v2.tabpfn_fit"
    estimator.save_fit_state(model_path)
    loaded = TabPFNClassifier.load_from_fit_state(model_path, device="cpu")
    sample = X.iloc[:3]
    if not np.array_equal(estimator.predict(sample), loaded.predict(sample)):
        raise AssertionError("Saved TabPFN predictions changed after reload")
    checkpoint = Path(os.environ["APPDATA"]) / "tabpfn" / "tabpfn-v2-classifier-finetuned-zk73skhh.ckpt"
    if not checkpoint.exists():
        raise RuntimeError(f"Official TabPFN v2 checkpoint missing: {checkpoint}")
    meta = {
        "training_rows": len(X), "classes": CLASSES,
        "feature_names": list(X.columns), "data_md5": data["md5"],
        "model_sha256": hashlib.sha256(model_path.read_bytes()).hexdigest(),
        "foundation_checkpoint_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        "foundation_checkpoint_source": "https://huggingface.co/Prior-Labs/TabPFN-v2-clf",
        "tabpfn": tabpfn.__version__, "torch": torch.__version__,
        "sklearn": sklearn.__version__, "n_estimators": 4,
        "trained_after_cross_validation": True,
        "training_set_accuracy_not_reported_as_test_result": True,
        "external_foundation_weights_required_on_load": True,
    }
    (OUT / "final_model_metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
