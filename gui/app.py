"""
Interactive GUI for Local Fractal Dimension Texture Segmentation.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk

from core.local_fractal import compute_local_fractal_map
from core.segmentation import otsu_threshold
from core.evaluation import compute_segmentation_metrics


class TextureSegmentationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Local Fractal Dimension Texture Segmentation Studio")
        self.geometry("950x650")
        self.configure(bg="#F1F5F9")

        self.current_img = None
        self.lfd_map = None
        self.mask = None

        self._build_ui()
        sample = os.path.join(os.path.dirname(__file__), "..", "sample_data", "textures.png")
        if os.path.exists(sample):
            self.load_image(os.path.abspath(sample))

    def _build_ui(self):
        header = tk.Frame(self, bg="#0F766E", height=60, padx=20)
        header.pack(fill=tk.X)
        tk.Label(header, text="TEXTURE SEGMENTATION VIA LOCAL FRACTAL DIMENSION", font=("Segoe UI", 13, "bold"), fg="#FFFFFF", bg="#0F766E").pack(anchor="w", pady=(10, 0))
        tk.Label(header, text="Segmentasi Citra Tekstur Berbasis Differential Box Counting (DBC)", font=("Segoe UI", 9), fg="#CCFBF1", bg="#0F766E").pack(anchor="w")

        tools = tk.Frame(self, bg="#FFFFFF", padx=15, pady=8, relief="groove", bd=1)
        tools.pack(fill=tk.X, padx=15, pady=10)

        ttk.Button(tools, text="Pilih Citra Tekstur...", command=self.on_browse).pack(side=tk.LEFT, padx=5)
        ttk.Button(tools, text="Hitung Peta Fraktal & Segmentasi", command=self.on_segment).pack(side=tk.LEFT, padx=5)

        # 3 Viewports: Original, LFD Map, Mask
        views = tk.Frame(self, bg="#F1F5F9")
        views.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.lbl_v1 = self._create_viewport(views, "Citra Asli")
        self.lbl_v2 = self._create_viewport(views, "Peta Dimensi Fraktal (LFD)")
        self.lbl_v3 = self._create_viewport(views, "Hasil Mask Segmentasi")

        # Status
        self.status = tk.Label(self, text="Siap.", bg="#E2E8F0", anchor="w", padx=10, font=("Segoe UI", 9))
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def _create_viewport(self, parent, title):
        frame = tk.Frame(parent, bg="#FFFFFF", relief="groove", bd=1)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
        tk.Label(frame, text=title, font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#334155").pack(pady=4)
        lbl = tk.Label(frame, bg="#E2E8F0")
        lbl.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        return lbl

    def load_image(self, path):
        img = Image.open(path).convert("L")
        self.current_img = np.array(img)
        self._display(self.lbl_v1, img)
        self.status.config(text=f"Citra dimuat: {os.path.basename(path)}")

    def _display(self, target_lbl, pil_img):
        resized = pil_img.resize((260, 260), Image.Resampling.NEAREST)
        tk_img = ImageTk.PhotoImage(resized)
        target_lbl.image = tk_img
        target_lbl.config(image=tk_img)

    def on_browse(self):
        f = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if f:
            self.load_image(f)

    def on_segment(self):
        if self.current_img is None:
            return
        self.status.config(text="Menghitung dimensi fraktal lokal...")
        self.update_idletasks()

        lfd = compute_local_fractal_map(self.current_img, window_size=15, stride=2)
        mask, thresh = otsu_threshold(lfd)

        # Normalize LFD map to visual image
        norm_lfd = ((lfd - np.min(lfd)) / (np.max(lfd) - np.min(lfd) + 1e-6) * 255).astype(np.uint8)
        self._display(self.lbl_v2, Image.fromarray(norm_lfd))
        self._display(self.lbl_v3, Image.fromarray(mask * 255))
        self.status.config(text=f"Segmentasi Selesai (Ambang LFD: {thresh:.3f})")


def launch_gui():
    app = TextureSegmentationApp()
    app.mainloop()


if __name__ == "__main__":
    launch_gui()
