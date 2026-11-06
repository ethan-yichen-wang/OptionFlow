"""Synthetic checks only; no empirical targets or models are loaded."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import numpy as np
import pandas as pd
from optionflow.estimation import fit, holm
from optionflow.scoring import circular_blocks, prepare_cells, r2_os, statistics

class CoreTests(unittest.TestCase):
    def test_holm_known_values(self):
        np.testing.assert_allclose(holm([.001, .01, .04, .2]), [.004, .03, .08, .2])

    def test_fixed_effects_against_explicit_dummies(self):
        rng = np.random.default_rng(719)
        products, dates = 8, 30
        i = np.repeat(np.arange(products), dates)
        t = np.tile(np.arange(dates), products)
        x = rng.normal(size=len(i))
        y = .4*x + rng.normal(size=products)[i] + rng.normal(size=dates)[t] + .1*rng.normal(size=len(i))
        frame = pd.DataFrame({'commodity': i.astype(str), 'outcome_date': t, 'x': x, 'y': y})
        actual = fit(frame, ['x'])['beta'][0]
        matrix = np.column_stack([np.ones(len(i)), x, pd.get_dummies(i).to_numpy()[:, 1:], pd.get_dummies(t).to_numpy()[:, 1:]])
        expected = np.linalg.lstsq(matrix, y, rcond=None)[0][1]
        self.assertAlmostEqual(actual, expected, places=11)

    def test_separate_universe_centering(self):
        frame = pd.DataFrame({'commodity': list('abcd')*2, 'outcome_date': np.repeat([1, 2], 4),
                              'y': [1., 3., 9., 15., 2., 4., 10., 16.],
                              'U_all': True, 'U_120': [True, True, False, False]*2})
        for name in ['p_O0', 'p_OC', 'p_OG', 'p_B_FE', 'p_C', 'p_G', 'p_training_mean']:
            frame[name] = np.arange(8, dtype=float)
        cells, means, dates = prepare_cells(frame)
        np.testing.assert_allclose(cells['relative', 'U_120'].target_value, [-1., 1., -1., 1.])
        np.testing.assert_allclose(cells['relative', 'U_all'].groupby('outcome_date').target_value.mean(), 0)
        self.assertEqual(len(dates), 2)

    def test_loss_known_answer(self):
        frame = pd.DataFrame({'target_value': [1., -1.], 'pred_C': [0., 0.],
                              'pred_baseline': [1., 1.], 'commodity': ['a', 'b'], 'outcome_date': [1, 1]})
        result, _ = statistics(frame)
        self.assertEqual(result['model_MSE'], 1.)
        self.assertEqual(result['baseline_MSE'], 2.)
        self.assertEqual(result['Delta_MSE'], 1.)
        self.assertEqual(result['R2_OS'], .5)
        self.assertTrue(np.isnan(r2_os(1., 0.)))

    def test_circular_block_indices(self):
        starts, indices = circular_blocks(7, 3, 20, 42)
        a, b = circular_blocks(7, 3, 20, 42)
        np.testing.assert_array_equal(starts, a)
        np.testing.assert_array_equal(indices, b)
        np.testing.assert_array_equal(indices[:, :3], (starts[:, :1] + np.arange(3)) % 7)
        self.assertEqual(indices.shape, (20, 7))

if __name__ == '__main__':
    unittest.main()
