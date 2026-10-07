import math
import unittest

from experiments.cross_domain_experiments import (
    run_noise_sweep,
    run_temporal_autocorrelation,
)


class CrossDomainExperimentTests(unittest.TestCase):
    def test_noise_sweep_uses_increasing_one_sided_bias_probabilities(self):
        shots = 50_000
        rows = run_noise_sweep(shots=shots)["rows"]
        levels = [row["noise_level"] for row in rows]
        probabilities = [row["expected_zero_probability"] for row in rows]

        self.assertEqual(levels, [0.0, 0.01, 0.03, 0.05, 0.10])
        self.assertEqual(probabilities, [0.5 + level * 0.5 for level in levels])
        self.assertTrue(all(a < b for a, b in zip(probabilities, probabilities[1:])))

        for row in rows:
            expected = shots * row["expected_zero_probability"]
            standard_deviation = math.sqrt(
                shots
                * row["expected_zero_probability"]
                * (1 - row["expected_zero_probability"])
            )
            self.assertLess(abs(row["observed_zeros"] - expected), 5 * standard_deviation)

    def test_autocorrelation_standard_error_accounts_for_repeats(self):
        result = run_temporal_autocorrelation(sequence_length=40, repeats=15)
        expected = round(1 / math.sqrt(40 * 15), 6)
        self.assertEqual(result["standard_error"], expected)

    def test_invalid_sweep_size_is_rejected(self):
        with self.assertRaises(ValueError):
            run_noise_sweep(shots=0)

    def test_invalid_autocorrelation_dimensions_are_rejected(self):
        with self.assertRaises(ValueError):
            run_temporal_autocorrelation(sequence_length=1)
        with self.assertRaises(ValueError):
            run_temporal_autocorrelation(repeats=0)


if __name__ == "__main__":
    unittest.main()
