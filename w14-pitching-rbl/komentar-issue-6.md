Nama: [NAMA LENGKAP]
NIM: [NIM]

Team Members
1. [Nama] ([NIM])
2. [Nama] ([NIM])
3. [Nama] ([NIM])
4. [Nama] ([NIM])

Project: **Klasifikasi Data Phase Space IAEA untuk Menilai Pengaruh Variasi Field Size terhadap Kualitas Berkas X-Ray dan Dosis Serap pada Varian Clinac 600C 6 MV**

- **Source of data:** IAEA Phase-space Database (https://www-nds.iaea.org/phsp/photon1/), Varian Clinac 600C 6 MV, dengan variasi field size
- **Method:** pembacaan phase space dengan Python → rekayasa fitur partikel (E, r, sudut, jenis) → klasifikasi field size dengan Random Forest, SVM, Naive Bayes, KNN (10-fold CV) → evaluasi accuracy/precision/recall/F1 + feature importance → indikator kualitas berkas (spektrum, TPR20,10, PDD10); dosis Monte Carlo (EGSnrc/TOPAS) sebagai target tambahan
- **Estimated time:** 4 minggu
- **Target outputs:** Medium story ([Anggota 1]), YouTube video ([Anggota 2]), Gist code ([Anggota 3]), OSF slides ([Anggota 4])

Slide pitching: [link ke pitching-rbl-phase-space.pdf]
