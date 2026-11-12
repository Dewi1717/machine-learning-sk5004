"""
Pipeline RBL: klasifikasi field size dari data phase space + indikator kualitas berkas.

Pemakaian:
    python pipeline.py ../data_synthetic          # uji dengan data sintetis
    python pipeline.py <folder berisi file IAEA>  # data asli (nama file harus memuat "<n>x<n>")

Tahap:
  1. baca semua *.IAEAheader, ambil field size dari nama file
  2. indikator kualitas berkas per field size: komposisi partikel, energi rata-rata
     (berbobot), spektrum, energi rata-rata vs radius (off-axis softening)
  3. klasifikasi PER PARTIKEL (RF, SVM, NB, KNN; 10-fold stratified CV)
  4. klasifikasi PER KELOMPOK partikel (histogram fitur dari 500 partikel)
"""
import re
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

sys.path.insert(0, str(Path(__file__).parent))
from iaea_phsp import read_phsp

DATA = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "data_synthetic")
OUT = Path(__file__).parent.parent / "output"
OUT.mkdir(exist_ok=True)
SYNTH = "synthetic" in str(DATA).lower()
TAG = " (DATA SINTETIS)" if SYNTH else ""
rng = np.random.default_rng(0)


def head(t):
    print("\n" + "=" * 74 + f"\n{t}\n" + "=" * 74)


# ---------------------------------------------------------------------------
# 1. Baca data
# ---------------------------------------------------------------------------
head(f"1. MEMBACA PHASE SPACE dari {DATA.name}{TAG}")
frames = []
for hdr in sorted(DATA.glob("*.IAEAheader")):
    m = re.search(r"(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)", hdr.stem)
    if not m:
        print(f"  lewati {hdr.name}: field size tidak ada di nama file")
        continue
    fs = float(m.group(1))
    t0 = time.time()
    d = read_phsp(hdr)
    r = np.hypot(d["x"], d["y"])
    df = pd.DataFrame({
        "fs": fs, "type": d["type"], "E": d["E"], "x": d["x"], "y": d["y"], "r": r,
        "theta_deg": np.degrees(np.arccos(np.clip(np.abs(d["w"]), 0, 1))),
        # selisih arah aktual vs arah dari sumber titik: besar untuk partikel terhambur
        "radial_mismatch_deg": np.degrees(np.arccos(np.clip(np.abs(d["w"]), 0, 1)))
                               - np.degrees(np.arctan(r / np.abs(d["z"]))),
        "weight": d["weight"],
    })
    frames.append(df)
    print(f"  {hdr.name}: {len(df):,} partikel, field size {fs:g} cm, {time.time()-t0:.2f} s")
data = pd.concat(frames, ignore_index=True)
FS = sorted(data["fs"].unique())

# ---------------------------------------------------------------------------
# 2. Indikator kualitas berkas
# ---------------------------------------------------------------------------
head("2. INDIKATOR KUALITAS BERKAS PER FIELD SIZE" + TAG)
rows = []
for fs in FS:
    s = data[data.fs == fs]
    ph = s[s.type == 1]
    wsum = s.weight.sum()
    core = ph[ph.r < 1.0]   # dekat sumbu
    rows.append({
        "field_size_cm": fs,
        "foton_%": 100 * s[s.type == 1].weight.sum() / wsum,
        "elektron_%": 100 * s[s.type == 2].weight.sum() / wsum,
        "positron_%": 100 * s[s.type == 3].weight.sum() / wsum,
        "E_mean_foton_MeV": np.average(ph.E, weights=ph.weight),
        "E_mean_foton_r<1cm": np.average(core.E, weights=core.weight),
        "foton_terhambur_%": 100 * np.mean(ph.radial_mismatch_deg > 2.0),
    })
bq = pd.DataFrame(rows)
print(bq.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
bq.to_csv(OUT / "beam_quality.csv", index=False)

fig, axes = plt.subplots(1, 3, figsize=(17, 4.6))
bins = np.linspace(0, 6, 61)
for fs in FS:
    ph = data[(data.fs == fs) & (data.type == 1)]
    h, _ = np.histogram(ph.E, bins=bins, weights=ph.weight, density=True)
    axes[0].step(bins[:-1], h, where="post", label=f"{fs:g}×{fs:g} cm²")
    rb = np.linspace(0, ph.r.quantile(0.995), 15)
    idx = np.digitize(ph.r, rb)
    em = [ph.E[idx == k].mean() if np.any(idx == k) else np.nan for k in range(1, len(rb))]
    axes[1].plot(0.5 * (rb[1:] + rb[:-1]), em, "o-", ms=3, label=f"{fs:g}×{fs:g}")
axes[0].set(title="Spektrum energi foton", xlabel="E (MeV)", ylabel="densitas")
axes[1].set(title="Energi rata-rata vs radius (off-axis)", xlabel="r di bidang phsp (cm)", ylabel="E rata-rata (MeV)")
axes[2].bar([f"{f:g}" for f in FS], bq["foton_terhambur_%"], color="#1F7A8C", label="foton terhambur")
axes[2].bar([f"{f:g}" for f in FS], bq["elektron_%"], bottom=bq["foton_terhambur_%"], color="#F2A541", label="elektron")
axes[2].set(title="Komponen non-primer (%)", xlabel="field size (cm)")
for ax in axes[:2]:
    ax.legend()
axes[2].legend()
fig.suptitle("Kualitas berkas" + TAG)
fig.tight_layout(); fig.savefig(OUT / "01_beam_quality.png", dpi=120); plt.close(fig)

# ---------------------------------------------------------------------------
# 3. Klasifikasi per partikel
# ---------------------------------------------------------------------------
head("3. KLASIFIKASI FIELD SIZE PER PARTIKEL (10-fold stratified CV)" + TAG)
FEAT = ["E", "r", "theta_deg", "radial_mismatch_deg", "type"]
N_CLS = 5000
sub = pd.concat([data[data.fs == fs].sample(N_CLS, random_state=1) for fs in FS])
X, y = sub[FEAT].values, sub["fs"].astype(int).astype(str).values
models = {
    "RF": RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=0),
    "SVM": make_pipeline(StandardScaler(), SVC(gamma="scale")),
    "NB": GaussianNB(),
    "KNN": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=15)),
}
cv = StratifiedKFold(10, shuffle=True, random_state=0)
res = []
preds = {}
for name, mdl in models.items():
    t0 = time.time()
    p = cross_val_predict(mdl, X, y, cv=cv, n_jobs=1)
    preds[name] = p
    res.append({"model": name, "accuracy": accuracy_score(y, p),
                "macro_F1": f1_score(y, p, average="macro"), "waktu_s": time.time() - t0})
res = pd.DataFrame(res)
print(res.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
labels = [str(int(f)) for f in FS]
best = res.sort_values("accuracy").iloc[-1]["model"]
print(f"\nConfusion matrix {best} (baris = aktual, kolom = prediksi) {labels}:")
print(confusion_matrix(y, preds[best], labels=labels))

rf = RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=0).fit(X, y)
imp = pd.Series(rf.feature_importances_, index=FEAT).sort_values(ascending=False)
print("\nFeature importance (RF):")
print(imp.round(3).to_string())

# akurasi per wilayah radius: partikel dekat sumbu sulit dibedakan
sub = sub.assign(pred=preds[best], ok=lambda d: d.pred == d.fs.astype(int).astype(str))
half5 = 0.5 * min(FS) * 30 / 100
inner = sub[sub.r < half5]
outer = sub[sub.r >= half5]
print(f"\nRecall per kelas ({best}) untuk partikel dekat sumbu (r < {half5:.2f} cm, "
      f"di dalam proyeksi lapangan terkecil):")
inner_recall = inner.groupby(inner.fs.astype(int).astype(str))["ok"].mean().reindex(labels)
for lab, v in inner_recall.items():
    print(f"   {lab:>3} cm: recall = {v:.3f}  (n={int((inner.fs.astype(int).astype(str) == lab).sum())})")
print("   -> dekat sumbu, partikel dari lapangan berbeda hampir identik; model cenderung "
      "menebak lapangan terkecil karena kerapatan partikelnya paling tinggi.")

# ---------------------------------------------------------------------------
# 4. Klasifikasi per kelompok partikel (bag of 500)
# ---------------------------------------------------------------------------
head("4. KLASIFIKASI PER KELOMPOK 500 PARTIKEL (fitur histogram)" + TAG)
BAG = 500
edges = {"E": np.linspace(0, 6, 13), "r": np.linspace(0, 3.5, 15), "theta_deg": np.linspace(0, 8, 9)}
Xb, yb = [], []
for fs in FS:
    s = data[data.fs == fs].sample(frac=1, random_state=2)
    for k in range(min(200, len(s) // BAG)):
        b = s.iloc[k * BAG:(k + 1) * BAG]
        f = np.concatenate([np.histogram(b[c], bins=e)[0] / BAG for c, e in edges.items()]
                           + [[np.mean(b.type == 2), np.mean(b.radial_mismatch_deg > 2)]])
        Xb.append(f); yb.append(str(int(fs)))
Xb, yb = np.array(Xb), np.array(yb)
pb = cross_val_predict(RandomForestClassifier(n_estimators=200, random_state=0), Xb, yb, cv=cv)
print(f"{len(yb)} kelompok, RF accuracy = {accuracy_score(yb, pb):.4f}")
print(confusion_matrix(yb, pb, labels=labels))

# Gambar ringkas klasifikasi
fig, axes = plt.subplots(1, 3, figsize=(16, 4.4))
axes[0].bar(res.model, res.accuracy, color=["#0B2A3C", "#1F7A8C", "#5FA8B8", "#8AA29E"])
axes[0].axhline(1 / len(FS), ls="--", color="gray", label="tebakan acak")
axes[0].set(ylim=(0, 1), title="Akurasi per partikel (10-fold CV)"); axes[0].legend()
for i, v in enumerate(res.accuracy):
    axes[0].text(i, v + 0.02, f"{v:.2f}", ha="center")
axes[1].barh(imp.index[::-1], imp.values[::-1], color="#F2A541")
axes[1].set_title("Feature importance (RF)")
bar_lab = [f"{l}×{l}" for l in labels] + ["kelompok\n500"]
axes[2].bar(bar_lab, list(inner_recall.values) + [accuracy_score(yb, pb)],
            color=["#5FA8B8"] * len(labels) + ["#0B2A3C"])
axes[2].set(ylim=(0, 1.05), title="Recall dekat sumbu per kelas vs akurasi per kelompok")
fig.suptitle("Klasifikasi field size" + TAG)
fig.tight_layout(); fig.savefig(OUT / "02_classification.png", dpi=120); plt.close(fig)

res.to_csv(OUT / "classification_per_particle.csv", index=False)
print(f"\nOutput di {OUT}")
