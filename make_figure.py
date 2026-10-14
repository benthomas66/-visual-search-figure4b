"""Plot search_accuracy.csv as figure4b_reproduction.png.

Run after simulate_search.py:  python make_figure.py
"""

import csv
import matplotlib.pyplot as plt


with open("search_accuracy.csv", newline="") as file:
    rows = list(csv.DictReader(file))


def get_curve(p_absent, observer):
    """Return the e2 values and accuracies for one observer and prior."""
    e2_values = []
    accuracies = []
    # Rows are already in increasing e2 order
    for row in rows:
        if float(row["p_absent"]) == p_absent and row["observer"] == observer:
            e2_values.append(float(row["true_e2"]))
            accuracies.append(float(row["accuracy"]))
    return e2_values, accuracies


figure, panels = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
left_panel = panels[0]
right_panel = panels[1]

# Left panel: p0 = 0.5
e2, accuracy = get_curve(0.5, "ideal")
left_panel.plot(e2, accuracy, label="Ideal",
                color="black", linestyle="-", marker="o")
e2, accuracy = get_curve(0.5, "flat_heuristic")
left_panel.plot(e2, accuracy, label="Flat heuristic",
                color="tab:blue", linestyle=":", marker="o")
e2, accuracy = get_curve(0.5, "falloff_heuristic")
left_panel.plot(e2, accuracy, label="Fall-off heuristic",
                color="tab:orange", linestyle="--", marker="o")
left_panel.set_title("Absent prior p0 = 0.5")
left_panel.set_ylabel("Proportion correct")

# Right panel: p0 = 0
e2, accuracy = get_curve(0.0, "ideal")
right_panel.plot(e2, accuracy, label="Ideal",
                 color="black", linestyle="-", marker="o")
e2, accuracy = get_curve(0.0, "flat_heuristic")
right_panel.plot(e2, accuracy, label="Flat heuristic",
                 color="tab:blue", linestyle=":", marker="o")
e2, accuracy = get_curve(0.0, "falloff_heuristic")
right_panel.plot(e2, accuracy, label="Fall-off heuristic",
                 color="tab:orange", linestyle="--", marker="o")
right_panel.set_title("Absent prior p0 = 0.0")
right_panel.legend()

for panel in panels:
    panel.set_xlabel("Generating e2 (degrees)")
    panel.set_xticks([1, 3, 5, 7, 9])
    panel.set_ylim(0.2, 1.0)
    panel.grid(alpha=0.2)

figure.suptitle("Figure 4b reproduction: ideal and heuristic searchers")
figure.tight_layout()
figure.savefig("figure4b_reproduction.png", dpi=300)
plt.close(figure)
print("Saved figure4b_reproduction.png")
