"""
Texture Segmentation Engine based on Fractal Feature Distributions.
Applies Otsu Thresholding and K-Means Clustering on Local Fractal Dimension maps.
"""

from typing import Tuple
import numpy as np


def otsu_threshold(feature_map: np.ndarray) -> Tuple[np.ndarray, float]:
    """
    Computes optimal Otsu threshold on continuous feature values.
    Returns binary segmentation mask (0 and 1) and optimal threshold.
    """
    # Normalize to [0, 255]
    f_min = float(np.min(feature_map))
    f_max = float(np.max(feature_map))
    if f_max - f_min < 1e-5:
        return np.zeros_like(feature_map, dtype=np.uint8), f_min

    norm = ((feature_map - f_min) / (f_max - f_min) * 255.0).astype(np.uint8)
    hist, _ = np.histogram(norm, bins=256, range=(0, 256))
    total = feature_map.size

    current_max = 0.0
    best_thresh_norm = 128
    weight_bg = 0
    sum_bg = 0
    sum_total = np.sum(np.arange(256) * hist)

    for t in range(256):
        weight_bg += hist[t]
        if weight_bg == 0:
            continue
        weight_fg = total - weight_bg
        if weight_fg == 0:
            break

        sum_bg += t * hist[t]
        mean_bg = sum_bg / weight_bg
        mean_fg = (sum_total - sum_bg) / weight_fg

        var_between = weight_bg * weight_fg * ((mean_bg - mean_fg) ** 2)
        if var_between > current_max:
            current_max = var_between
            best_thresh_norm = t

    real_thresh = f_min + (best_thresh_norm / 255.0) * (f_max - f_min)
    mask = (feature_map >= real_thresh).astype(np.uint8)
    return mask, real_thresh


def kmeans_segmentation(feature_map: np.ndarray, k: int = 2, max_iters: int = 20) -> np.ndarray:
    """
    K-Means clustering on pixel-level fractal dimension features.
    """
    flat = feature_map.flatten().astype(np.float32)
    # Initialize centroids evenly across percentiles
    percentiles = np.linspace(10, 90, k)
    centroids = np.percentile(flat, percentiles)

    labels = np.zeros_like(flat, dtype=np.int32)

    for _ in range(max_iters):
        # Assign clusters
        dists = np.abs(flat[:, np.newaxis] - centroids[np.newaxis, :])
        new_labels = np.argmin(dists, axis=1)

        if np.array_equal(labels, new_labels):
            break
        labels = new_labels

        # Update centroids
        for c in range(k):
            mask_c = labels == c
            if np.any(mask_c):
                centroids[c] = np.mean(flat[mask_c])

    return labels.reshape(feature_map.shape)
