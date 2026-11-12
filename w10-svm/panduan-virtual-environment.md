# Panduan Virtual Environment untuk scikit-learn (Windows)

Jawaban untuk *challenge* ketiga di slide 72: *"Find information how to create and use virtual environment, that might be helpful to scikit-learn."*

## Apa itu virtual environment?
Virtual environment (venv) adalah folder berisi **salinan interpreter Python beserta paket-paketnya**, terpisah dari Python utama di sistem.

Kegunaannya:
- Setiap proyek bisa memakai versi paket yang berbeda tanpa saling bentrok. Contohnya, proyek A memakai scikit-learn 1.3 dan proyek B memakai 1.9.
- Paket tidak dipasang ke Python sistem, sehingga sistem tetap bersih.
- Lingkungan mudah dibuat ulang di komputer lain lewat `requirements.txt`.

## Langkah yang dipakai untuk tugas ini

### 1. Buat venv
Di PowerShell atau Command Prompt:
```
python -m venv %USERPROFILE%\.venvs\sk5004-svm
```
Venv sengaja **diletakkan di luar folder OneDrive** (`C:\Users\<nama>\.venvs\`). Isinya ribuan file, dan kalau ikut tersinkron OneDrive, sinkronisasinya jadi berat.
Pilihan lain yang umum adalah membuat folder `.venv` di dalam folder proyek: `python -m venv .venv`.

### 2. Aktifkan venv
| Shell | Perintah |
|---|---|
| PowerShell | `& "$env:USERPROFILE\.venvs\sk5004-svm\Scripts\Activate.ps1"` |
| Command Prompt | `%USERPROFILE%\.venvs\sk5004-svm\Scripts\activate.bat` |
| Git Bash | `source ~/.venvs/sk5004-svm/Scripts/activate` |
| Linux / macOS | `source ~/.venvs/sk5004-svm/bin/activate` |

Setelah aktif, prompt terminal diawali `(sk5004-svm)`.
Kalau PowerShell menolak menjalankan skrip, jalankan sekali saja: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### 3. Pasang paket
```
python -m pip install --upgrade pip
python -m pip install scikit-learn matplotlib
```
scikit-learn otomatis memasang numpy, scipy, joblib, dan threadpoolctl.

### 4. Cek bahwa venv yang dipakai
```
python -c "import sys, sklearn; print(sys.executable); print(sklearn.__version__)"
```
Path yang tercetak harus berada di dalam folder `.venvs\sk5004-svm`.
Di tugas ini hasilnya `C:\Users\...\.venvs\sk5004-svm\Scripts\python.exe` dan scikit-learn **1.9.1**.

### 5. Jalankan kode
```
python svm_datacamp.py
```

### 6. Simpan daftar paket agar bisa dibuat ulang
```
python -m pip freeze > requirements.txt
```
Di komputer lain cukup jalankan: `python -m venv .venv`, aktifkan venv, lalu `pip install -r requirements.txt`.

### 7. Keluar dari venv / menghapusnya
```
deactivate
```
Untuk menghapus venv, cukup hapus foldernya.

## Alternatif
- **conda** (Anaconda/Miniconda): `conda create -n sk5004 python=3.11 scikit-learn` lalu `conda activate sk5004`. Cocok kalau butuh paket non-Python.
- **uv**: `uv venv` lalu `uv pip install scikit-learn`. Hasilnya sama dengan venv, tetapi pemasangan paketnya jauh lebih cepat.
- **VS Code**: `Ctrl+Shift+P` → *Python: Select Interpreter* → pilih `python.exe` di folder venv.
- **Jupyter**: setelah venv aktif, jalankan `pip install ipykernel` lalu `python -m ipykernel install --user --name sk5004-svm`. Kernel venv itu kemudian bisa dipilih di notebook.

## Masalah umum saat instalasi lokal (dan solusinya)
| Masalah | Solusi |
|---|---|
| `ModuleNotFoundError: No module named 'sklearn'` | Paketnya bernama `scikit-learn` (bukan `sklearn`) saat install. Pastikan juga venv sudah aktif. |
| Ada beberapa Python di sistem, `pip` memasang ke Python yang salah | Selalu pakai `python -m pip ...`, bukan `pip ...` |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Error kompilasi saat install | Pakai Python versi yang didukung (3.10–3.13) supaya pip mengunduh *wheel* jadi, tanpa perlu kompilasi. |
