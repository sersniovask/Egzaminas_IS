"""Descriptive audit of repeated Opel/Saab errors; never used to train models."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

from src.data import load_vehicle

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results" / "further_20260928" / "diagnosis"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    X, y, metadata = load_vehicle(ROOT / "data")
    frequency = pd.read_csv(ROOT / "results" / "main" / "error_frequency_by_record.csv")
    frequency = frequency.set_index("row_index").loc[np.arange(len(X))]
    assert frequency.true.tolist() == y.tolist()
    cars = np.flatnonzero(y.isin(["opel", "saab"]).to_numpy())
    Z = StandardScaler().fit_transform(X.iloc[cars])
    D = pairwise_distances(Z)
    np.fill_diagonal(D, np.inf)
    car_labels = y.iloc[cars].to_numpy()
    records = []
    for i, row_index in enumerate(cars):
        same = np.where(car_labels == car_labels[i])[0]
        opposite = np.where(car_labels != car_labels[i])[0]
        nearest_same = float(D[i, same].min())
        nearest_opposite = float(D[i, opposite].min())
        five = np.argsort(D[i])[:5]
        records.append({
            "row_index": int(row_index), "true": car_labels[i],
            "errors_in_five_tests": int(frequency.loc[row_index, "errors_in_five_tests"]),
            "nearest_same_distance": nearest_same,
            "nearest_opposite_distance": nearest_opposite,
            "opposite_closer": bool(nearest_opposite < nearest_same),
            "opposite_among_five_nearest": int((car_labels[five] != car_labels[i]).sum()),
            "nearest_opposite_row_index": int(cars[opposite[np.argmin(D[i, opposite])]]),
        })
    frame = pd.DataFrame(records)
    frame.to_csv(OUT / "car_neighborhoods.csv", index=False)
    duplicates = X.duplicated(keep=False)
    cross_label_duplicate_groups = 0
    if duplicates.any():
        joined = X[duplicates].copy()
        joined["target"] = y[duplicates]
        cross_label_duplicate_groups = int(sum(
            group.target.nunique() > 1
            for _, group in joined.groupby(list(X.columns), dropna=False)))
    summary = {
        "data_md5": metadata["md5"], "car_rows": len(cars),
        "persistent_errors_all_classes": int((frequency.errors_in_five_tests == 5).sum()),
        "persistent_car_errors": int((frame.errors_in_five_tests == 5).sum()),
        "feature_duplicate_rows": int(duplicates.sum()),
        "cross_label_duplicate_groups": cross_label_duplicate_groups,
        "analysis_uses_all_labels": True,
        "must_not_be_used_for_training_or_independent_test_selection": True,
    }
    for name, group in [("persistent", frame[frame.errors_in_five_tests == 5]),
                        ("never_wrong", frame[frame.errors_in_five_tests == 0])]:
        summary[name] = {
            "rows": len(group),
            "opposite_closer_fraction": float(group.opposite_closer.mean()),
            "median_opposite_among_five_nearest": float(group.opposite_among_five_nearest.median()),
            "median_nearest_opposite_distance": float(group.nearest_opposite_distance.median()),
        }
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
