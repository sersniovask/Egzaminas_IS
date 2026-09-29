"""Plot the saved outer-test results without retraining or changing them."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "further_20260928"
ASSETS = ROOT / "report_assets"
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "Arial", "font.size": 9, "savefig.dpi": 180})


def paired_differences() -> None:
    specs = [
        ("svm_extended", "Dar platesnis SVM", "#cb7641"),
        ("extra_trees", "ExtraTrees", "#a44e4e"),
        ("tabpfn_v2", "TabPFN v2", "#2a7568"),
    ]
    fig, ax = plt.subplots(figsize=(8.3, 3.25), layout="constrained")
    rng = np.random.default_rng(20260929)
    for y, (key, label, color) in enumerate(specs):
        frame = pd.read_csv(RESULTS / key / "paired_fold_metrics.csv")
        wide = frame.pivot(index="split", columns="model", values="macro_f1")
        if len(wide) != 50 or not {key, "wide_svm"}.issubset(wide.columns):
            raise ValueError(f"Incomplete paired tests for {key}")
        delta = (wide[key] - wide["wide_svm"]).to_numpy()
        ax.scatter(delta, y + rng.uniform(-0.13, 0.13, len(delta)),
                   s=15, alpha=0.4, color=color, edgecolors="none")
        ax.scatter([delta.mean()], [y], marker="D", s=65, color=color,
                   edgecolors="white", linewidth=0.8, zorder=4)
        ax.text(delta.mean() + 0.004, y - 0.23, f"vid. {delta.mean():+.3f}",
                color=color, fontsize=8, weight="bold")
    ax.axvline(0, color="#263746", linewidth=1)
    ax.set_yticks(range(3), [x[1] for x in specs])
    ax.set_ylim(2.55, -0.55)
    ax.set_xlim(-0.23, 0.18)
    ax.set_xlabel("Macro-F1 skirtumas nuo ankstesnio platesnio SVM tame pačiame išoriniame teste")
    ax.grid(axis="x", color="#d9e1e8", linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    fig.savefig(ASSETS / "further_paired_differences.png", bbox_inches="tight")
    plt.close(fig)


def confusion_comparison() -> None:
    files = [
        ("wide_svm", "Ankstesnis platesnis SVM"),
        ("tabpfn_v2", "TabPFN v2"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(8.3, 3.9), layout="constrained")
    for ax, (key, title) in zip(axes, files):
        frame = pd.read_csv(RESULTS / "tabpfn_v2" / f"confusion_{key}.csv", index_col=0)
        frame = frame.loc[["bus", "opel", "saab", "van"], ["bus", "opel", "saab", "van"]]
        counts = frame.to_numpy(dtype=int)
        if counts.sum() != 4230:
            raise ValueError(f"Unexpected confusion total for {key}")
        pct = counts / counts.sum(axis=1, keepdims=True) * 100
        ax.imshow(pct, cmap="Blues", vmin=0, vmax=100)
        ax.set_title(title, fontsize=10, weight="bold")
        ax.set_xticks(range(4), frame.columns)
        ax.set_yticks(range(4), frame.index)
        ax.set_xlabel("Prognozė")
        ax.set_ylabel("Tikroji klasė")
        for row in range(4):
            for col in range(4):
                ax.text(col, row, f"{counts[row, col]}\n({pct[row, col]:.1f} %)",
                        ha="center", va="center", fontsize=7.5,
                        color="white" if pct[row, col] > 65 else "#23313e")
        for row, col in [(1, 2), (2, 1)]:
            ax.add_patch(Rectangle((col - 0.5, row - 0.5), 1, 1, fill=False,
                                   edgecolor="#cf644d", linewidth=2.2))
    fig.savefig(ASSETS / "further_confusion_comparison.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    paired_differences()
    confusion_comparison()
    print(ASSETS / "further_paired_differences.png")
    print(ASSETS / "further_confusion_comparison.png")
