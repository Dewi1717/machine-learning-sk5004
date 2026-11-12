# Assignment w11 — Mind & concept maps, system dynamics, virtual environment, hands-on

Sumber: https://github.com/dudung/sk5004-01-2024-2/issues/3

## Instruksi
1. Pelajari 4 slide: [mind map & concept map](https://osf.io/9qkvc), [system dynamics](https://osf.io/z5vn2), [data science & python venv](https://osf.io/tzvsw), [practicing python for ML](https://osf.io/k8b7q).
2. Tulis NIM dan nama.
3. Nyatakan untuk setiap slide bahwa Anda sudah mempelajarinya.

Setiap slide punya tugas atau *challenge* sendiri, dan semuanya dikerjakan di subfolder masing-masing.

## Isi folder
| Folder / file | Isi | Hasil utama |
|---|---|---|
| slide kuliah | tidak disertakan di repo (hak cipta dosen), lihat 4 link OSF di atas | — |
| `ringkasan-slide.md` | ringkasan keempat slide dalam bahasa Indonesia | — |
| `01-mindmap-conceptmap/` | mind map + concept map (Mermaid) untuk topik riset phase space IAEA Clinac 600C 6 MV; `preview.html` untuk melihat diagramnya | 3 pertanyaan riset + perbandingan kedua alat |
| `02-venv/` | jawaban soal data science, link PyPI, log venv → `requirements.txt` → venv kedua, contoh modul `statistics` | venv kedua **identik** (107 paket) |
| `03-python-ml/` | Iris dengan 6 algoritma + challenge metrik manual vs sklearn | SVM CV 0.9833; manual = sklearn (selisih 1e-16) |
| `04-system-dynamics/` | model SD mainan (stock-flow) area tambang batubara | grafik 3 skenario investasi lingkungan |
| `komentar-issue-3.md` | draf laporan untuk issue #3 | — |

## Menjalankan kode
Pakai venv yang sudah dibuat:
```
& "$env:USERPROFILE\.venvs\sk5004-w11-a\Scripts\Activate.ps1"
python 03-python-ml\iris_six_algorithms.py
python 04-system-dynamics\sd_coal_mining_toy.py
python 02-venv\statistics_module.py
```

## Checklist
- [x] 4 slide diunduh dan diringkas
- [x] Mind map dan concept map ide riset + pertanyaan riset
- [x] Jawaban data science + link PyPI
- [x] venv → requirements.txt → venv kedua (log di `02-venv/venv_log.txt`)
- [ ] **Screenshot** proses venv (diminta slide; ambil sendiri di terminal Anda)
- [ ] Cek ukuran lapangan yang tersedia di database IAEA untuk Clinac 600C, lalu sesuaikan mind map
- [x] Challenge Iris: tabel 6 algoritma × 3 kelas, metrik manual vs sklearn
- [x] Latihan system dynamics
- [ ] Isi NIM di `02-venv/jawaban-data-science.md`
- [ ] Unggah folder ini ke GitHub, lalu kirim laporan ke issue #3 (draf di `komentar-issue-3.md`)
