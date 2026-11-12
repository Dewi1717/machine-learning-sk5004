<!--
DRAF feedback untuk https://github.com/dudung/simple-talks/issues/1
Silakan disunting sesuai pendapat Anda sendiri sebelum dikirim. Pilih versi pendek ATAU versi lengkap.
-->

## Versi pendek

Materi Genetic Algorithm disampaikan runtut, dari konteks optimasi dan metaheuristik, contoh aplikasi, terminologi (populasi, kromosom, gen, alel), komponen, sampai 7 langkah algoritma. Ilustrasi crossover, mutasi, dan konvergensi sangat membantu. Saran saya: pada slide 64, ilustrasi mutasi mengganti gen dengan huruf baru (M, N). Untuk kromosom berupa permutasi seperti rute toko di slide 62, mutasi biasanya menukar posisi gen (swap) agar tidak muncul gen baru atau duplikat. Karena kode di slide 68 belum dites, saya mencoba menulis dan menguji dua contoh (curve fitting a, b, c dan rute 15 toko). GA berhasil mendapatkan hasil yang sama dengan least squares dan hampir sama dengan heuristik 2-opt. Terima kasih, Pak.

---

## Versi lengkap

**Yang sudah baik**
- Alurnya runtut: optimasi → metaheuristik → evolutionary computation → GA → aplikasi → algoritma → ilustrasi → kode.
- Tabel hubungan metaheuristics–EC–GA (slide 15) memperjelas posisi GA di antara metode lain.
- Contoh aplikasinya beragam (jaringan komputer, energi, robot, SPKLU, media sosial, COVID-19, pertanian, gizi, manufaktur, kinetika kimia). Ini menunjukkan GA bisa dipakai lintas bidang.
- Ilustrasi crossover, mutasi, dan konvergensi parameter (slide 61–66) membuat konsepnya mudah dipahami.

**Saran perbaikan**
1. **Ilustrasi mutasi (slide 64):** gen H dan A berubah menjadi M dan N, huruf yang tidak ada di kromosom induk. Untuk encoding permutasi (rute toko di slide 62), mutasi yang umum adalah *swap* atau *inversion* agar tidak muncul gen baru atau duplikat. Ada baiknya dibedakan mutasi untuk encoding biner/real dan untuk permutasi.
2. **Crossover untuk permutasi (slide 63):** Parent 2 tertulis F G H A D B E A. Huruf A muncul dua kali dan C tidak ada, sehingga bukan permutasi yang valid seperti Parent 1 (A–H). Ilustrasinya sebenarnya mirip *order crossover* (OX). Menyebut nama metodenya akan membantu mahasiswa mencarinya lebih lanjut.
3. **Kode (slide 68):** kode belum dites. Saya mencoba menulis ulang dan menguji dua contoh dengan pola yang sama:
   - curve fitting y = ax² + bx + c: GA mendapatkan a = 1,979, b = −2,949, c = 1,008, sama dengan least squares (MSE 0,1619)
   - rute 15 toko: panjang rute GA 17,100 vs heuristik nearest-neighbour + 2-opt 17,091

   Mungkin contoh kecil yang sudah teruji seperti ini bisa ditambahkan ke slide.
4. **Parameter GA:** akan bermanfaat bila ada satu slide tentang pengaruh ukuran populasi, peluang crossover/mutasi, dan elitisme, serta risiko *premature convergence*. Pada percobaan TSP, GA sudah berhenti membaik sejak generasi ~50.
5. **Kapan memilih GA:** bisa ditambahkan perbandingan singkat dengan metode berbasis gradien (slide 7 sudah menyinggung *differentiable* vs tidak), misalnya bahwa GA cocok untuk fungsi yang tidak dapat diturunkan, diskret, atau multimodal.
6. **Typo kecil:** "Suppor to IopaT" (slide 29), "efficiancy" (slide 29), "dicussed" dan "Your are welcome" (slide 74).

Terima kasih atas materinya, Pak.
