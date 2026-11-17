# LAPORAN CAPSTONE PROJECT

## SEGMENTASI CITRA TEKSTUR MENGGUNAKAN LOCAL FRACTAL DIMENSION (LFD) DAN ADAPTIVE CLUSTERING
### (*Texture Image Segmentation Based on Local Fractal Dimension and Multi-Scale Clustering*)

**Program Studi**: S1 Ilmu Komputer / Informatika  
**Fakultas**: Matematika dan Ilmu Pengetahuan Alam (FMIPA)  
**Kelompok**: Tim Pengembang Capstone DIKE FMIPA UGM  
**Anggota Tim**:  
1. Aji Kusuma Putra (NIM: 22/503701/PA/21657)  
2. Rayhan Haldi Hermawan (NIM: 24/545406/PA/23176)  
**Kontak**: Rayhanhaldi13@gmail.com | [GitHub Repositori](https://github.com/VelAstra)  
**Tahun Akademik**: 2026/2027  

---

## RINGKASAN EKSEKUTIF

Segmentasi tekstur citra merupakan tahapan kritis dalam analisis citra medis, mikroskopi material, dan penginderaan jauh. Metode segmentasi berbasis intensitas warna sering kali gagal ketika dua wilayah berbeda memiliki rata-rata intensitas abu-abu yang identik namun pola kekasaran spasial yang kontras.

Proyek capstone ini merancang dan mengimplementasikan sistem segmentasi tekstur berbasis **Local Fractal Dimension (LFD)** menggunakan algoritma *Differential Box Counting* (DBC). Dengan memperlakukan variasi intensitas piksel sebagai dimensi spasial ketiga $(x, y, z)$, nilai dimensi fraktal lokal diekstraksi pada setiap jendela geser untuk membentuk peta fitur fraktal 2D densitas tinggi. Segmentasi dilakukan secara adaptif menggunakan ambang batas Otsu dan clustering K-Means. Sistem diuji pada citra komposit multi-tekstur, mencapai nilai **Intersection over Union (IoU) 84,2%** dan **Dice Similarity Coefficient 91,4%**.

---

## BAB I: PENDAHULUAN

### 1.1 Latar Belakang
Tekstur alami memiliki variasi mikro yang sulit dikarakterisasi hanya dengan filter linier atau gradien orde pertama. Teori geometri fraktal menyediakan kerangka matematis yang kuat untuk mengukur kekasaran permukaan (*surface roughness*) dan keteraturan diri.

### 1.2 Rumusan Masalah
1. Bagaimana mengimplementasikan algoritma Differential Box Counting (DBC) yang efisien untuk menghasilkan peta dimensi fraktal lokal (*LFD Map*)?
2. Bagaimana memisahkan batas wilayah tekstur berdasarkan distribusi nilai LFD menggunakan ambang adaptif Otsu?
3. Bagaimana mengukur akurasi segmentasi terhadap ground-truth menggunakan metrik IoU dan Dice Coefficient?

### 1.3 Pembagian Tugas Tim Capstone (2 Mahasiswa)
1. **Aji Kusuma Putra** (NIM: 22/503701/PA/21657): Preprocessing citra tekstur, normalisasi kontras, sintesis pola tekstur komposit, perancangan algoritma Differential Box Counting (DBC), dan generator peta LFD kontinu. (`sample_data/generate_textures.py`, `core/local_fractal.py`).
2. **Rayhan Haldi Hermawan** (NIM: 24/545406/PA/23176): Segmentasi adaptif Otsu, klasterisasi K-Means multi-wilayah, Desktop GUI Tkinter, visualisasi peta panas LFD, integrasi CLI, dan evaluasi metrik kuantitatif (IoU, Dice, Pixel Accuracy). (`core/segmentation.py`, `core/evaluation.py`, `gui/app.py`, `cli.py`).

---

## BAB II: LANDASAN TEORI & FORMULASI MATEMATIKA

### 2.1 Differential Box Counting (DBC)
Pada bidang citra $M \times M$, blok berukuran $s \times s$ dipertimbangkan. Jika nilai intensitas abu-abu minimum dan maksimum pada blok tersebut adalah $I_{\min}$ dan $I_{\max}$, maka kontribusi jumlah kotak berukuran $s$ pada kolom tersebut adalah:
$$n_r(i, j) = \text{ceil}\left( \frac{I_{\max} - I_{\min}}{s'} \right) + 1$$
Total kotak terisi adalah $N_r = \sum n_r(i, j)$. Dimensi fraktal lokal $D_F$ diperoleh dari kemiringan regresi linier dalam ruang log-log:
$$D_F = \frac{\Delta \log(N_r)}{\Delta \log(1 / r)}$$

---

## BAB III: METODOLOGI & ARSITEKTUR SISTEM

Alur kerja sistem:
1. Pembacaan citra tekstur grayscale.
2. Pemindaian jendela geser (*sliding window*) untuk mengekstraksi matriks sub-blok.
3. Estimasi LFD lokal pada setiap koordinat $(x, y)$.
4. Pembangkitan peta fitur kontinu dimensi fraktal.
5. Pemisahan wilayah tekstur menggunakan ambang batas inter-kelas variansi Otsu.
6. Evaluasi kuantitatif terhadap masker kebenaran (*ground truth*).

---

## BAB IV: PENGUJIAN DAN EVALUASI

Hasil pengujian pada citra komposit tekstur sintesis dan dataset Brodatz:
* **Intersection over Union (IoU)**: 84,2%
* **Dice Similarity Coefficient (DSC)**: 91,4%
* **Pixel Accuracy**: 95,8%
* **Waktu Komputasi**: 0,18 s untuk citra $128 \times 128$.

---

## BAB V: KESIMPULAN

Dimensi fraktal lokal (LFD) berhasil menjadi deskriptor tekstur diskriminatif yang mampu membedakan wilayah dengan tingkat kekasaran berbeda meskipun nilai kecerahan rata-ratanya serupa.
