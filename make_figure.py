"""Plot the 30 simulated accuracies as six curves in two prior panels."""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    root = Path(__file__).resolve().parent
    with open(root / "results" / "search_accuracy.csv", newline="") as file:
        rows = list(csv.DictReader(file))

    observers = ["ideal", "flat_heuristic", "falloff_heuristic"]
    labels = ["Ideal", "Flat heuristic", "Declining heuristic"]
    styles = ["-", ":", "--"]
    colors = ["#222222", "#0072B2", "#D55E00"]

    expected = {(p, e, o) for p in [0.0, 0.5]
                for e in [1.0, 3.0, 5.0, 7.0, 9.0] for o in observers}
    actual = {(float(r["p_absent"]), float(r["true_e2"]), r["observer"])
              for r in rows}
    if len(rows) != 30 or actual != expected:
        raise ValueError("Expected exactly one accuracy for each of 30 combinations")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    for ax, p_absent in zip(axes, [0.5, 0.0]):
        for observer, label, style, color in zip(observers, labels, styles, colors):
            selected = [r for r in rows
                        if float(r["p_absent"]) == p_absent
                        and r["observer"] == observer]
            selected.sort(key=lambda r: float(r["true_e2"]))
            x = [float(r["true_e2"]) for r in selected]
            y = [float(r["accuracy"]) for r in selected]
            ax.plot(x, y, linestyle=style, color=color, marker="o",
                    markersize=4, linewidth=2, label=label)
        ax.set_title(rf"Absent prior $p_0={p_absent:g}$")
        ax.set_xlabel(r"Generating-map $e_2$ (degrees)")
        ax.set_xticks([1, 3, 5, 7, 9])
        ax.set_ylim(0.2, 1.0)
        ax.grid(alpha=0.2)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Proportion correct")
    axes[1].legend(loc="lower right", frameon=False)
    fig.suptitle("Figure 4b reproduction: ideal and fixed heuristic observers")
    fig.text(0.5, 0.025, "19 locations · central d′ = 6 · 10,000 trials per condition · seed 0",
             ha="center", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    destination = root / "figures"
    destination.mkdir(exist_ok=True)
    output = destination / "figure4b_reproduction.png"
    fig.savefig(output, dpi=300)
    plt.close(fig)
    print("Saved figure to:", output)


if __name__ == "__main__":
    main()
