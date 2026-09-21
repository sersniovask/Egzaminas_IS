"""OpenML Vehicle duomenys ir griežta įvesties schemos patikra."""
from __future__ import annotations

import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import arff

OPENML_URL = "https://openml.org/data/v1/download/54/vehicle.arff"
OPENML_MD5 = "fbba18157b188f309d772f9ca4e578f5"
CLASSES = ["bus", "opel", "saab", "van"]


def load_vehicle(cache_dir: Path):
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / "vehicle.arff"
    if not path.exists():
        # Tiesioginė oficialaus OpenML failo nuoroda; vietinė kopija leidžia pakartoti bandymą.
        urllib.request.urlretrieve(OPENML_URL, path)
    digest = hashlib.md5(path.read_bytes()).hexdigest()
    if digest != OPENML_MD5:
        raise ValueError(f"OpenML failo MD5 neatitinka metaduomenų: {digest}")
    raw, _ = arff.loadarff(path)
    frame = pd.DataFrame(raw)
    if "Class" not in frame.columns:
        raise ValueError("Nėra tikslinio Class stulpelio")
    y = frame.pop("Class").map(lambda v: v.decode() if isinstance(v, bytes) else str(v))
    X = frame.apply(pd.to_numeric, errors="raise")
    if X.shape != (846, 18) or sorted(y.unique()) != CLASSES:
        raise ValueError(f"Netikėta duomenų schema: {X.shape}, {sorted(y.unique())}")
    if not np.isfinite(X.to_numpy()).all():
        raise ValueError("Pradiniuose duomenyse yra NaN arba begalybė")
    metadata = {
        "source": OPENML_URL, "openml_id": 54, "version": 1,
        "md5": digest, "rows": len(X), "features": list(X.columns),
        "cached_file_modified_utc": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
        "class_counts": y.value_counts().sort_index().to_dict(),
        "duplicate_rows": int(pd.concat([X, y.rename("Class")], axis=1).duplicated().sum()),
        "missing_cells": int(X.isna().sum().sum()),
        "feature_stats": {
            name: {"min": float(X[name].min()), "max": float(X[name].max()),
                   "median": float(X[name].median()), "variance": float(X[name].var(ddof=0))}
            for name in X.columns
        },
        "constant_features": [name for name in X.columns if X[name].nunique() <= 1],
    }
    return X, y, metadata


def validate_record(record: dict, feature_names: list[str]) -> pd.DataFrame:
    if set(record) != set(feature_names):
        raise ValueError("Įraše turi būti tiksliai tie patys 18 požymių pavadinimų")
    row = pd.DataFrame([{name: record[name] for name in feature_names}])
    row = row.apply(pd.to_numeric, errors="raise")
    # NaN leidžiamas: mokymo metu išmoktas imputatorius jį užpildys.
    if np.isinf(row.to_numpy()).any():
        raise ValueError("Begalybės reikšmė neleidžiama")
    return row
