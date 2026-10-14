"""Simulate the ideal and heuristic searchers in Figure 4b of
Zhang & Geisler (2025), doi:10.1167/jov.25.4.5.
Original code: https://github.com/anqi-j/supraoptimal-covert-search

Run from this folder:  python simulate_search.py
"""

import csv
import numpy as np


N_LOCATIONS = 19
N_TRIALS = 10000
SEED = 0

# Eccentricity (deg) of each location. 6.9295 is the notebooks' value;
# the exact grid value is 6.9282.
ECCENTRICITY = np.array([0.0] + [4.0] * 6 + [6.9295] * 6 + [8.0] * 6)

ABSENT_PRIORS = [0.0, 0.5]
GENERATING_D_MAX = 6.0
GENERATING_E2_VALUES = [1.0, 3.0, 5.0, 7.0, 9.0]

# Heuristic maps, the same in every condition
FLAT_D = 3.9
FALLOFF_D_MAX = 6.9
FALLOFF_E2 = 7.0


def visibility_map(d_max, e2):
    """Equation 6 of the paper: d'(e) = d_max * e2 / (e + e2)."""
    return d_max * e2 / (ECCENTRICITY + e2)


def make_prior(p_absent):
    """Return 20 probabilities: index 0 is absent, 1-19 are the locations."""
    p_location = (1.0 - p_absent) / N_LOCATIONS
    return np.array([p_absent] + [p_location] * N_LOCATIONS)


def choose_state(responses, assumed_dprime, prior):
    """Return 0 for absent or 1-19 for a location (Equation 1)."""
    location_scores = (
        np.log(prior[1:])
        + assumed_dprime * responses
        - 0.5 * assumed_dprime**2
    )

    if prior[0] == 0:
        absent_score = -np.inf  # Exclude absence
    else:
        absent_score = np.log(prior[0])

    # scores[k] is location k, whose response is responses[k - 1]
    scores = np.concatenate(([absent_score], location_scores))
    return np.argmax(scores)


def run_condition(rng, prior, generating_dprime, flat_dprime, falloff_dprime):
    """Run one condition and return the number correct for each observer."""
    n_correct_ideal = 0
    n_correct_flat = 0
    n_correct_falloff = 0

    for trial in range(N_TRIALS):
        true_state = rng.choice(N_LOCATIONS + 1, p=prior)

        # Draw sensory noise; the target adds d' at its location
        responses = rng.standard_normal(N_LOCATIONS)
        if true_state > 0:
            responses[true_state - 1] += generating_dprime[true_state - 1]

        # All observers judge the same responses
        ideal_decision = choose_state(responses, generating_dprime, prior)
        flat_decision = choose_state(responses, flat_dprime, prior)
        falloff_decision = choose_state(responses, falloff_dprime, prior)

        if ideal_decision == true_state:
            n_correct_ideal += 1
        if flat_decision == true_state:
            n_correct_flat += 1
        if falloff_decision == true_state:
            n_correct_falloff += 1

    return n_correct_ideal, n_correct_flat, n_correct_falloff


def run_simulation():
    """Run all 10 conditions and return 30 result rows (3 per condition)."""
    rng = np.random.default_rng(SEED)

    flat_dprime = np.full(N_LOCATIONS, FLAT_D)
    falloff_dprime = visibility_map(FALLOFF_D_MAX, FALLOFF_E2)
    observer_names = ["ideal", "flat_heuristic", "falloff_heuristic"]

    results = []
    for p_absent in ABSENT_PRIORS:
        prior = make_prior(p_absent)

        for e2 in GENERATING_E2_VALUES:
            generating_dprime = visibility_map(GENERATING_D_MAX, e2)
            n_correct = run_condition(
                rng, prior, generating_dprime, flat_dprime, falloff_dprime
            )

            for observer, correct in zip(observer_names, n_correct):
                accuracy = correct / N_TRIALS
                results.append([
                    p_absent, GENERATING_D_MAX, e2, observer,
                    N_TRIALS, correct, accuracy,
                ])
                print(f"p_absent={p_absent}  e2={e2}  {observer}: {accuracy}")

    return results


if __name__ == "__main__":
    results = run_simulation()

    with open("search_accuracy.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "p_absent", "true_d_max", "true_e2", "observer",
            "n_trials", "n_correct", "accuracy",
        ])
        writer.writerows(results)

    print("Saved search_accuracy.csv")
