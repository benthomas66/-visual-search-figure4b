"""Simulate the Figure 4b ideal and heuristic observer comparison.

Run from this folder: python simulate_search.py
Source: Zhang & Geisler (2025), doi:10.1167/jov.25.4.5.
Original code: https://github.com/anqi-j/supraoptimal-covert-search
"""

import csv
import numpy as np


# One center location and three groups of six locations.
n_locations = 19
eccentricity = np.array(
    [0.0]
    + [4.0] * 6
    + [6.9295] * 6
    + [8.0] * 6
)


def choose_response(responses, assumed_dprime, prior):
    """Score all states and return 0 for absent, or 1 through 19 for a location."""

    prior_term = np.log(prior[1:])
    evidence_term = assumed_dprime * responses
    penalty_term = 0.5 * assumed_dprime**2
    location_scores = prior_term + evidence_term - penalty_term

    if prior[0] == 0:
        absent_score = -np.inf
    else:
        absent_score = np.log(prior[0])

    # Index 0 is absence; indices 1 through 19 are target hypotheses.
    scores = np.concatenate(([absent_score], location_scores))
    response_state = np.argmax(scores)
    return response_state


def run_simulation(n_trials=10000, seed=0):
    """Run the ten conditions and return three accuracy rows per condition."""

    # Initialize once, outside every trial loop.
    rng = np.random.default_rng(seed)

    d_max = 6.0
    absent_probabilities = [0.0, 0.5]
    generating_e2_values = [1.0, 3.0, 5.0, 7.0, 9.0]

    # These assumed maps stay fixed throughout the sweep.
    flat_assumed_dprime = np.array([3.9] * n_locations)
    declining_assumed_dprime = 6.9 * 7.0 / (eccentricity + 7.0)

    results = []

    for p_absent in absent_probabilities:
        p_location = (1.0 - p_absent) / n_locations
        prior = np.array([p_absent] + [p_location] * n_locations)

        for e2 in generating_e2_values:
            # This map generates the sensory responses in this condition.
            generating_dprime = d_max * e2 / (eccentricity + e2)

            n_correct_ideal = 0
            n_correct_flat = 0
            n_correct_declining = 0

            for trial in range(n_trials):
                true_state = rng.choice(np.arange(20), p=prior)
                responses = rng.standard_normal(n_locations)

                if true_state > 0:
                    # State 3 corresponds to physical array index 2, etc.
                    responses[true_state - 1] = (
                        responses[true_state - 1]
                        + generating_dprime[true_state - 1]
                    )

                # All three observers receive these same responses.
                ideal_response = choose_response(
                    responses, generating_dprime, prior
                )
                flat_response = choose_response(
                    responses, flat_assumed_dprime, prior
                )
                declining_response = choose_response(
                    responses, declining_assumed_dprime, prior
                )

                if ideal_response == true_state:
                    n_correct_ideal = n_correct_ideal + 1
                if flat_response == true_state:
                    n_correct_flat = n_correct_flat + 1
                if declining_response == true_state:
                    n_correct_declining = n_correct_declining + 1

            ideal_accuracy = n_correct_ideal / n_trials
            flat_accuracy = n_correct_flat / n_trials
            declining_accuracy = n_correct_declining / n_trials

            # Each row contains one accuracy estimate, not a whole curve.
            results.append([
                p_absent, d_max, e2, "ideal",
                n_trials, n_correct_ideal, ideal_accuracy
            ])
            results.append([
                p_absent, d_max, e2, "flat_heuristic",
                n_trials, n_correct_flat, flat_accuracy
            ])
            results.append([
                p_absent, d_max, e2, "falloff_heuristic",
                n_trials, n_correct_declining, declining_accuracy
            ])

            print("p_absent:", p_absent, "e2:", e2)
            print("Ideal:", ideal_accuracy)
            print("Flat heuristic:", flat_accuracy)
            print("Declining heuristic:", declining_accuracy)

    return results


# Run this section when opening the script directly.
# Importing choose_response in test_model.py does not run the simulation.
if __name__ == "__main__":
    results = run_simulation()

    with open("search_accuracy.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "p_absent", "true_d_max", "true_e2", "observer",
            "n_trials", "n_correct", "accuracy"
        ])
        writer.writerows(results)

    print("Saved search_accuracy.csv")
