# Local Fractal Dimension for Image Texture Segmentation Suite

> **Proyek Capstone 3**: Segmentasi Citra Tekstur Menggunakan Local Fractal Dimension (LFD) dan Adaptive Clustering  
> **Program Studi**: S1 Ilmu Komputer / Informatika, FMIPA, Universitas Gadjah Mada  

---

## Ringkasan Proyek
Menggunakan *Differential Box Counting* (DBC) untuk menghitung dimensi fraktal lokal (*Local Fractal Dimension* - LFD) pada setiap piksel citra, menghasilkan peta kekasaran spasial 2D kontinu, dan melakukan segmentasi wilayah tekstur menggunakan ambang batas Otsu serta evaluasi IoU dan Dice Coefficient.

### Pembagian Tugas Tim 4 Mahasiswa
1. **Mahasiswa 1**: Preprocessing Citra & Normalisasi Kontras Tekstur.
2. **Mahasiswa 2**: Ekstraksi Fitur DBC & Pembangkitan Peta Dimensi Fraktal Lokal (LFD).
3. **Mahasiswa 3**: Modul Segmentasi Adaptif (Otsu Thresholding & K-Means Clustering).
4. **Mahasiswa 4**: Antarmuka Grafis (Tkinter GUI), Visualisasi Peta Panas, & Evaluasi Metrik (IoU, Dice).

---

## Cara Menjalankan

```bash
# Menjalankan segmentasi dan evaluasi terhadap ground truth
python cli.py segment sample_data/textures.png --gt sample_data/textures_mask.png

# Menjalankan antarmuka grafis
python cli.py gui

# Menjalankan pengujian otomatis
python -m unittest discover tests
```
