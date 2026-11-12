# Naskah Presentasi (±5 menit)

Naskah yang sama juga tersimpan sebagai *speaker notes* di setiap slide pptx.

| Slide | Durasi | Naskah |
|---|---|---|
| 1. Judul | 0:20 | Selamat pagi/siang. Saya akan mempresentasikan ide proyek RBL: klasifikasi data phase space IAEA untuk menilai pengaruh field size terhadap kualitas berkas X-ray dan dosis serap pada Varian Clinac 600C 6 MV. |
| 2. Masalah & RQ | 0:50 | Ketika field size diubah, hamburan dari kepala linac dan kontaminasi elektron ikut berubah, sehingga kualitas berkas dan dosis juga berubah. Data phase space IAEA mencatat setiap partikel, jadi kita bisa menelitinya. Ada tiga pertanyaan riset: RQ1 tentang kualitas berkas, RQ2 tentang akurasi klasifikasi ML, dan RQ3 tentang ciri yang paling berpengaruh serta kaitannya dengan dosis. |
| 3. Sumber data | 0:50 | Data berasal dari IAEA Phase-space Database untuk Varian Clinac 600C 6 MV. Setiap baris berisi satu partikel: jenis, energi, posisi, arah, dan bobot. Labelnya adalah field size. File phase space sangat besar sehingga dipakai sub-sampel. |
| 4. Metode | 1:00 | Metodenya lima tahap: membaca phase space dengan Python, membuat fitur (energi, jarak radial, sudut, jenis partikel), klasifikasi field size dengan RF, SVM, Naive Bayes, dan KNN memakai 10-fold CV, evaluasi dengan accuracy, precision, recall, F1, dan feature importance, lalu menghitung indikator kualitas berkas. Dosis Monte Carlo menjadi target tambahan. |
| 5. Waktu | 0:40 | Estimasinya 4 minggu. Minggu 1: data dan reader. Minggu 2: fitur dan klasifikasi. Minggu 2–3: kualitas berkas. Dosis Monte Carlo opsional. Minggu 4: menyiapkan keempat luaran. |
| 6. Luaran & tim | 0:30 | Luarannya ada empat: cerita Medium, video YouTube, kode di Gist, dan slide di OSF. Setiap anggota tim bertanggung jawab atas satu luaran. |
| 7. Penutup | 0:30 | Hasil yang diharapkan: peta pengaruh field size pada kualitas berkas, model ML yang mengenali field size beserta fitur pentingnya, dan pipeline Python terbuka. Terima kasih, saya terbuka untuk pertanyaan dan masukan. |
| **Total** | **≈ 4:40** | |
