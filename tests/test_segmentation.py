"""
Unit and Integration Tests for Local Fractal Dimension Texture Segmentation.
"""

import unittest
import numpy as np

from core.local_fractal import compute_differential_box_counting_patch, compute_local_fractal_map
from core.segmentation import otsu_threshold, kmeans_segmentation
from core.evaluation import compute_segmentation_metrics


class TestTextureSegmentation(unittest.TestCase):

    def test_patch_dbc(self):
        # Flat patch
        flat = np.full((16, 16), 128, dtype=np.float32)
        df_flat = compute_differential_box_counting_patch(flat)
        self.assertAlmostEqual(df_flat, 2.0, places=1)

        # Rough noise patch
        noise = np.random.uniform(0, 255, (16, 16)).astype(np.float32)
        df_noise = compute_differential_box_counting_patch(noise)
        self.assertGreater(df_noise, 2.0)

    def test_local_map_and_segmentation(self):
        img = np.zeros((32, 32), dtype=np.uint8)
        # Left side smooth, right side rough
        img[:, 16:] = np.random.uniform(0, 255, (32, 16)).astype(np.uint8)

        lfd = compute_local_fractal_map(img, window_size=9, stride=2)
        self.assertEqual(lfd.shape, (32, 32))

        # Otsu segmentation
        mask, thresh = otsu_threshold(lfd)
        self.assertEqual(mask.shape, (32, 32))

        gt = np.zeros((32, 32), dtype=np.uint8)
        gt[:, 16:] = 1
        metrics = compute_segmentation_metrics(mask, gt)
        self.assertGreater(metrics["iou"], 0.70)
        self.assertGreater(metrics["dice"], 0.80)


if __name__ == "__main__":
    unittest.main()
