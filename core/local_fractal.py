"""
Local Fractal Dimension (LFD) Feature Map Extractor.
Implements Differential Box Counting (DBC) and Multi-Scale Sliding Box Counting
to compute pixel-level local fractal dimension maps.
"""

from typing import Tuple
import numpy as np


def compute_differential_box_counting_patch(patch: np.ndarray, scales=(2, 4, 8)) -> float:
    """
    Computes Differential Box Counting (Sarkar & Chaudhuri, 1994) on an N x N patch.
    Treats grayscale intensity as the third spatial dimension (x, y, z).
    """
    h, w = patch.shape
    if min(h, w) < max(scales):
        return 2.0

    counts = []
    inv_scales = []

    for s in scales:
        grid_y = h // s
        grid_x = w // s
        if grid_y == 0 or grid_x == 0:
            continue

        trimmed = patch[: grid_y * s, : grid_x * s]
        blocks = trimmed.reshape(grid_y, s, grid_x, s)

        # Min and Max intensity in each sub-block
        min_vals = blocks.min(axis=(1, 3))
        max_vals = blocks.max(axis=(1, 3))

        # Height of box in intensity space: s / 256
        intensity_scale = 256.0 / (h / float(s))
        boxes_occupied = np.ceil((max_vals - min_vals) / max(1e-3, intensity_scale)) + 1
        n_s = np.sum(boxes_occupied)

        counts.append(max(1.0, float(n_s)))
        inv_scales.append(1.0 / float(s))

    if len(counts) < 2:
        return 2.0

    log_inv = np.log(inv_scales)
    log_counts = np.log(counts)
    poly = np.polyfit(log_inv, log_counts, 1)
    df = float(poly[0])
    return max(1.0, min(3.0, df))


def compute_local_fractal_map(
    image: np.ndarray,
    window_size: int = 15,
    stride: int = 2
) -> np.ndarray:
    """
    Computes dense 2D Local Fractal Dimension (LFD) map.
    """
    h, w = image.shape
    half = window_size // 2

    # Pad image
    padded = np.pad(image.astype(np.float32), half, mode="reflect")

    out_h = (h + stride - 1) // stride
    out_w = (w + stride - 1) // stride
    lfd_map_low = np.zeros((out_h, out_w), dtype=np.float32)

    scales = (2, 4) if window_size < 16 else (2, 4, 8)

    for i, y in enumerate(range(half, half + h, stride)):
        for j, x in enumerate(range(half, half + w, stride)):
            patch = padded[y - half : y + half + 1, x - half : x + half + 1]
            lfd_map_low[i, j] = compute_differential_box_counting_patch(patch, scales=scales)

    # Upsample back to (h, w)
    if stride > 1:
        from PIL import Image
        pil_low = Image.fromarray(lfd_map_low)
        pil_up = pil_low.resize((w, h), Image.Resampling.BILINEAR)
        lfd_map = np.array(pil_up, dtype=np.float32)
    else:
        lfd_map = lfd_map_low

    return lfd_map
