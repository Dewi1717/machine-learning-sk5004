# Detail Proyek RBL

**Judul:** Klasifikasi Data Phase Space IAEA untuk Menilai Pengaruh Variasi Field Size terhadap Kualitas Berkas X-Ray dan Dosis Serap pada Varian Clinac 600C 6 MV

## Pertanyaan riset (dari concept map w11)
- **RQ1:** Bagaimana pengaruh variasi field size terhadap kualitas berkas X-ray 6 MV (spektrum energi, energi rata-rata, TPR20,10, PDD10)?
- **RQ2:** Seberapa akurat Random Forest, SVM, Naive Bayes, dan KNN membedakan data phase space dari field size yang berbeda, berdasarkan ciri tiap partikel?
- **RQ3:** Ciri partikel mana yang paling menentukan perbedaan antar field size, dan bagaimana kaitannya dengan dosis serap?

## 1. Sumber data
- **IAEA Phase-space Database for External Beam Radiotherapy:** https://www-nds.iaea.org/phsp/photon1/
- Linac **Varian Clinac 600C**, berkas foton **6 MV**.
- Format IAEA: `.IAEAheader` (metadata) + `.IAEAphsp` (biner). Setiap record berisi jenis partikel, energi, posisi x/y, cosinus arah u/v (w), dan bobot statistik.
- Label kelas: **field size**, sesuai ukuran yang tersedia di database. ⚠️ Daftar field size perlu dicek langsung di situs IAEA.
- File berukuran besar (jutaan partikel), sehingga dipakai sub-sampel acak per field size.

## 2. Metode
1. **Membaca phase space:** reader Python (numpy) berdasarkan informasi di `.IAEAheader`.
2. **Rekayasa fitur:** energi E, jarak radial r = √(x² + y²), sudut terhadap sumbu berkas, jenis partikel.
3. **Klasifikasi field size:** Random Forest, SVM, Naive Bayes, KNN (scikit-learn), 10-fold stratified cross-validation.
4. **Evaluasi:** accuracy, precision, recall, F1 (per kelas, one-vs-rest), confusion matrix, feature importance.
5. **Kualitas berkas:** spektrum energi, energi rata-rata, fluens vs radius, TPR20,10 dan PDD10.
6. **Dosis serap (opsional):** simulasi Monte Carlo di fantom air dengan input phase space (EGSnrc/DOSXYZnrc atau TOPAS), menghasilkan PDD, profil, dan output factor.

Lingkungan kerja: Python 3.11, numpy, pandas, scikit-learn, matplotlib dalam virtual environment + `requirements.txt` (seperti w10–w11).

## 3. Estimasi waktu: 4 minggu
| Minggu | Kegiatan |
|---|---|
| 1 | unduh data, reader phase space, eksplorasi data (EDA) |
| 2 | rekayasa fitur + klasifikasi 4 algoritma |
| 2–3 | analisis kualitas berkas (spektrum, TPR20,10, PDD10) |
| 3–4 | dosis Monte Carlo (opsional / target tambahan) |
| 4 | menyusun luaran: Medium, YouTube, Gist, OSF |

## 4. Target luaran
| Luaran | Isi | Penanggung jawab |
|---|---|---|
| Medium story | cerita populer tentang phase space dan pengaruh field size | [Anggota 1] |
| YouTube video | video 5–10 menit tentang alur riset dan hasilnya | [Anggota 2] |
| Gist code | kode reader + klasifikasi yang bisa dijalankan ulang | [Anggota 3] |
| OSF slides | slide hasil lengkap + DOI | [Anggota 4] |

## 5. Anggota tim (maksimal 4)
1. [Nama] ([NIM])
2. [Nama] ([NIM])
3. [Nama] ([NIM])
4. [Nama] ([NIM])
