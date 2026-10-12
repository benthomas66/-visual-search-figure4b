"""Read search_accuracy.csv and plot the six accuracy curves.

Run from this folder: python make_figure.py
"""

import csv
import os
import matplotlib.pyplot as plt


with open("search_accuracy.csv", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

observer_names = ["ideal", "flat_heuristic", "falloff_heuristic"]
observer_labels = ["Ideal", "Flat heuristic", "Declining heuristic"]
line_styles = ["-", ":", "--"]
colors = ["black", "tab:blue", "tab:orange"]
prior_values = [0.5, 0.0]

figure, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)

for panel_index in range(2):
    p_absent = prior_values[panel_index]
    axis = axes[panel_index]

    for observer_index in range(3):
        observer_name = observer_names[observer_index]
        e2_values = []
        accuracy_values = []

        # The simulator saves each observer's points in increasing e2 order.
        for row in rows:
            if float(row["p_absent"]) == p_absent:
                if row["observer"] == observer_name:
                    e2_values.append(float(row["true_e2"]))
                    accuracy_values.append(float(row["accuracy"]))

        axis.plot(
            e2_values,
            accuracy_values,
            label=observer_labels[observer_index],
            linestyle=line_styles[observer_index],
            color=colors[observer_index],
            marker="o"
        )

    axis.set_title("Absent prior p0 = " + str(p_absent))
    axis.set_xlabel("Generating e2 (degrees)")
    axis.set_xticks([1, 3, 5, 7, 9])
    axis.set_ylim(0.2, 1.0)
    axis.grid(alpha=0.2)

axes[0].set_ylabel("Proportion correct")
axes[1].legend()
figure.suptitle("Figure 4b reproduction: ideal and heuristic observers")
figure.tight_layout()

os.makedirs("figures", exist_ok=True)
figure.savefig("figures/figure4b_reproduction.png", dpi=300)
plt.close(figure)
print("Saved figures/figure4b_reproduction.png")
