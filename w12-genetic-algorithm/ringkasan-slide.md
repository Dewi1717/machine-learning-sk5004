# Ringkasan Slide — Genetic Algorithm: A Very Short Intro

Sumber: Sparisoma Viridi, `17_ga_short_intro.pdf`, v6 (14 Mei 2025), https://osf.io/c87ka

---

## 1. Pengantar (slide 3–21)
- **Optimasi** adalah mencari input yang membuat fungsi objektif bernilai maksimum atau minimum. Pembagian utama algoritma optimasi: apakah fungsi objektifnya **bisa diturunkan** (berbasis gradien) atau tidak.
- Trik untuk masalah sulit: sederhanakan dulu masalahnya (misalnya dengan *Gaussian smoothing* fungsi biaya), lalu tambahkan kembali kompleksitasnya secara bertahap.
- **Komodo Mlipir Algorithm (KMA)** adalah metaheuristik buatan Indonesia. Populasinya dibagi tiga kelompok:
  - *big males*: eksploitasi tinggi
  - *female*: kawin dengan big male terbaik (eksploitasi) atau partenogenesis (eksplorasi)
  - *small males*: gerakan *mlipir* (eksplorasi)
- **Metaheuristik** menyelesaikan masalah optimasi kompleks dengan meniru fenomena alam atau kecerdasan manusia. Ada 6 kelompok: neighborhood heuristics, evolutionary computation, swarm intelligence, human intelligence, astronomi/fisika, dan fenomena alam.
- **Hierarki:** Metaheuristik ⊃ Evolutionary Computation (EC) ⊃ GA. Keluarga EC terdiri dari GA, Genetic Programming, Differential Evolution, Evolution Strategy, dan Evolutionary Programming.

## 2. Aplikasi (slide 22–33)
Optimasi jaringan komputer (*oriented crossover*), sistem energi hibrid terbarukan, perencanaan jalur robot, lokasi SPKLU (Irlandia), maksimisasi pengaruh di media sosial, prediksi kasus COVID-19 (ANFIS + GA), pertanian presisi (IopaT), komposisi gizi seimbang, *cellular manufacturing*, dan optimasi koefisien laju reaksi kimia.

## 3. Algoritma (slide 34–59)
- **GA** adalah teknik pencarian solusi aproksimasi yang terinspirasi evolusi biologis: pewarisan, mutasi, dan seleksi alam (Darwin).
- **Istilah:**

| Istilah | Arti |
|---|---|
| Populasi | himpunan sebagian dari semua solusi yang mungkin |
| Kromosom | satu solusi (individu) |
| Gen | satu posisi elemen dalam kromosom |
| Alel | nilai gen pada kromosom tertentu |

- **Komponen:**
  - **Populasi**: kromosom bisa dikodekan sebagai biner, array, atau struktur data lain (mis. rute truk)
  - **Fungsi fitness**: menilai seberapa baik setiap solusi; makin tinggi makin baik
  - **Seleksi**:
    - *roulette wheel*: peluang terpilih sebanding dengan fitness
    - *tournament*: individu terbaik dari subset acak
    - *rank-based*: peluang berdasarkan peringkat
  - **Crossover**: menggabungkan dua induk. Jenisnya single-point, multi-point, uniform, dan blend.
  - **Mutasi**: perubahan acak dengan peluang kecil untuk menjaga keragaman populasi dan menjelajah ruang solusi baru
- **7 langkah:** (1) inisialisasi → (2) evaluasi → (3) seleksi → (4) crossover → (5) mutasi → (6) penggantian → (7) ulangi langkah 2–6 sampai jumlah generasi tercapai atau kondisi berhenti terpenuhi.

## 4. Ilustrasi (slide 60–66)
- Elitisme (*survival of the fittest*), crossover, dan mutasi dari generasi k ke k+1.
- Kromosom berupa urutan toko yang dikunjungi dari supply point (encoding permutasi).
- Konvergensi parameter a, b, c dalam ±10 generasi (contoh DataCamp).
- Rute TSP membaik dari generasi 0 → 5 → 69.

## 5. Kode (slide 67–72)
Dua contoh kode dari internet yang **belum dites**: DataCamp (Amberle McKee, 2024) untuk mencari parameter kurva U, dan MLInsightsCentral (2023) untuk masalah rute stasiun.

## 6. Penutup (slide 73–76)
Feedback diminta di https://github.com/dudung/simple-talks/issues/1

---

## Hasil uji kode sendiri (`ga_examples.py`)
Kedua contoh mengikuti 7 langkah di slide dan dijalankan di venv `sk5004-w11-a` (Python 3.11.9, numpy 2.4.6).

| Contoh | Encoding & operator | Hasil GA | Pembanding |
|---|---|---|---|
| A. Curve fitting y = ax² + bx + c (data dari a=2, b=−3, c=1 + noise) | real; tournament, blend crossover (BLX-0.5), mutasi Gaussian, elitisme | a=1.9791, b=−2.9487, c=1.0080, MSE 0.1619 | least squares: a=1.9788, b=−2.9487, c=1.0098, MSE 0.1619 |
| B. Rute supply point + 15 toko (TSP) | permutasi; tournament, order crossover (OX), swap mutation, elitisme | panjang 17.100 (stabil sejak generasi ~50) | nearest-neighbour + 2-opt: 17.091 |

Gambar: `output/A_curve_fitting.png`, `output/B_tsp_route.png`.
