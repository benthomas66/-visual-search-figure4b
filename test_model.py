"""Basic checks. Run from this folder: python test_model.py"""

import csv
import numpy as np
from simulate_search import choose_response


# The prior has 20 entries; the physical maps have 19.
n_locations = 19
for p_absent in [0.0, 0.5]:
    p_location = (1.0 - p_absent) / n_locations
    prior = np.array([p_absent] + [p_location] * n_locations)
    assert len(prior) == 20
    assert np.isclose(prior.sum(), 1.0)


# With zero detectability, the larger absent prior wins.
prior = np.array([0.5] + [0.5 / 19] * 19)
dprime = np.zeros(19)
responses = np.zeros(19)
assert choose_response(responses, dprime, prior) == 0

# With absence excluded, a tie selects the first target location.
prior = np.array([0.0] + [1.0 / 19] * 19)
assert choose_response(responses, dprime, prior) == 1


# Strong target responses recover all 19 locations; all-noise selects absence.
prior = np.array([0.5] + [0.5 / 19] * 19)
dprime = np.array([20.0] * 19)
for true_state in range(20):
    responses = np.zeros(19)
    if true_state > 0:
        responses[true_state - 1] = dprime[true_state - 1]
    assert choose_response(responses, dprime, prior) == true_state


# Independently calculate all joint Gaussian likelihoods and compare decisions.
rng = np.random.default_rng(7)
dprime = np.linspace(1.0, 6.0, 19)
for p_absent in [0.0, 0.5]:
    prior = np.array([p_absent] + [(1.0 - p_absent) / 19] * 19)
    for trial in range(100):
        responses = rng.standard_normal(19)
        joint_scores = np.zeros(20)
        for state in range(20):
            if prior[state] == 0:
                joint_scores[state] = -np.inf
            else:
                means = np.zeros(19)
                if state > 0:
                    means[state - 1] = dprime[state - 1]
                joint_scores[state] = (
                    np.log(prior[state])
                    - 0.5 * np.sum((responses - means)**2)
                )
        expected_state = np.argmax(joint_scores)
        assert choose_response(responses, dprime, prior) == expected_state


# Check that the saved simulation has three results for every condition.
with open("search_accuracy.csv", newline="") as file:
    rows = list(csv.DictReader(file))
assert len(rows) == 30
for p_absent in [0.0, 0.5]:
    for e2 in [1.0, 3.0, 5.0, 7.0, 9.0]:
        for observer in ["ideal", "flat_heuristic", "falloff_heuristic"]:
            matching_rows = 0
            for row in rows:
                if float(row["p_absent"]) == p_absent:
                    if float(row["true_e2"]) == e2:
                        if row["observer"] == observer:
                            matching_rows = matching_rows + 1
            assert matching_rows == 1
for row in rows:
    accuracy = int(row["n_correct"]) / int(row["n_trials"])
    assert float(row["accuracy"]) == accuracy
    assert 0.0 <= accuracy <= 1.0

print("All basic model checks passed.")
