"""Summarize historical inner searches and independently refit chosen MLPs."""
from __future__ import annotations

import json
import warnings
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.exceptions import ConvergenceWarning

from run_experiment import make_outer_splits
from src.data import load_vehicle
from src.models import build_pipeline


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results" / "training_audit_20260928"
BASE = ROOT / "results" / "main"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = yaml.safe_load((ROOT / "configs/main.yaml").read_text(encoding="utf-8"))
    X, y, _ = load_vehicle(ROOT / "data")
    scores = pd.read_csv(BASE / "fold_metrics.csv")
    assert len(scores) == 350
    param_rows, audit_rows = [], []
    splits = list(make_outer_splits(X, y, cfg))
    for row in scores.itertuples():
        if row.method in {"centroid", "knn"}:
            continue
        params = json.loads(row.params)
        inner = pd.read_csv(BASE / "inner_search" / f"{row.split:02d}_{row.method}.csv")
        winner = inner.loc[inner.rank_test_score.idxmin()]
        record = {"split": int(row.split), "method": row.method,
                  "inner_macro_f1": float(winner.mean_test_score),
                  "outer_macro_f1": float(row.macro_f1),
                  "inner_minus_outer": float(winner.mean_test_score - row.macro_f1),
                  "inner_candidates": len(inner), "params": json.dumps(params, sort_keys=True)}
        for key, value in params.items():
            record[key] = str(value)
        param_rows.append(record)
    frame = pd.DataFrame(param_rows)
    frame.to_csv(OUT / "chosen_parameters.csv", index=False)
    summary = {}
    for method, group in frame.groupby("method"):
        values = {}
        for field in [c for c in group if c.startswith("model__")]:
            counts = Counter(group[field].dropna())
            values[field] = dict(counts.most_common())
        summary[method] = {"parameter_frequencies": values,
                           "inner_macro_f1_mean": float(group.inner_macro_f1.mean()),
                           "outer_macro_f1_mean": float(group.outer_macro_f1.mean()),
                           "inner_minus_outer_mean": float(group.inner_minus_outer.mean()),
                           "inner_minus_outer_sd": float(group.inner_minus_outer.std()),
                           "boundary_choices": {}}
    (OUT / "parameter_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    for split, (repeat, fold, train, test) in enumerate(splits):
        old = scores[(scores.split == split) & (scores.method == "mlp")].iloc[0]
        params = json.loads(old.params)
        model = build_pipeline("mlp", int(cfg["seed"] + repeat * 100 + fold))
        model.set_params(**params)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ConvergenceWarning)
            model.fit(X.iloc[train], y.iloc[train])
        net = model.named_steps["model"].network_
        validation = np.asarray(net.validation_scores_, dtype=float)
        loss = np.asarray(net.loss_curve_, dtype=float)
        audit_rows.append({"split": split, "n_iter": int(net.n_iter_),
                           "max_iter": net.max_iter, "best_validation_accuracy": float(net.best_validation_score_),
                           "last_validation_accuracy": float(validation[-1]),
                           "last_training_loss": float(loss[-1]),
                           "loss_first": float(loss[0]),
                           "loss_decreased": bool(loss[-1] < loss[0]),
                           "convergence_warnings": sum(issubclass(w.category, ConvergenceWarning) for w in caught),
                           "outer_macro_f1": float(old.macro_f1)})
    diagnostics = pd.DataFrame(audit_rows)
    diagnostics.to_csv(OUT / "mlp_refit_diagnostics.csv", index=False)
    overview = {"folds": len(diagnostics),
                "iterations_median": float(diagnostics.n_iter.median()),
                "iterations_min": int(diagnostics.n_iter.min()),
                "iterations_max": int(diagnostics.n_iter.max()),
                "convergence_warning_count": int(diagnostics.convergence_warnings.sum()),
                "loss_decreased_count": int(diagnostics.loss_decreased.sum()),
                "best_validation_accuracy_mean": float(diagnostics.best_validation_accuracy.mean()),
                "last_training_loss_mean": float(diagnostics.last_training_loss.mean())}
    (OUT / "mlp_summary.json").write_text(json.dumps(overview, indent=2), encoding="utf-8")
    print(json.dumps(overview, indent=2))


if __name__ == "__main__":
    main()
