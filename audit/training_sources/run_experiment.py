"""Vienos komandos pakartojamas Vehicle siluetų klasifikavimo eksperimentas."""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
import warnings
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parent / ".matplotlib"))

import joblib
import matplotlib
if "ipykernel" not in sys.modules:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import sklearn
import yaml
from scipy import stats
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import (balanced_accuracy_score, confusion_matrix, f1_score,
                             classification_report)
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.inspection import permutation_importance

from src.data import CLASSES, load_vehicle
from src.models import build_pipeline, grid_for
from src.provenance import provenance, planned_fits, peak_rss_bytes
from threadpoolctl import threadpool_limits

warnings.filterwarnings("ignore", category=ConvergenceWarning)
METHODS = ["centroid", "knn", "svm", "mlp", "rbf"]
ABLATIONS = ["svm_linear", "svm_unscaled"]


def metrics(y_true, y_pred):
    return {"macro_f1": f1_score(y_true, y_pred, labels=CLASSES, average="macro", zero_division=0),
            "balanced_accuracy": balanced_accuracy_score(y_true, y_pred)}


def make_outer_splits(X, y, cfg):
    # Kiekvienas pakartojimas turi savo nustatytą sėklą, visiems modeliams indeksai vienodi.
    for repeat, seed in enumerate(cfg["outer_seeds"]):
        splitter = StratifiedKFold(n_splits=cfg["outer_folds"], shuffle=True, random_state=seed)
        for fold, (train, test) in enumerate(splitter.split(X, y)):
            yield repeat, fold, train, test


def fit_model(name, X_train, y_train, cfg, seed, jobs, audit_path=None):
    scaled = name != "svm_unscaled"
    base_name = "svm" if name == "svm_unscaled" else name
    pipeline = build_pipeline(base_name, seed, scaled=scaled)
    grid = grid_for(base_name, cfg)
    if grid is None:
        return pipeline.fit(X_train, y_train), {}
    inner = StratifiedKFold(n_splits=cfg["inner_folds"], shuffle=True, random_state=seed)
    # GridSearchCV mokosi tik iš išorinio mokymo skaidinio; pirminė metrika Macro-F1.
    search = GridSearchCV(pipeline, grid, scoring="f1_macro", cv=inner, n_jobs=jobs,
                          error_score="raise", refit=True)
    search.fit(X_train, y_train)
    if audit_path is not None:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(search.cv_results_).to_csv(audit_path, index=False)
    return search.best_estimator_, search.best_params_


def corrected_ci(differences, n_test, n_train):
    """Nadeau–Bengio pataisa koreliuotiems kartotinės CV skirtumams."""
    d = np.asarray(differences, dtype=float)
    if len(d) < 2:
        return [None, None]
    variance = d.var(ddof=1)
    standard_error = np.sqrt((1 / len(d) + n_test / n_train) * variance)
    radius = stats.t.ppf(0.975, len(d) - 1) * standard_error
    return [float(d.mean() - radius), float(d.mean() + radius)]


def perturbed_scores(model, X_test, y_test, train_std, cfg, split_id, name):
    out = []
    original = X_test.to_numpy(dtype=float)
    for kind, levels in [("noise", cfg["noise_sigmas"]), ("missing", cfg["missing_rates"])]:
        for level in levels:
            for realization in range(cfg["robustness_repeats"]):
                # Ta pati perturbacija taikoma kiekvienam modeliui, tik bandymo objektams.
                rng = np.random.default_rng(cfg["seed"] + split_id * 10000 + realization * 100 + int(level * 1000))
                changed = original.copy()
                if kind == "noise":
                    changed += rng.normal(0, level, changed.shape) * train_std
                else:
                    changed[rng.random(changed.shape) < level] = np.nan
                pred = model.predict(pd.DataFrame(changed, columns=X_test.columns, index=X_test.index))
                out.append({"method": name, "split": split_id, "kind": kind, "level": level,
                            "realization": realization, **metrics(y_test, pred)})
    return out


def svm_margin(model, X_test, predicted):
    # SVC OVO grąžina šešias porines funkcijas; diagnostikai naudojamas mažiausias |balas|.
    values = model.decision_function(X_test)
    classes = list(model.named_steps["model"].classes_)
    pairs = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    selected = []
    for row, label in zip(values, predicted):
        index = classes.index(label)
        selected.append(float(min(abs(row[j]) for j, (a, b) in enumerate(pairs) if index in (a, b))))
    return selected


def save_outputs(out_dir, cfg, metadata, records, predictions, robustness, importances, models):
    out_dir.mkdir(parents=True, exist_ok=True)
    folds = pd.DataFrame(records)
    preds = pd.DataFrame(predictions)
    robust = pd.DataFrame(robustness)
    perm = pd.DataFrame(importances)
    folds.to_csv(out_dir / "fold_metrics.csv", index=False)
    preds.to_csv(out_dir / "out_of_fold_predictions.csv", index=False)
    robust.to_csv(out_dir / "robustness.csv", index=False)
    perm.to_csv(out_dir / "feature_permutation.csv", index=False)
    (out_dir / "data_metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "run_config.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    environment = {"python": platform.python_version(), "numpy": np.__version__,
                   "pandas": pd.__version__, "scipy": scipy.__version__, "scikit_learn": sklearn.__version__}
    (out_dir / "environment.json").write_text(json.dumps(environment, indent=2), encoding="utf-8")

    summary = folds.groupby("method").agg(macro_f1_mean=("macro_f1", "mean"),
                                             macro_f1_sd=("macro_f1", "std"),
                                             balanced_accuracy_mean=("balanced_accuracy", "mean"),
                                             balanced_accuracy_sd=("balanced_accuracy", "std"),
                                             train_seconds_mean=("train_seconds", "mean")).sort_values("macro_f1_mean", ascending=False)
    summary.to_csv(out_dir / "results_summary.csv")
    baseline = summary.loc[["centroid", "knn"], "macro_f1_mean"].idxmax()
    pair = folds.pivot(index="split", columns="method", values="macro_f1")
    differences = pair["svm"] - pair[baseline]
    n_test = metadata["rows"] / cfg["outer_folds"]
    n_train = metadata["rows"] - n_test
    ci = corrected_ci(differences, n_test, n_train)
    repeat_diffs = folds.pivot_table(index="repeat", columns="method", values="macro_f1")["svm"] - folds.pivot_table(index="repeat", columns="method", values="macro_f1")[baseline]
    hypothesis = {"baseline": baseline, "mean_difference": float(differences.mean()),
                  "corrected_95pct_ci": ci, "positive_repeats": int((repeat_diffs > 0).sum()),
                  "confirmed": bool(differences.mean() >= 0.02 and (repeat_diffs > 0).sum() >= 3 and ci[0] > 0)}
    (out_dir / "hypothesis.json").write_text(json.dumps(hypothesis, indent=2), encoding="utf-8")

    # Pakartotinėje CV kiekvienas objektas pasirodo teste penkis kartus; matrica nėra 846 nepriklausomos prognozės.
    for name in models:
        subset = preds[preds.method == name]
        cm = confusion_matrix(subset.true, subset.predicted, labels=CLASSES)
        pd.DataFrame(cm, index=CLASSES, columns=CLASSES).to_csv(out_dir / f"confusion_{name}.csv")
        if name == "svm":
            fig, ax = plt.subplots(figsize=(6, 5))
            normalized = cm / cm.sum(axis=1, keepdims=True)
            im = ax.imshow(normalized, vmin=0, vmax=1, cmap="Blues")
            for i in range(4):
                for j in range(4):
                    ax.text(j, i, f"{normalized[i,j]:.2f}\n({cm[i,j]})", ha="center", va="center")
            ax.set(xticks=range(4), yticks=range(4), xticklabels=CLASSES, yticklabels=CLASSES,
                   xlabel="Prognozuota", ylabel="Tikroji klasė", title="SVM painiavos matrica (5 kartotiniai bandymai)")
            fig.colorbar(im, ax=ax)
            fig.tight_layout()
            fig.savefig(out_dir / "confusion_svm.png", dpi=180)
            plt.close(fig)
            report = classification_report(subset.true, subset.predicted, labels=CLASSES, output_dict=True, zero_division=0)
            (out_dir / "class_report_svm.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    fig, ax = plt.subplots(figsize=(9, 5))
    order = [v for v in METHODS + ABLATIONS if v in models]
    ax.boxplot([folds.loc[folds.method == name, "macro_f1"] for name in order], tick_labels=order)
    ax.set(ylabel="Macro-F1", title="Vienodi išoriniai skaidiniai visiems metodams")
    ax.grid(axis="y", alpha=.3)
    fig.tight_layout()
    fig.savefig(out_dir / "macro_f1_boxplot.png", dpi=180)
    plt.close(fig)

    if not robust.empty:
        robust.groupby(["method", "kind", "level"])[["macro_f1", "balanced_accuracy"]].agg(["mean", "std"]).to_csv(out_dir / "robustness_summary.csv")
    if not perm.empty:
        perm.groupby("feature").drop_mean.mean().sort_values(ascending=False).to_csv(out_dir / "feature_importance_summary.csv")
    errors = preds[(preds.method == "svm") & (preds.true != preds.predicted)]
    errors.sort_values("margin", ascending=False).drop_duplicates("row_index").head(10).to_csv(out_dir / "high_margin_errors.csv", index=False)
    correct = preds[(preds.method == "svm") & (preds.true == preds.predicted)]
    correct.sort_values("margin").drop_duplicates("row_index").head(10).to_csv(out_dir / "low_margin_correct.csv", index=False)
    return summary, hypothesis


def postprocess(out_dir, cache_dir):
    """Vienos komandos darbo eiga baigiama nepriklausoma patikra ir ataskaita."""
    project = Path(__file__).resolve().parent
    for script in ["verify_results.py", "build_report.py"]:
        subprocess.run([sys.executable, str(project / script), "--results", str(out_dir.resolve()),
                        "--cache", str(cache_dir.resolve())], cwd=project, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/main.yaml")
    parser.add_argument("--out", default="results/main")
    parser.add_argument("--cache", default="data")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--quick", action="store_true", help="Tik techninis dviejų išorinių skaidinių patikrinimas; ne galutiniai rezultatai")
    parser.add_argument("--postprocess-only", action="store_true", help="Patikrinti išsaugotus rezultatus ir atnaujinti ataskaitą be mokymo")
    args = parser.parse_args()
    if args.postprocess_only:
        postprocess(Path(args.out), Path(args.cache))
        return
    started_run = time.perf_counter()
    if args.jobs != 1:
        raise ValueError("Audituojamam atminties biudžetui naudokite --jobs 1")
    threadpool_limits(limits=4)
    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    if planned_fits(cfg) > 20000:
        raise ValueError("Planuojamas eksperimentas viršija 20 000 pritaikymų")
    X, y, metadata = load_vehicle(Path(args.cache))
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_identity = provenance(Path(__file__).resolve().parent)
    (out_dir / "provenance.json").write_text(json.dumps(run_identity, indent=2), encoding="utf-8")
    records, predictions, robustness, importances = [], [], [], []
    missing_features, edge_records = [], []
    splits = list(make_outer_splits(X, y, cfg))
    if args.quick:
        splits = splits[:2]
    models = METHODS + ABLATIONS
    for split_id, (repeat, fold, train, test) in enumerate(splits):
        X_train, X_test = X.iloc[train], X.iloc[test]
        y_train, y_test = y.iloc[train], y.iloc[test]
        train_std = X_train.std(ddof=0).to_numpy()
        seed = cfg["seed"] + repeat * 100 + fold
        print(f"Split {split_id+1}/{len(splits)} (repeat={repeat}, fold={fold})", flush=True)
        for name in models:
            started = time.perf_counter()
            model, params = fit_model(name, X_train, y_train, cfg, seed, args.jobs, out_dir / "inner_search" / f"{split_id:02d}_{name}.csv")
            train_seconds = time.perf_counter() - started
            predict_started = time.perf_counter()
            pred = model.predict(X_test)
            predict_seconds = time.perf_counter() - predict_started
            score = metrics(y_test, pred)
            records.append({"split": split_id, "repeat": repeat, "fold": fold, "method": name,
                            **score, "train_seconds": train_seconds, "predict_seconds": predict_seconds, "test_rows": len(test), "params": json.dumps(params)})
            margins = svm_margin(model, X_test, pred) if name == "svm" else [np.nan] * len(test)
            predictions.extend({"split": split_id, "repeat": repeat, "fold": fold, "method": name,
                                "row_index": int(row), "true": truth, "predicted": guess, "margin": margin}
                               for row, truth, guess, margin in zip(test, y_test, pred, margins))
            if name in METHODS:
                robustness.extend(perturbed_scores(model, X_test, y_test, train_std, cfg, split_id, name))
            if name == "svm":
                # Kiekvieno požymio visiškas nebuvimas yra atskira diagnostika.
                for feature in X.columns:
                    changed = X_test.copy()
                    changed[feature] = np.nan
                    altered = metrics(y_test, model.predict(changed))
                    missing_features.append({"split": split_id, "feature": feature,
                        **altered, "f1_drop": score["macro_f1"] - altered["macro_f1"]})
                lower, upper = X_train.quantile(.05), X_train.quantile(.95)
                edge_counts = ((X_test < lower) | (X_test > upper)).sum(axis=1)
                edge_records.extend({"split": split_id, "repeat": repeat, "row_index": int(i),
                    "edge_features": int(n), "error": bool(t != g)}
                    for i, n, t, g in zip(test, edge_counts, y_test, pred))
                # Permutacija liečia tik bandymo dalį ir nepakeičia parinkto modelio.
                result = permutation_importance(model, X_test, y_test, scoring="f1_macro", n_repeats=3,
                                                random_state=seed, n_jobs=1)
                importances.extend({"split": split_id, "feature": feature, "drop_mean": float(value)}
                                   for feature, value in zip(X.columns, result.importances_mean))
            print(f"  {name}: F1={score['macro_f1']:.3f}, BA={score['balanced_accuracy']:.3f}, fit={train_seconds:.1f}s", flush=True)
        pd.DataFrame(missing_features).to_csv(out_dir / "missing_feature_sensitivity.csv", index=False)
        pd.DataFrame(edge_records).to_csv(out_dir / "error_edges.csv", index=False)
        # Išsaugoma po kiekvieno skaidinio, kad ilgą bandymą būtų galima audituoti.
        summary, hypothesis = save_outputs(out_dir, cfg, metadata, records, predictions, robustness, importances, models)
    print(summary.to_string())
    print("Hipoteze:", json.dumps(hypothesis, ensure_ascii=True))
    if not args.quick:
        # Diegiamas modelis išmokomas iš viso rinkinio, parinkus parametrus vidine CV.
        final, params = fit_model("svm", X, y, cfg, cfg["seed"], args.jobs, out_dir / "inner_search" / "final_svm.csv")
        joblib.dump({"pipeline": final, "feature_names": list(X.columns), "labels": CLASSES,
                     "openml_md5": metadata["md5"], "params": params,
                     "model_version": run_identity["code_sha256"][:16] + "-" + run_identity["created_utc"],
                     "code_sha256": run_identity["code_sha256"]}, out_dir / "final_svm.joblib")
        resources = {"model_fits": planned_fits(cfg), "wall_seconds_before_reporting": time.perf_counter() - started_run,
                     "peak_process_rss_bytes": peak_rss_bytes(), "jobs": 1, "native_thread_limit": 4,
                     "scope": "Main process: training, predictions, diagnostics and figure generation; reporting subprocess excluded"}
        resources["within_fit_budget"] = resources["model_fits"] <= 20000
        resources["within_time_budget"] = resources["wall_seconds_before_reporting"] <= 3600
        resources["within_memory_budget"] = resources["peak_process_rss_bytes"] <= 2_000_000_000
        (out_dir / "resources.json").write_text(json.dumps(resources, indent=2), encoding="utf-8")
        postprocess(out_dir, Path(args.cache))


if __name__ == "__main__":
    main()
