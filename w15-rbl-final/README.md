# Assignment w15 — RBL Final Presentation (progres proyek)

Sumber: https://github.com/dudung/sk5004-01-2024-2/issues/7

## Instruksi
Presentasi progres 5 menit, berisi:
- **Tim:** nama semua anggota
- **Ringkasan:** sumber data, metode, kategori ML, estimasi waktu
- **Isi:** definisi masalah, usulan solusi, diskusi (temuan awal, tantangan, keputusan), pemahaman
- **Pembagian tugas:** Medium story, YouTube video, Gist code, OSF slides

Setelah presentasi, kirim semua informasi di atas **sebagai komentar** di issue #7 (tanpa link atau lampiran).

## Isi folder
| File / folder | Isi |
|---|---|
| `rbl-final-progres.pptx` / `.pdf` | deck 8 slide + speaker notes (±5 menit) |
| `komentar-issue-7.md` | draf komentar lengkap untuk issue #7 (dengan diagram Mermaid) |
| `code/iaea_phsp.py` | reader + writer format phase space IAEA |
| `code/make_synthetic_phsp.py` | pembuat phase space **sintetis** untuk uji pipeline |
| `code/pipeline.py` | klasifikasi field size + indikator kualitas berkas |
| `data_synthetic/` | 3 file phase space sintetis (5×5, 10×10, 20×20 cm²), masing-masing 300 ribu partikel. **Tidak ada di repo** (22,5 MB); buat ulang dengan `python code/make_synthetic_phsp.py` |
| `output/` | log, CSV, dan 2 gambar hasil pipeline |
| `build_deck.js` | skrip pembuat deck (membaca angka dari `output/`); dari folder root: `npm install && npm run deck:w15` |

## ⚠️ Tentang data sintetis
Data asli IAEA belum bisa diunduh: situsnya memakai proteksi bot dan ukuran filenya GB. Karena itu pipeline diuji dengan phase space **sintetis** buatan sendiri (model mainan: foton primer + hamburan kepala + elektron kontaminan + pelunakan off-axis). Semua angka di deck diberi label **DATA SINTETIS** dan **bukan** hasil riset.

## Menjalankan dengan data asli
1. Unduh file phase space Clinac 600C 6 MV dari IAEA (`.IAEAheader` + `.IAEAphsp`) ke satu folder.
2. Pastikan nama file memuat field size, mis. `..._10x10.IAEAheader`.
3. Jalankan:
```
& "$env:USERPROFILE\.venvs\sk5004-w11-a\Scripts\Activate.ps1"
python code\pipeline.py <folder data asli>
```
Jika header IAEA asli menyimpan Z atau extra float/long, reader akan menyesuaikan diri lewat `$RECORD_CONTENTS` dan memeriksa `$RECORD_LENGTH`.

## Checklist
- [x] Reader IAEA (uji round-trip lolos)
- [x] Pipeline klasifikasi + kualitas berkas (diuji dengan data sintetis)
- [x] Deck progres + PDF + draf komentar
- [ ] Isi nama/NIM tim di slide 1, slide 8, dan `komentar-issue-7.md`
- [ ] Unduh data asli IAEA dan jalankan ulang pipeline
- [ ] Presentasi, lalu kirim komentar ke issue #7
