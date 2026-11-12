# Ringkasan Slide — Support Vector Machine (a very short intro)

Sumber: Sparisoma Viridi, `13_svm_short_intro.pdf`, v8 (24 Apr 2025), https://osf.io/pzqf9

---

## 1. Pengantar (slide 3–8)
- **SVM** adalah algoritma *supervised learning*. SVM mengklasifikasi data dengan mencari **hyperplane optimal** yang **memaksimalkan jarak (margin)** antara titik-titik terdekat dari kelas yang berbeda di ruang N-dimensi.
- **Aplikasi:** citra medis (deteksi tumor di X-ray/MRI), filter spam, bioinformatika (klasifikasi gen, fungsi protein), dan keuangan (peramalan, penilaian risiko).
- **Kelebihan** (menurut scikit-learn): efektif di ruang berdimensi tinggi; tetap efektif ketika jumlah dimensi lebih besar dari jumlah sampel; hemat memori karena hanya memakai *support vectors*; fleksibel karena kernel bisa dipilih atau dibuat sendiri.
- **Kekurangan:** lambat untuk dataset besar; parameter C, gamma, dan kernel sulit di-tuning; kurang baik untuk data yang banyak noise atau kelasnya tumpang tindih; sulit diinterpretasi (terutama dengan kernel non-linear); boros memori karena support vectors harus disimpan.

## 2. Ilustrasi dan istilah (slide 9–17)
| Istilah | Arti |
|---|---|
| **Hyperplane** | batas keputusan **w·x − b = 0** |
| **Support vectors** | titik-titik terdekat ke hyperplane, terletak di **w·x − b = ±1** |
| **Margin** | jarak antara support vector dan hyperplane. Lebar total margin = **2/‖w‖** |
| **Weight vector w** | vektor yang tegak lurus terhadap hyperplane |

## 3. Kernel (slide 18–32)
- **Fungsi kernel** k(x, z) = ⟨φ(x), φ(z)⟩ menghitung *dot product* di ruang fitur berdimensi tinggi tanpa harus menghitung φ secara eksplisit. Inilah yang disebut *kernel trick*.
- Dengan memetakan data ke dimensi yang lebih tinggi, data yang **tidak linear-separable** di ruang asal bisa dipisahkan dengan sebuah hyperplane.
- Kernel yang umum dipakai: **linear, polynomial, RBF/Gaussian, sigmoid**. Ada juga Laplace RBF, hyperbolic tangent, Bessel, ANOVA, dan linear splines.

## 4. Flowchart (slide 33–43)
SVM sering menjadi bagian dari sistem yang lebih besar, misalnya:
- *grid search* parameter SVM
- deteksi aktivitas suara (SVM-VAD)
- diagnosis kerusakan dengan PCA nonlinear + SVM
- optimasi parameter SVM dengan fruit fly optimization, genetic algorithm, PSO, atau krill herd
- prakiraan daya angin dengan hybrid EMD-SVM
- hierarchical SVM untuk brain-computer interface

## 5. Langkah klasifikasi biner (slide 44–58)
1. Formulasi masalah: data (xᵢ, yᵢ) dengan yᵢ ∈ {−1, +1}
2. Definisikan hyperplane w·x − b = 0
3. Maksimalkan margin 2/‖w‖, atau setara dengan meminimalkan ½‖w‖² dengan syarat yᵢ(w·xᵢ − b) ≥ 1
4. Bentuk fungsi Lagrangian dengan pengali αᵢ ≥ 0
5. Cari *saddle point* (turunan terhadap w dan b = 0)
6. Ubah ke formulasi *dual* (hanya bergantung pada xᵢ·xⱼ)
7. Selesaikan masalah *quadratic programming*
8. Dapatkan w = Σ αᵢyᵢxᵢ dan b dari support vectors (αᵢ > 0)
9. Prediksi: sign(w·x − b)
10. (Opsional) **Kernel trick**: ganti xᵢ·xⱼ dengan K(xᵢ, xⱼ) untuk data non-linear
11. Prediksi dengan kernel: sign(Σ αᵢyᵢK(xᵢ, x) − b)

## 6. Kode Python dari DataCamp (slide 59–69)
- Dataset breast cancer (569 sampel, 30 fitur, label malignant/benign), split 70/30 dengan `random_state=109`, memakai `svm.SVC(kernel='linear')`.
- Hyperparameter yang bisa di-tuning:
  - **kernel**: polynomial dan RBF untuk batas non-linear
  - **C (regularisasi)**: penalti untuk kesalahan klasifikasi
  - **gamma**: gamma rendah membuat model *longgar* terhadap data latih, gamma tinggi membuatnya terlalu pas (*overfitting*)

> **Catatan koreksi:** slide 68 (dikutip dari DataCamp) menyebut *"smaller C → small-margin, larger C → larger-margin"*. Yang benar justru **kebalikannya**: C kecil → margin **lebar** (lebih toleran terhadap kesalahan), C besar → margin **sempit** (lebih ketat).
> Gambar `output/01_hyperplane_margin.png` membuktikannya: C = 1000 menghasilkan margin 2,56, sedangkan C = 0,05 menghasilkan margin 3,62.

## 7. Challenges (slide 72) dan statusnya
| Challenge | Status |
|---|---|
| Jalankan kode DataCamp secara online | perlu login DataCamp, jadi dikerjakan sendiri (lihat README) |
| Jalankan kode secara lokal | ✅ `svm_datacamp.py` di dalam venv |
| Cari cara membuat dan memakai virtual environment | ✅ `panduan-virtual-environment.md` |

---

## Hasil menjalankan kode secara lokal
Python 3.11.9, scikit-learn 1.9.1, di dalam venv `sk5004-svm`.

**A. Kode DataCamp (kernel linear, tanpa scaling):** hasilnya sama persis dengan tutorial DataCamp.

| Metrik | Nilai |
|---|---|
| Accuracy | **0.9649** |
| Precision | 0.9811 |
| Recall | 0.9630 |

Confusion matrix [malignant, benign] = [[61, 2], [4, 104]], dengan 48 support vector.

**B. Tuning** (data di-standardisasi dengan `StandardScaler`):

| kernel | C | gamma | akurasi uji |
|---|---|---|---|
| linear | 1 | scale | **0.9883** |
| rbf | 1 | scale | 0.9825 |
| sigmoid | 1 | scale | 0.9825 |
| poly | 1 | scale | 0.9006 |
| rbf | 0.01 | scale | 0.6316 (underfit) |
| rbf | 1 | 1.0 | 0.6316 (overfit, 398 SV) |

GridSearchCV 5-fold memilih `rbf, C=10, gamma='scale'`: akurasi CV 0.9723, akurasi uji 0.9883.
Standardisasi saja sudah menaikkan akurasi dari 0.9649 menjadi 0.9883.

**C. Kernel pada data lingkaran:** kernel linear hanya mencapai 62%, sedangkan poly (derajat 2) dan RBF mencapai 100%. Ini menunjukkan kegunaan *kernel trick*.
