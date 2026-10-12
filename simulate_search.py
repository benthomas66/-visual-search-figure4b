"""Reproduce a focused ideal-versus-heuristic covert-search simulation.

Based on the model and parameter scan in Zhang & Geisler (2025),
"Optimal visual search with highly heuristic decision rules."
Original repository: https://github.com/anqi-j/supraoptimal-covert-search

A readable implementation of the published rule; see THIRD_PARTY_NOTICES.md.
Run: python simulate_search.py
Output: results/search_accuracy.csv
"""

import csv
from pathlib import Path

import numpy as np


# ------------------------------------------------------------
# 1. FIXED MODEL SETTINGS
# ------------------------------------------------------------

n_locations = 19
n_trials = 10000
random_seed = 0

d_max = 6.0

# There is one location at 0 degrees, six at 4 degrees,
# six at about 6.93 degrees, and six at 8 degrees.
eccentricity = np.array(
    [0.0]
    + [4.0] * 6
    + [6.9295] * 6
    + [8.0] * 6
)

# Each item in a sweep is a separate simulated condition.
absent_probabilities = [0.0, 0.5]
true_e2_values = [1.0, 3.0, 5.0, 7.0, 9.0]

# The two heuristic observers use FIXED assumed maps.
flat_assumed_dprime = np.array([3.9] * n_locations)

falloff_assumed_dprime = (
    6.9 * 7.0 / (eccentricity + 7.0)
)



# ------------------------------------------------------------
# 2. SCORING ONE SET OF SENSORY RESPONSES
# ------------------------------------------------------------

def choose_response(responses, assumed_dprime, prior):
    """Return the highest-scoring state: 0 = absent, 1..19 = location."""

    # The observer evaluates all 19 target-location hypotheses.
    # log(0) = -infinity excludes a zero-prior hypothesis.
    with np.errstate(divide="ignore"):
        prior_term = np.log(prior[1:])
    evidence_term = assumed_dprime * responses
    penalty_term = 0.5 * assumed_dprime**2

    location_scores = prior_term + evidence_term - penalty_term

    # The absent hypothesis is evaluated separately.
    # When its prior is zero, it must never be selected.
    if prior[0] == 0:
        absent_score = -np.inf
    else:
        absent_score = np.log(prior[0])

    # Array index now matches the state label (0..19).
    scores = np.concatenate(([absent_score], location_scores))
    response_state = np.argmax(scores)

    return response_state


# ------------------------------------------------------------
# 3. RUN THE SIMULATION FOR EACH CONDITION
# ------------------------------------------------------------

def make_prior(p_absent):
    """State 0 is absent; states 1..19 share the remaining probability."""
    if not 0.0 <= p_absent <= 1.0:
        raise ValueError("p_absent must be between zero and one")
    p_location = (1.0 - p_absent) / n_locations
    prior = np.array([p_absent] + [p_location] * n_locations)
    assert np.isclose(prior.sum(), 1.0)
    return prior


def generate_responses(rng, true_state, true_dprime):
    """Generate evidence; only the simulator knows the true state."""
    responses = rng.standard_normal(n_locations)
    if true_state > 0:
        # State labels 1..19 correspond to physical array indices 0..18.
        responses[true_state - 1] += true_dprime[true_state - 1]
    return responses


def run_simulation(n_trials=n_trials, seed=random_seed):
    """Return 30 result rows; all observers share each trial's evidence."""
    if n_trials <= 0:
        raise ValueError("n_trials must be positive")
    # One seeded generator for the entire sweep, outside every trial loop.
    rng = np.random.default_rng(seed)
    results = []

    for p_absent in absent_probabilities:
        prior = make_prior(p_absent)

        for e2 in true_e2_values:
            # The true map is fixed throughout this condition.
            true_dprime = d_max * e2 / (eccentricity + e2)

            # Each observer is tested on the SAME sensory responses.
            observer_maps = {
                "ideal": true_dprime,
                "flat_heuristic": flat_assumed_dprime,
                "falloff_heuristic": falloff_assumed_dprime,
            }

            n_correct = {
                "ideal": 0,
                "flat_heuristic": 0,
                "falloff_heuristic": 0,
            }

            for trial in range(n_trials):
                # First, the simulator chooses the true state.
                true_state = rng.choice(
                    np.arange(n_locations + 1),
                    p=prior
                )

                # Draw independent N(0,1) noise at all 19 locations.
                responses = generate_responses(rng, true_state, true_dprime)

                # Each observer interprets the SAME responses using
                # its own assumed visibility map.
                for observer_name in observer_maps:
                    assumed_dprime = observer_maps[observer_name]
                    response_state = choose_response(
                        responses, assumed_dprime, prior
                    )

                    if response_state == true_state:
                        n_correct[observer_name] += 1

            # Record the accuracy for each observer in this condition.
            for observer_name in observer_maps:
                accuracy = n_correct[observer_name] / n_trials

                results.append({
                    "p_absent": p_absent,
                    "true_d_max": d_max,
                    "true_e2": e2,
                    "observer": observer_name,
                    "n_trials": n_trials,
                    "n_correct": n_correct[observer_name],
                    "accuracy": accuracy,
                })

                print(
                    "p_absent =", p_absent,
                    "| true_e2 =", e2,
                    "| observer =", observer_name,
                    "| accuracy =", round(accuracy, 4)
                )


    return results


# ------------------------------------------------------------
# 4. SAVE RESULTS FOR THE FIGURE SCRIPT
# ------------------------------------------------------------

def save_results(results):
    output_folder = Path(__file__).resolve().parent / "results"
    output_folder.mkdir(exist_ok=True)
    output_file = output_folder / "search_accuracy.csv"

    with open(output_file, "w", newline="") as file:
        columns = [
            "p_absent", "true_d_max", "true_e2", "observer",
            "n_trials", "n_correct", "accuracy"
        ]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

    print("\nSaved results to:", output_file)


if __name__ == "__main__":
    results = run_simulation()
    save_results(results)
