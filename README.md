# Local Fractal Dimension for Image Texture Segmentation Suite

> **Proyek Capstone 3**: Segmentasi Citra Tekstur Menggunakan Local Fractal Dimension (LFD) dan Adaptive Clustering  
> **Program Studi**: S1 Ilmu Komputer / Informatika, FMIPA, Universitas Gadjah Mada  
> **Anggota Tim Pengembang**:  
> - Aji Kusuma Putra (NIM: 22/503701/PA/21657)  
> - Rayhan Haldi Hermawan (NIM: 24/545406/PA/23176)  

---

## Ringkasan Proyek
Menggunakan *Differential Box Counting* (DBC) untuk menghitung dimensi fraktal lokal (*Local Fractal Dimension* - LFD) pada setiap piksel citra, menghasilkan peta kekasaran spasial 2D kontinu, dan melakukan segmentasi wilayah tekstur menggunakan ambang batas Otsu serta evaluasi IoU dan Dice Coefficient.

### Pembagian Tugas Tim (2 Mahasiswa)
1. **Aji Kusuma Putra** (`22/503701/PA/21657`): Preprocessing citra tekstur, normalisasi kontras, sintesis pola tekstur komposit, perancangan algoritma Differential Box Counting (DBC), dan generator peta LFD kontinu. (Modul: `sample_data/generate_textures.py`, `core/local_fractal.py`).
2. **Rayhan Haldi Hermawan** (`24/545406/PA/23176`): Segmentasi adaptif Otsu, klasterisasi K-Means multi-wilayah, Desktop GUI Tkinter, visualisasi peta panas LFD, integrasi CLI, dan evaluasi metrik kuantitatif (IoU, Dice, Pixel Accuracy). (Modul: `core/segmentation.py`, `core/evaluation.py`, `gui/app.py`, `cli.py`).

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
