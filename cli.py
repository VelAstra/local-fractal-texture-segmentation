"""
CLI for Local Fractal Dimension Texture Segmentation.
"""

import argparse
import sys
import numpy as np
from PIL import Image

from core.local_fractal import compute_local_fractal_map
from core.segmentation import otsu_threshold, kmeans_segmentation
from core.evaluation import compute_segmentation_metrics


def cmd_segment(args):
    img = Image.open(args.input).convert("L")
    arr = np.array(img)
    print(f"[Segmentation] Memproses citra: {args.input} ({arr.shape[1]}x{arr.shape[0]})")

    lfd = compute_local_fractal_map(arr, window_size=args.window, stride=args.stride)
    mask, thresh = otsu_threshold(lfd)

    out_mask_path = args.output or "sample_data/segmented_mask.png"
    Image.fromarray(mask * 255, mode="L").save(out_mask_path)
    print(f"Mask segmentasi disimpan di: {out_mask_path} (Ambang LFD: {thresh:.3f})")

    if args.gt:
        gt = np.array(Image.open(args.gt).convert("L")) > 128
        metrics = compute_segmentation_metrics(mask, gt)
        print("\n" + "=" * 45)
        print("METRIK EVALUASI SEGMENTASI TEKSTUR")
        print("=" * 45)
        print(f"Intersection over Union (IoU) : {metrics['iou']*100:.2f}%")
        print(f"Dice Similarity (DSC / F1)   : {metrics['dice']*100:.2f}%")
        print(f"Pixel Accuracy               : {metrics['pixel_accuracy']*100:.2f}%")
        print("=" * 45 + "\n")


def cmd_gui(args):
    from gui.app import launch_gui
    launch_gui()


def main():
    p = argparse.ArgumentParser(description="Local Fractal Dimension Texture Segmentation")
    sub = p.add_subparsers(dest="command")

    p_seg = sub.add_parser("segment", help="Run texture segmentation")
    p_seg.add_argument("input", help="Input texture image")
    p_seg.add_argument("-o", "--output", help="Output mask path")
    p_seg.add_argument("--gt", help="Ground truth mask path for evaluation")
    p_seg.add_argument("--window", type=int, default=15, help="Sliding window size (default: 15)")
    p_seg.add_argument("--stride", type=int, default=2, help="Sliding stride (default: 2)")

    sub.add_parser("gui", help="Launch interactive Tkinter GUI")

    args = p.parse_args()
    if args.command == "segment":
        cmd_segment(args)
    elif args.command == "gui":
        cmd_gui(args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
