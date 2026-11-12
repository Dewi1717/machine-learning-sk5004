# Ringkasan 4 Slide — Assignment w11

---

## 1. Mind map and concept map (`07_mind_map_concept_map.pdf`, https://osf.io/9qkvc)
- **Mind map**: alat *brainstorming* visual yang dimulai dari satu ide pusat lalu bercabang ke subtopik. Bentuknya bebas dan non-linear, intuitif, tetapi kurang detail dalam menjelaskan hubungan. Cocok untuk memunculkan ide.
- **Concept map**: graf dengan node berupa konsep dan **panah berlabel** sebagai hubungan. Satu node boleh punya beberapa induk (di mind map hanya satu). Cocok untuk analisis mendalam.
- Alat visual lain yang dibandingkan: *system diagram*, *decision tree*, *flowchart*.
- **Ide riset** bisa datang dari mana saja (pengalaman, materi yang tersedia, minat pribadi), jadi perlu dikumpulkan terus-menerus. **Pertanyaan riset** harus jelas, ringkas, terbuka, dan menentukan ruang lingkup penelitian.
- **Dalam riset:** mind map dipakai untuk menemukan ide, concept map untuk merumuskan pertanyaan riset. Mulailah dengan mind map, lalu ubah menjadi concept map.
- Diagram bisa ditulis dengan **Mermaid** di GitHub issue (`mindmap` dan `graph`). Kelemahannya, arah cabang mindmap diatur otomatis oleh Mermaid dan tidak bisa dikontrol.
- **Tugas:** buat mind map ide riset, buat concept map untuk menghasilkan pertanyaan riset, lalu bandingkan hasil keduanya. → [01-mindmap-conceptmap/](01-mindmap-conceptmap/mindmap-conceptmap-riset.md)

## 2. System dynamics model (`14_sys_dyn_short_intro.pdf`, https://osf.io/z5vn2)
- **System dynamics (SD)** adalah metodologi pemodelan matematis berbasis simulasi dan teori *feedback* untuk membantu pengambilan keputusan dalam sistem yang kompleks dan dinamis (sosial, manajerial, ekonomi, ekologi).
- *Systems thinking* menggambarkan hubungan sebab-akibat antarvariabel, sedangkan SD **mengkuantifikasi** dampak interaksi tersebut.
- **Tantangan** (contoh dari bidang sumber daya air): pengetahuan dan pengalaman pemodel, kebutuhan menggabungkan berbagai aspek, validasi model, dan integrasi subsistem.
- **Validasi**: validitas struktural, perilaku, dan prediktif. Model yang cocok dengan data historis belum tentu akurat untuk memprediksi masa depan.
- **Empat tahap** membangun model SD (Forrester): konseptualisasi, formulasi, pengujian, implementasi.
- **Aplikasi**:
  - simulasi lini pengemasan: pemodelannya cepat, tetapi sulit menelusuri penyebab hilangnya produktivitas
  - kinerja sistem manufaktur
  - *rebound effect* pada ekonomi sirkular
  - manajemen lingkungan di area tambang batubara: punya *causal loop* positif dan negatif serta 5 subsistem (atmosfer, limbah padat, air, tutupan vegetasi, reklamasi lahan); kesimpulannya, pemulihan vegetasi perlu diperkuat
- Slide ini tidak berisi tugas eksplisit. Sebagai latihan, saya buat model SD mainan (stock-flow, integrasi Euler) yang terinspirasi contoh tambang batubara. → [04-system-dynamics/](04-system-dynamics/sd_coal_mining_toy.py)

## 3. Data science and Python venv (`data_science_and_python_env.pdf`, https://osf.io/tzvsw)
- Data science mengubah data menjadi insight yang bisa ditindaklanjuti. Bidang ini tidak berdiri sendiri, melainkan irisan matematika, komputasi, dan pengetahuan domain.
- Alur kerja data scientist: kumpulkan → eksplorasi → bersihkan → analisis/model → simpulkan → laporkan. Analisis hanya satu dari keenam langkah itu.
- Empat aspek dasar: **matematika, teknologi, visualisasi, komunikasi**.
- **Virtual environment**: kemampuan Python memasang paket itu bermata dua, karena dependensi antarproyek bisa bentrok. Solusinya venv, yaitu direktori mandiri berisi versi Python dan paket tertentu. Bisa dibuat dengan `virtualenv` atau modul bawaan `venv` (sejak Python 3.3).
- Contoh modul `statistics` bawaan untuk *central tendency* (mean, median, mode).
- **Tugas:** pertanyaan tentang data science, link PyPI, dan membuat venv → `requirements.txt` → venv kedua. → [02-venv/](02-venv/jawaban-data-science.md)

## 4. Practicing Python for ML (`practicing_python_for_ml.pdf`, https://osf.io/k8b7q)
- Belajar dari internet: pilih mesin pencari yang tepat (Dogpile, Ecosia, Google, DuckDuckGo) dan pakai operator pencarian Google (`" "`, `OR`, `site:`, `filetype:`, `before:`/`after:`, dll.).
- Contoh proyek ML pertama dengan dataset **Iris**:
  - cek library → muat data → shape, `head`, `describe`, distribusi kelas
  - visualisasi univariat (box-whisker, histogram) dan multivariat (scatter matrix)
  - split 80/20, lalu 6 algoritma (**LR, LDA** linear; **KNN, CART, NB, SVM** nonlinear) dengan 10-fold CV
  - SVM terbaik → prediksi validation set → accuracy, confusion matrix, classification report
- Metrik: precision, recall, accuracy, F1-score.
- **Challenge:** buat tabel hasil keenam algoritma untuk ketiga kelas Iris, lalu hitung accuracy/precision/recall/F1 secara manual (kelas A vs non-A) dan bandingkan dengan sklearn. → [03-python-ml/](03-python-ml/iris_six_algorithms.py)
