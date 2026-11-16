"""
Segmentation Accuracy Evaluation Module.
Computes IoU (Jaccard Index), Dice Similarity Coefficient (F1), and Pixel Accuracy.
"""

from typing import Dict, Any
import numpy as np


def compute_segmentation_metrics(pred_mask: np.ndarray, gt_mask: np.ndarray) -> Dict[str, float]:
    p = (pred_mask > 0).astype(np.uint8)
    g = (gt_mask > 0).astype(np.uint8)

    tp = int(np.sum((p == 1) & (g == 1)))
    fp = int(np.sum((p == 1) & (g == 0)))
    fn = int(np.sum((p == 0) & (g == 1)))
    tn = int(np.sum((p == 0) & (g == 0)))

    # Handle polarity inversion if necessary (unsupervised clustering might flip 0 and 1)
    iou1 = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 1.0
    # Inverted check
    tp_inv = tn
    fp_inv = fn
    fn_inv = fp
    iou_inv = tp_inv / (tp_inv + fp_inv + fn_inv) if (tp_inv + fp_inv + fn_inv) > 0 else 1.0

    if iou_inv > iou1:
        # Flipped cluster labeling
        tp, fp, fn, tn = tp_inv, fp_inv, fn_inv, int(np.sum((p == 1) & (g == 1)))
        iou = iou_inv
    else:
        iou = iou1

    dice = (2.0 * tp) / (2.0 * tp + fp + fn) if (2.0 * tp + fp + fn) > 0 else 1.0
    pixel_acc = (tp + tn) / float(p.size) if p.size > 0 else 1.0

    return {
        "iou": float(iou),
        "dice": float(dice),
        "pixel_accuracy": float(pixel_acc),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
    }
