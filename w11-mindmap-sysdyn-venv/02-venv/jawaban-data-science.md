# Jawaban Assignment — Data Science and Python venv

Slide: `data_science_and_python_env.pdf` (https://osf.io/tzvsw), hlm. 32–33.

**NIM:** [NIM]

## 1. Penjelasan singkat tentang data science
Data science adalah proses ilmiah untuk **mengubah data menjadi wawasan (insight)** agar keputusan yang diambil lebih baik. Tujuannya adalah *turning data into actionable value*.
Data science tidak berdiri sendiri. Bidang ini merupakan irisan dari matematika/statistika, ilmu komputer/pemrograman, dan pengetahuan domain (diagram Venn di slide 4).

## 2. Perbedaan data, data science, dan data scientist
| | Arti | Contoh |
|---|---|---|
| **Data** | fakta mentah (angka, teks, gambar, sinyal) yang belum diolah | tabel ukuran bunga Iris, log sensor |
| **Data science** | bidang atau proses ilmiah yang mengolah data menjadi insight dan keputusan | eksplorasi, pembersihan, pemodelan, dan pelaporan data Iris |
| **Data scientist** | orang yang menjalankan proses data science | orang yang mengumpulkan data → mengeksplorasi → membersihkan → menganalisis/membuat model → menarik kesimpulan → melaporkan ke pemangku kepentingan |

Analisis/pemodelan hanyalah **satu** dari enam langkah kerja seorang data scientist (slide 6–7).

## 3. Empat aspek dasar data science
1. **Mathematics**: fungsi, relasi, asumsi, kesimpulan, abstraksi; juga statistika, graf (analisis jejaring sosial), matriks, dan supervised machine learning.
2. **Technology**: Python tingkat lanjut (manipulasi tabel, pembersihan data), *computational notebook* (Jupyter), serta GitHub untuk version control dan publikasi proyek.
3. **Visualization**: memilih jenis plot yang tepat sesuai tipe data dan pesan yang ingin disampaikan, prinsip kapan dan bagaimana memakai visualisasi, serta dashboard interaktif online.
4. **Communication**: komentar dan dokumentasi kode, motivasi dan interpretasi hasil di notebook, serta laporan teknis yang jelas, ringkas, dan sesuai audiens.

## 4. Link PyPI
| Paket | Link | Perintah |
|---|---|---|
| Jupyter Notebook | https://pypi.org/project/notebook/ | `pip install notebook` |
| Matplotlib | https://pypi.org/project/matplotlib/ | `pip install matplotlib` |
| NumPy | https://pypi.org/project/numpy/ | `pip install numpy` |

## 5. Virtual environment → requirements.txt → virtual environment kedua
Seluruh perintah dan outputnya ada di [`venv_log.txt`](venv_log.txt). Ringkasnya (Windows, Python 3.11.9):

```
python -m venv %USERPROFILE%\.venvs\sk5004-w11-a                 # venv pertama
%USERPROFILE%\.venvs\sk5004-w11-a\Scripts\activate
python -m pip install numpy pandas matplotlib scikit-learn notebook
python -m pip freeze > requirements.txt                          # simpan daftar paket
deactivate

python -m venv %USERPROFILE%\.venvs\sk5004-w11-b                 # venv kedua
%USERPROFILE%\.venvs\sk5004-w11-b\Scripts\activate
python -m pip install -r requirements.txt                        # pasang dari requirements.txt
python -m pip freeze                                             # hasilnya identik dengan requirements.txt
```

> Assignment meminta **screenshot** setiap proses. Log teks sudah tersedia di `venv_log.txt`. Untuk screenshot, jalankan ulang perintah di atas di terminal Anda sendiri lalu ambil tangkapan layarnya.

## 6. Modul `statistics` (slide 24–28)
Jalankan `python statistics_module.py`. Hasilnya:

```
dataset       mean  median    mode   multimode   stdev
dataset_1    5.000       5       5         [5]   2.693
dataset_2    8.333       5       5         [5]   9.206
dataset_3    5.333       6       3         [3]   1.936

Catatan:
- dataset_1 dan dataset_2 punya median dan modus sama (5), tetapi mean dataset_2
  jauh lebih besar karena outlier 18 dan 29. Median lebih tahan terhadap outlier.
- dataset_3: angka 3 muncul 3x, sedangkan 6 dan 7 masing-masing 2x, jadi modusnya 3.
  Datanya menumpuk di nilai kecil, sehingga mean (5.333) dan median (6) berbeda.
```
