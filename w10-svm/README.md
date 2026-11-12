# Assignment w10 — Intro to Support Vector Machine

Sumber: https://github.com/dudung/sk5004-01-2024-2/issues/2

## Instruksi
1. Pelajari slide [pzqf9](https://osf.io/pzqf9) (`13_svm_short_intro.pdf`).
2. Laporkan NIM, nama, dan bukti bahwa tugas sudah dikerjakan.

Tugas yang harus dikerjakan ada di slide 72 (*Challenges*):
1. Jalankan kode DataCamp secara online.
2. Jika berhasil, jalankan secara lokal (tantangan instalasi Python dan paket).
3. Cari cara membuat dan memakai virtual environment.

## Isi folder
| File | Isi |
|---|---|
| slide kuliah | tidak disertakan di repo (hak cipta dosen), unduh di https://osf.io/pzqf9 |
| `ringkasan-slide.md` | ringkasan materi dalam bahasa Indonesia + hasil |
| `svm_datacamp.py` | kode DataCamp (bagian A) + tuning (B) + ilustrasi margin/kernel (C) |
| `panduan-virtual-environment.md` | jawaban challenge 3: cara membuat dan memakai venv |
| `requirements.txt` | daftar paket di venv (untuk dibuat ulang) |
| `output/` | log hasil run dan 3 gambar |
| `komentar-issue-2.md` | draf laporan untuk issue #2 |

## Menjalankan
```
& "$env:USERPROFILE\.venvs\sk5004-svm\Scripts\Activate.ps1"
python svm_datacamp.py
```

## Checklist
- [x] Slide diunduh dan diringkas
- [ ] Challenge 1: jalankan kode di DataCamp DataLab (butuh akun DataCamp, dikerjakan sendiri)
      → buka https://www.datacamp.com/tutorial/svm-classification-scikit-learn-python, klik "Run code", lalu salin link workbook-nya
- [x] Challenge 2: kode berjalan lokal (Accuracy 0.9649, sama dengan DataCamp)
- [x] Challenge 3: venv dibuat (`%USERPROFILE%\.venvs\sk5004-svm`) + panduan
- [ ] Unggah file folder ini ke GitHub Anda (opsional, seperti teman-teman lain)
- [ ] Kirim laporan ke issue #2 (draf di `komentar-issue-2.md`)
