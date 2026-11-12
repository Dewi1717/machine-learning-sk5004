# Persiapan Kuis Genetic Algorithm (w13)

Bahan: slide `17_ga_short_intro.pdf` (https://osf.io/c87ka); ringkasannya ada di `../w12-genetic-algorithm/ringkasan-slide.md`.
Kuis aslinya ada di Edunex. File ini hanya **latihan mandiri** untuk persiapan, bukan kunci jawaban kuis.

---

## A. Rangkuman 1 halaman

**Posisi GA:** Metaheuristik ⊃ Evolutionary Computation (EC) ⊃ GA.
Anggota EC: GA, Genetic Programming (GP), Differential Evolution (DE), Evolution Strategy (ES), Evolutionary Programming (EP).

**6 kelompok metaheuristik:** neighborhood heuristics, evolutionary computation, swarm intelligence, human intelligence, astronomi & fisika, fenomena alam.

**Istilah**

| Istilah | Arti | Contoh pada kromosom `1 0 1 1 0` |
|---|---|---|
| Populasi | sekumpulan solusi kandidat | 50 kromosom seperti ini |
| Kromosom | satu solusi (individu) | `1 0 1 1 0` |
| Gen | satu posisi dalam kromosom | posisi ke-3 |
| Alel | nilai gen | nilai pada posisi ke-3 = `1` |

**5 komponen:** populasi, fungsi fitness, seleksi, crossover, mutasi.
**3 operator genetik:** seleksi, crossover (rekombinasi), mutasi.

**7 langkah:** (1) inisialisasi → (2) evaluasi fitness → (3) seleksi → (4) crossover → (5) mutasi → (6) penggantian (*replacement*) → (7) ulangi 2–6 sampai jumlah generasi tercapai atau kondisi berhenti terpenuhi.

**Seleksi**
- *Roulette wheel*: peluang = fitnessᵢ / Σfitness
- *Tournament*: ambil k individu acak, pilih yang terbaik
- *Rank-based*: peluang berdasarkan peringkat, bukan nilai fitness mentah

**Crossover**
- *Single-point*: satu titik potong, ekor kedua induk ditukar
- *Multi-point*: beberapa titik potong
- *Uniform*: tiap gen diambil acak dari salah satu induk; keragamannya tinggi
- *Blend*: gen anak = campuran gen induk dengan faktor acak (untuk encoding real)

**Mutasi:** perubahan acak berpeluang **kecil** untuk menjaga keragaman dan menjelajah ruang solusi baru. Contohnya *bit flip* untuk biner, *swap* untuk permutasi, dan *Gaussian* untuk bilangan real.

**Elitisme:** individu terbaik langsung dibawa ke generasi berikutnya (*survival of the fittest*).

**Kapan memakai GA:** fungsi objektif yang tidak bisa diturunkan, diskret/kombinatorial (rute, penjadwalan), atau punya banyak optimum lokal. Hasilnya **aproksimasi**, bukan jaminan optimum global.

**KMA (Komodo Mlipir Algorithm):** metaheuristik dari Indonesia dengan 3 kelompok:
- *big males*: eksploitasi tinggi, eksplorasi rendah
- *female*: kawin dengan big male terbaik (eksploitasi) atau partenogenesis (eksplorasi)
- *small males*: gerakan *mlipir* (eksplorasi)

---

## B. Soal latihan

**1.** Urutkan dari yang paling umum ke yang paling khusus: GA, metaheuristik, evolutionary computation.

**2.** Pada kromosom `A C B E D`, apa yang disebut gen dan apa yang disebut alel?

**3.** Sebutkan 7 langkah GA secara berurutan.

**4.** Empat individu memiliki fitness 10, 20, 30, 40. Dengan *roulette wheel selection*:
  a. berapa peluang tiap individu terpilih?
  b. jika bilangan acak r = 0,45 dipakai pada peluang kumulatif, individu ke berapa yang terpilih?

**5.** *Single-point crossover* pada induk `P1 = 1100101` dan `P2 = 0011100` dengan titik potong setelah bit ke-3. Tuliskan kedua anaknya.

**6.** Mengapa mutasi *bit flip* tidak cocok untuk kromosom rute `0-3-2-1-4`? Mutasi apa yang cocok?

**7.** Apa beda *tournament selection* dan *rank-based selection*?

**8.** Apa yang terjadi jika peluang mutasi terlalu besar? Bagaimana jika terlalu kecil?

**9.** Untuk memaksimalkan f(x) = x² dengan x bilangan bulat 0–31 (encoding 5 bit), berapa fitness kromosom `10011`?

**10.** Sebutkan 3 aplikasi GA dari slide.

**11.** Benar atau salah: "GA selalu menemukan solusi optimum global."

**12.** Apa fungsi elitisme?

---

## C. Pembahasan

1. Metaheuristik ⊃ evolutionary computation ⊃ GA.
2. Gen = posisi (mis. posisi ke-2). Alel = nilai pada posisi itu (mis. `C`).
3. Inisialisasi → evaluasi → seleksi → crossover → mutasi → penggantian → ulangi.
4. a. Σ = 100, jadi peluangnya 0,1; 0,2; 0,3; 0,4.
   b. Peluang kumulatif 0,1 | 0,3 | 0,6 | 1,0. r = 0,45 berada di selang (0,3; 0,6], jadi yang terpilih **individu ke-3** (fitness 30).
5. `P1 = 110|0101`, `P2 = 001|1100` → anak 1 = `110` + `1100` = **`1101100`**, anak 2 = `001` + `0101` = **`0010101`**.
6. Kromosom rute adalah permutasi. Jika satu gen diubah begitu saja, akan muncul kota ganda atau kota yang hilang. Yang cocok adalah **swap** (tukar dua posisi), **inversion**, atau **scramble**.
7. Tournament: ambil subset acak berukuran k, pemenangnya yang fitness-nya terbaik. Rank-based: semua individu diurutkan, peluang ditentukan dari peringkat, sehingga tidak terpengaruh skala nilai fitness.
8. Terlalu besar: pencarian menjadi hampir acak dan solusi baik ikut rusak. Terlalu kecil: populasi cepat seragam dan terjebak optimum lokal (*premature convergence*).
9. `10011`₂ = 16 + 2 + 1 = 19, jadi f = 19² = **361**.
10. Contohnya: perencanaan jalur robot, lokasi stasiun pengisian kendaraan listrik, optimasi jaringan komputer. Yang lain: sistem energi hibrid, prediksi COVID-19, pertanian presisi (IopaT), komposisi gizi, *cellular manufacturing*, kinetika reaksi kimia, maksimisasi pengaruh di media sosial.
11. **Salah.** GA menghasilkan solusi aproksimasi yang baik, tanpa jaminan optimum global.
12. Menjaga individu terbaik agar tidak hilang akibat crossover atau mutasi, sehingga fitness terbaik tidak pernah turun dari generasi ke generasi.

Contoh kode GA yang sudah diuji (curve fitting dan rute 15 toko) ada di `../w12-genetic-algorithm/ga_examples.py`.
