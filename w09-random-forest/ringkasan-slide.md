# Ringkasan Slide — Random Forest Algorithm (a very short intro for classification)

Sumber: Sparisoma Viridi, `12_random_forest_intro.pdf`, v6 (23 Apr 2025), https://osf.io/hjdf9  
Contoh data dan ilustrasi di slide diambil dari artikel Samy Baladram di Medium/Towards Data Science.

---

## 1. Pengantar (slide 3–14)

- **Kecerdasan buatan (AI)** adalah sistem komputer yang dapat mengerjakan tugas kompleks yang biasanya membutuhkan penalaran, pengambilan keputusan, atau kreativitas manusia. Rujukannya definisi NASA (EO 13960, Section 238(g) NDAA 2019).
- **Machine learning (ML)** adalah subbidang AI. Mesin belajar dari data (angka, gambar, teks) yang sudah dikumpulkan dan disiapkan sebagai *training data*. Makin banyak data, makin baik.
- Lima kategori algoritma ML (IBM):

| Jenis | Ciri | Contoh |
|---|---|---|
| Supervised | data berlabel, target diketahui | regresi, klasifikasi, Naïve Bayes, NN, **Random Forest** |
| Unsupervised | data tanpa label, mencari pola | K-means, hierarchical clustering, PCA, GMM, Apriori |
| Semi-supervised | sedikit data berlabel + banyak data tak berlabel | GAN |
| Self-supervised | model membuat labelnya sendiri dari bagian input lain | CV, NLP |
| Reinforcement | belajar dari *reward* dan *punishment* | game, robotika |

Random Forest termasuk **supervised learning**.

## 2. Decision Tree (slide 15–50)

- Decision tree dipakai untuk klasifikasi maupun regresi. Model mempelajari **aturan keputusan sederhana** dari data latih.
- Strukturnya hierarkis: **root node → internal node / branch → leaf node**. Keputusan akhir diambil di daun.

### Data contoh (dataset golf)
Fitur: `sunny`, `overcast`, `rainy` (one-hot dari Outlook), `Temperature` (°F), `Humidity` (%), `Wind` (0/1). Target: `Play` (Yes/No).
Data latih 14 baris (indeks 0–13), data uji 14 baris (indeks 14–27).

### Tahap pelatihan
1. Mulai dari seluruh data di root node.
2. Pilih fitur dan *split point* terbaik, yaitu yang menghasilkan **weighted Gini impurity terkecil**. Di root ada 23 kandidat split point.
   - Contoh: `sunny ≤ 0.5` → 9/14·0.346 + 5/14·0.480 = **0.394**
   - `overcast ≤ 0.5` memberi impurity terendah (**0.357**). Sisi kanannya langsung murni (semua Yes).
3. Buat child node dari hasil split.
4. Ulangi langkah 2–3 pada node yang belum murni sampai kriteria berhenti terpenuhi.
5. Beri setiap daun label **kelas mayoritas**. Setelah pohon jadi, sampel latih tidak diperlukan lagi.

### Tahap pengujian
Setiap data uji ditelusuri dari root, mengikuti kondisi di tiap node, sampai mencapai daun. Label daun itulah prediksinya. Pohon tunggal ini hanya memakai sedikit fitur, sehingga akurasinya terbatas.

### Parameter kunci (slide 51–57)
- **max_depth**: kedalaman maksimum pohon. Makin kecil, pohon makin sederhana.
- **min_samples_split**: jumlah sampel minimum di sebuah node agar node itu masih boleh dipecah.
- **min_samples_leaf**: jumlah sampel minimum di setiap daun.
- **criterion**: ukuran kualitas split, yaitu `"gini"` (Gini impurity) atau `"entropy"` (information gain).

## 3. Random Forest (slide 58–83)

- Random Forest menumbuhkan **banyak decision tree**, lalu menggabungkan hasilnya. Idenya: banyak model yang **tidak saling berkorelasi** lebih akurat bila bekerja bersama daripada sendiri-sendiri. Satu pohon bisa salah, tetapi mayoritas pohon cenderung benar.
- **Klasifikasi**: setiap pohon memberi *vote*, dan kelas dengan suara terbanyak menjadi jawaban. **Regresi**: hasilnya rata-rata output semua pohon.

### Mekanisme utama
1. **Bootstrap sampling**: setiap pohon mendapat set latih sendiri yang diambil acak *dengan pengembalian*. Ada data yang muncul berkali-kali dan ada yang tidak terpakai. Data yang tidak terpakai (*out-of-bag*) bisa dipakai untuk menguji pohon itu.
2. **Random feature selection**: saat membuat split, setiap pohon hanya mempertimbangkan subset fitur acak (biasanya √(jumlah fitur)).
3. **Growing trees**: setiap pohon tumbuh dari bootstrap sample dan fitur terpilihnya, sampai node murni atau tidak bisa dipecah lagi.
4. **Final prediction**: semua pohon melakukan voting.

### Tahap pelatihan
Buat beberapa bootstrap sample, lalu bangun satu pohon untuk setiap sample. Ulangi sampai semua sample terpakai.

### Tahap pengujian
Setiap pohon memprediksi data baru lewat jalurnya masing-masing, lalu hasilnya digabung dengan voting mayoritas. Contoh di slide: **74 YES vs 26 NO**, sehingga prediksinya **YES**.

### Tree vs Forest
Satu pohon membuat batas keputusan yang kaku dan mudah *overfit*. Hutan merata-ratakan banyak pohon sehingga hasilnya lebih stabil dan biasanya lebih akurat.

## 4. Kesimpulan slide
- Telah dibahas pengantar ML yang terkait dengan Random Forest.
- Telah ditunjukkan tahapan decision tree dan random forest untuk klasifikasi.
- Telah diberikan perbandingan ilustratif hasil kedua algoritma.

---

## Hasil reproduksi dengan Python (`random_forest_golf.py`)

| Model | Akurasi data uji (14 data) |
|---|---|
| Decision Tree (gini, default) | 42.86% |
| Random Forest (100 pohon, `max_features='sqrt'`) | **64.29%** |

- Split di root sama dengan slide: `overcast ≤ 0.5` (weighted Gini 0.357), dan `sunny ≤ 0.5` menghasilkan 0.394.
- Random Forest lebih akurat daripada satu pohon. Ini sesuai pesan slide "tree vs forest".
- Fitur paling penting menurut Random Forest: **humidity** dan **temperature**.
- Datanya sangat kecil (14 data latih), jadi angka akurasi masih sensitif terhadap *random seed*. Grafik `output/02_tree_vs_forest.png` menunjukkan rata-rata dari 20 seed: akurasi forest naik seiring bertambahnya jumlah pohon dan selalu di atas pohon tunggal.
