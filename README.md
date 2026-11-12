# SK5004 Machine Learning and Artificial Intelligence — Tugas w09–w15

Kumpulan pengerjaan tugas mingguan mata kuliah **SK5004 Machine Learning and Artificial Intelligence** (Institut Teknologi Bandung).
Instruksi setiap tugas berasal dari issue di [dudung/sk5004-01-2024-2](https://github.com/dudung/sk5004-01-2024-2/issues).

**Nama:** [NAMA LENGKAP] · **NIM:** [NIM]

## Daftar tugas

| Minggu | Topik | Issue | Isi utama |
|---|---|---|---|
| [w09](w09-random-forest/) | Pengantar Random Forest | [#1](https://github.com/dudung/sk5004-01-2024-2/issues/1) | ringkasan slide; Decision Tree vs Random Forest pada dataset golf (akurasi uji 42,9% → 64,3%) |
| [w10](w10-svm/) | Pengantar Support Vector Machine | [#2](https://github.com/dudung/sk5004-01-2024-2/issues/2) | kode SVM DataCamp dijalankan lokal (accuracy 0,9649), tuning kernel/C/gamma, panduan virtual environment |
| [w11](w11-mindmap-sysdyn-venv/) | Mind & concept map, system dynamics, venv, Python untuk ML | [#3](https://github.com/dudung/sk5004-01-2024-2/issues/3) | mind map & concept map ide riset (Mermaid); venv → requirements.txt → venv kedua; Iris dengan 6 algoritma + metrik manual vs sklearn; model system dynamics |
| [w12](w12-genetic-algorithm/) | Genetic Algorithm | [#4](https://github.com/dudung/sk5004-01-2024-2/issues/4) | dua contoh GA yang diuji (curve fitting, rute 15 toko); draf feedback slide |
| [w13](w13-quiz-genetic-algorithm/) | Kuis Genetic Algorithm | [#5](https://github.com/dudung/sk5004-01-2024-2/issues/5) | rangkuman + 12 soal latihan dengan pembahasan |
| [w14](w14-pitching-rbl/) | Pitching ide RBL | [#6](https://github.com/dudung/sk5004-01-2024-2/issues/6) | deck pitching 7 slide + naskah; detail proyek |
| [w15](w15-rbl-final/) | RBL final (progres) | [#7](https://github.com/dudung/sk5004-01-2024-2/issues/7) | reader format phase space IAEA, pipeline klasifikasi field size + kualitas berkas, deck progres 8 slide |

Setiap folder punya `README.md` sendiri (instruksi, isi folder, checklist) dan `komentar-issue-N.md` (draf laporan untuk issue).

## Proyek RBL

**Klasifikasi Data Phase Space IAEA untuk Menilai Pengaruh Variasi Field Size terhadap Kualitas Berkas X-Ray dan Dosis Serap pada Varian Clinac 600C 6 MV**

Alurnya: ide riset (w11, mind map & concept map) → pitching (w14) → progres (w15).
Hasil di w15 masih berasal dari **data phase space sintetis** untuk menguji pipeline, sehingga **belum** menjadi hasil riset. Lihat [w15-rbl-final/README.md](w15-rbl-final/README.md).

## Menjalankan kode

Python 3.11 (diuji dengan 3.11.9):

```
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

| Skrip | Perintah (dari folder root) |
|---|---|
| w09 Random Forest | `python w09-random-forest/random_forest_golf.py` |
| w10 SVM | `python w10-svm/svm_datacamp.py` |
| w11 Iris 6 algoritma | `python w11-mindmap-sysdyn-venv/03-python-ml/iris_six_algorithms.py` |
| w11 system dynamics | `python w11-mindmap-sysdyn-venv/04-system-dynamics/sd_coal_mining_toy.py` |
| w11 modul statistics | `python w11-mindmap-sysdyn-venv/02-venv/statistics_module.py` |
| w12 Genetic Algorithm | `python w12-genetic-algorithm/ga_examples.py` |
| w15 data sintetis | `python w15-rbl-final/code/make_synthetic_phsp.py` |
| w15 pipeline | `python w15-rbl-final/code/pipeline.py w15-rbl-final/data_synthetic` |

Setiap skrip menyimpan gambar dan log ke folder `output/` di sebelahnya.

Deck presentasi (w14, w15) dibuat dengan [pptxgenjs](https://gitbrent.github.io/PptxGenJS/) (Node.js):

```
npm install
npm run deck:w14
npm run deck:w15
```

## Yang tidak disertakan di repo
- **Slide kuliah dosen** (hak cipta Sparisoma Viridi). Tautan OSF-nya ada di README setiap minggu.
- **Data phase space sintetis w15** (22,5 MB). Buat ulang dengan `make_synthetic_phsp.py`.
- `node_modules/`, virtual environment, dan file sementara (lihat `.gitignore`).

## Struktur
```
.
├── README.md
├── requirements.txt          # paket Python
├── package.json              # pptxgenjs untuk deck
├── tools/apply_theme.js      # helper warna & font tema deck
├── w09-random-forest/
├── w10-svm/
├── w11-mindmap-sysdyn-venv/
│   ├── 01-mindmap-conceptmap/
│   ├── 02-venv/
│   ├── 03-python-ml/
│   └── 04-system-dynamics/
├── w12-genetic-algorithm/
├── w13-quiz-genetic-algorithm/
├── w14-pitching-rbl/
└── w15-rbl-final/
    ├── code/
    └── output/
```
