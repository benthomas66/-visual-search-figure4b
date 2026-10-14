"""Basic checks. Run from this folder after simulate_search.py:  python test_model.py"""

import csv
import numpy as np
from simulate_search import N_LOCATIONS, choose_state, make_prior


# 1. The prior has 20 entries (absent + 19 locations) and sums to one.
for p_absent in [0.0, 0.5]:
    prior = make_prior(p_absent)
    assert len(prior) == N_LOCATIONS + 1
    assert np.isclose(prior.sum(), 1.0)


# 2. With zero detectability only the prior matters:
#    absent (0.5) beats each location (0.5 / 19).
zero_dprime = np.zeros(N_LOCATIONS)
zero_responses = np.zeros(N_LOCATIONS)
assert choose_state(zero_responses, zero_dprime, make_prior(0.5)) == 0


# 3. Indexing: a very visible target is always found, including
#    absence (0) and the last location (19).
prior = make_prior(0.5)
high_dprime = np.full(N_LOCATIONS, 20.0)
for true_state in range(N_LOCATIONS + 1):
    responses = np.zeros(N_LOCATIONS)
    if true_state > 0:
        responses[true_state - 1] = high_dprime[true_state - 1]
    assert choose_state(responses, high_dprime, prior) == true_state


# 4. Same decisions as the full Gaussian log likelihood of all 19
#    responses plus the log prior.
rng = np.random.default_rng(7)
dprime = np.linspace(1.0, 6.0, N_LOCATIONS)
for p_absent in [0.0, 0.5]:
    prior = make_prior(p_absent)
    for trial in range(100):
        responses = rng.standard_normal(N_LOCATIONS)
        full_scores = np.zeros(N_LOCATIONS + 1)
        for state in range(N_LOCATIONS + 1):
            if prior[state] == 0:
                full_scores[state] = -np.inf
                continue
            means = np.zeros(N_LOCATIONS)
            if state > 0:
                means[state - 1] = dprime[state - 1]
            full_scores[state] = (
                np.log(prior[state]) - 0.5 * np.sum((responses - means) ** 2)
            )
        assert choose_state(responses, dprime, prior) == np.argmax(full_scores)


# 5. Same decisions as the notebooks' bookkeeping: score the noise with the
#    assumed map, add assumed d' x generating d' to the target's score, and
#    divide the prior by p0.
rng = np.random.default_rng(11)
generating_dprime = np.linspace(6.0, 1.0, N_LOCATIONS)
assumed_dprime = np.full(N_LOCATIONS, 3.9)
for p_absent in [0.0, 0.5]:
    prior = make_prior(p_absent)
    if p_absent == 0:
        with np.errstate(divide="ignore"):
            log_prior_ratio = np.log(prior)
    else:
        log_prior_ratio = np.log(prior / prior[0])
    for trial in range(200):
        true_state = rng.integers(0, N_LOCATIONS + 1)
        noise = rng.standard_normal(N_LOCATIONS)

        notebook_scores = np.zeros(N_LOCATIONS + 1)
        notebook_scores[1:] = assumed_dprime * (noise - assumed_dprime / 2)
        responses = noise.copy()
        if true_state > 0:
            k = true_state - 1
            notebook_scores[true_state] += assumed_dprime[k] * generating_dprime[k]
            responses[k] += generating_dprime[k]
        notebook_decision = np.argmax(log_prior_ratio + notebook_scores)

        assert choose_state(responses, assumed_dprime, prior) == notebook_decision


# 6. The CSV has exactly one row for each of the 30 combinations.
with open("search_accuracy.csv", newline="") as file:
    rows = list(csv.DictReader(file))
assert len(rows) == 30

for p_absent in [0.0, 0.5]:
    for e2 in [1.0, 3.0, 5.0, 7.0, 9.0]:
        for observer in ["ideal", "flat_heuristic", "falloff_heuristic"]:
            n_matches = 0
            for row in rows:
                if (float(row["p_absent"]) == p_absent
                        and float(row["true_e2"]) == e2
                        and row["observer"] == observer):
                    n_matches += 1
            assert n_matches == 1

for row in rows:
    assert int(row["n_trials"]) == 10000
    assert float(row["accuracy"]) == int(row["n_correct"]) / int(row["n_trials"])

print("All basic model checks passed.")
