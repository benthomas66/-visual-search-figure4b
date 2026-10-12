"""Sanity checks and an independent likelihood check. Run with unittest."""

import contextlib
import io
import unittest

import numpy as np
import simulate_search as model


class ModelTests(unittest.TestCase):
    def test_priors_and_location_count(self):
        self.assertEqual(len(model.eccentricity), 19)
        for p_absent in [0.0, 0.5, 1.0]:
            prior = model.make_prior(p_absent)
            self.assertEqual(len(prior), 20)
            self.assertAlmostEqual(prior.sum(), 1.0)
            self.assertEqual(prior[0], p_absent)
            np.testing.assert_allclose(prior[1:], (1 - p_absent) / 19)

    def test_response_generation_and_indexing(self):
        dprime = np.arange(1.0, 20.0)
        for state in [0, 1, 3, 19]:
            noise = np.random.default_rng(12).standard_normal(19)
            expected = noise.copy()
            if state > 0:
                expected[state - 1] += dprime[state - 1]
            actual = model.generate_responses(np.random.default_rng(12), state, dprime)
            np.testing.assert_array_equal(actual, expected)

    def test_decision_matches_full_gaussian_likelihoods(self):
        # Independently evaluate all 20 joint Gaussian densities in log space.
        rng = np.random.default_rng(7)
        dprime = 6 * 3 / (model.eccentricity + 3)
        for p_absent in [0.0, 0.5]:
            prior = model.make_prior(p_absent)
            for trial in range(100):
                responses = rng.standard_normal(19)
                scores = np.full(20, -np.inf)
                for state in range(20):
                    if prior[state] == 0:
                        continue
                    means = np.zeros(19)
                    if state > 0:
                        means[state - 1] = dprime[state - 1]
                    scores[state] = np.log(prior[state]) - 0.5 * np.sum((responses - means)**2)
                self.assertEqual(model.choose_response(responses, dprime, prior),
                                 np.argmax(scores))

    def test_zero_detectability_uses_prior_and_excludes_absence(self):
        responses = np.ones(19)
        zeros = np.zeros(19)
        self.assertEqual(model.choose_response(responses, zeros, model.make_prior(0.5)), 0)
        # All target states tie; numpy selects the first, and never absent.
        self.assertEqual(model.choose_response(responses, zeros, model.make_prior(0.0)), 1)

    def test_high_detectability_recovers_every_state(self):
        rng = np.random.default_rng(3)
        dprime = np.full(19, 20.0)
        prior = model.make_prior(0.5)
        for state in range(20):
            responses = model.generate_responses(rng, state, dprime)
            self.assertEqual(model.choose_response(responses, dprime, prior), state)

    def test_source_notebook_scoring_equivalence(self):
        # Authors shift the score by assumed_dprime * generating_dprime;
        # we shift the response first. These give the same scores.
        rng = np.random.default_rng(4)
        generating = 6 * 5 / (model.eccentricity + 5)
        assumed = model.falloff_assumed_dprime
        prior = model.make_prior(0.5)
        for state in range(20):
            noise = rng.standard_normal(19)
            responses = noise.copy()
            source_scores = np.log(prior[1:]) + assumed * (noise - assumed / 2)
            if state > 0:
                responses[state - 1] += generating[state - 1]
                source_scores[state - 1] += assumed[state - 1] * generating[state - 1]
            expected = np.argmax(np.concatenate(([np.log(prior[0])], source_scores)))
            self.assertEqual(model.choose_response(responses, assumed, prior), expected)

    def test_sweep_shape_and_seed_reproducibility(self):
        with contextlib.redirect_stdout(io.StringIO()):
            first = model.run_simulation(n_trials=20, seed=8)
            second = model.run_simulation(n_trials=20, seed=8)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 30)
        keys = {(r["p_absent"], r["true_e2"], r["observer"]) for r in first}
        self.assertEqual(len(keys), 30)
        for row in first:
            self.assertEqual(row["accuracy"], row["n_correct"] / row["n_trials"])
            self.assertTrue(0 <= row["accuracy"] <= 1)


if __name__ == "__main__":
    unittest.main()
