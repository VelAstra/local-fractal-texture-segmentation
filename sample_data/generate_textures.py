"""
Synthetic Multi-Texture Composite Image Generator.
Creates textured images combining smooth surfaces and high-complexity fractal textures.
"""

import os
from typing import Tuple
import numpy as np
from PIL import Image


def generate_texture_composite(size: int = 128, filepath: str = "sample_data/textures.png") -> Tuple[str, np.ndarray]:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # 1. Background: rough high-frequency fractal-like noise
    rng = np.random.default_rng(42)
    bg = rng.normal(128, 45, (size, size))

    # 2. Foreground: circular smooth gradient patch
    y, x = np.mgrid[0:size, 0:size]
    center = size // 2
    dist = np.sqrt((x - center) ** 2 + (y - center) ** 2)
    radius = size // 3
    gt_mask = (dist <= radius).astype(np.uint8)

    fg = 180 + 30 * np.sin(x / 5.0)

    composite = np.where(gt_mask == 1, fg, bg)
    composite = np.clip(composite, 0, 255).astype(np.uint8)

    Image.fromarray(composite, mode="L").save(filepath)
    mask_path = os.path.splitext(filepath)[0] + "_mask.png"
    Image.fromarray(gt_mask * 255, mode="L").save(mask_path)

    return filepath, gt_mask


if __name__ == "__main__":
    p, m = generate_texture_composite()
    print(f"Generated texture sample: {p} and ground truth mask")
