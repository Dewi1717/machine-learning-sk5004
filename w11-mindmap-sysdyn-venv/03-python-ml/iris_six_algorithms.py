"""
Assignment w11 - Practicing Python for ML (slide k8b7q / gv8h5)

Alur mengikuti slide (contoh "Your First Machine Learning Project in Python"):
  1. muat dataset Iris, cek ukuran, 10 baris pertama, ringkasan statistik, distribusi kelas
  2. visualisasi: box-whisker, histogram, scatter matrix
  3. split 80/20 (random_state=1), 6 algoritma dengan 10-fold stratified CV
  4. prediksi validation set dengan SVM dan juga dengan kelima algoritma lainnya

Challenge (slide 49):
  a. tabel hasil LR, LDA, KNN, CART, NB, SVM untuk Iris-setosa, Iris-versicolor, Iris-virginica
  b. hitung accuracy, precision, recall, F1 secara MANUAL dari TP/TN/FP/FN
     (kelas A vs gabungan non-A), lalu bandingkan dengan sklearn.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
from sklearn.datasets import load_iris
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)
pd.set_option("display.width", 120)


def header(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# ---------------------------------------------------------------------------
# 1. Load data (dataset sama dengan iris.csv di slide; diambil dari sklearn
#    agar tidak perlu unduh)
# ---------------------------------------------------------------------------
iris = load_iris()
names = ["sepal-length", "sepal-width", "petal-length", "petal-width"]
dataset = pd.DataFrame(iris.data, columns=names)
dataset["class"] = ["Iris-" + iris.target_names[t] for t in iris.target]

header("1. DATASET")
print("shape:", dataset.shape)
print(dataset.head(10))
print(dataset.describe())
print(dataset.groupby("class").size())

# ---------------------------------------------------------------------------
# 2. Visualisasi
# ---------------------------------------------------------------------------
dataset.plot(kind="box", subplots=True, layout=(2, 2), sharex=False, sharey=False,
             figsize=(8, 6), title="Box and whisker")
plt.tight_layout(); plt.savefig(OUT / "01_box_whisker.png", dpi=110); plt.close("all")
dataset.hist(figsize=(8, 6))
plt.tight_layout(); plt.savefig(OUT / "02_histogram.png", dpi=110); plt.close("all")
colors = dataset["class"].map({"Iris-setosa": "tab:blue", "Iris-versicolor": "tab:orange",
                               "Iris-virginica": "tab:green"})
scatter_matrix(dataset[names], figsize=(9, 9), c=colors, alpha=0.8)
plt.suptitle("Scatter matrix (biru=setosa, oranye=versicolor, hijau=virginica)")
plt.savefig(OUT / "03_scatter_matrix.png", dpi=110); plt.close("all")

# ---------------------------------------------------------------------------
# 3. Split dan 10-fold CV untuk 6 algoritma
# ---------------------------------------------------------------------------
X = dataset[names].values
y = dataset["class"].values
X_train, X_validation, Y_train, Y_validation = train_test_split(
    X, y, test_size=0.20, random_state=1)

models = [
    ("LR", LogisticRegression(max_iter=1000)),
    ("LDA", LinearDiscriminantAnalysis()),
    ("KNN", KNeighborsClassifier()),
    ("CART", DecisionTreeClassifier(random_state=1)),
    ("NB", GaussianNB()),
    ("SVM", SVC(gamma="auto")),
]

header("2. 10-FOLD STRATIFIED CROSS-VALIDATION (data latih 120 sampel)")
results = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
    cv = cross_val_score(model, X_train, Y_train, cv=kfold, scoring="accuracy")
    results.append(cv)
    print(f"{name:<5}: {cv.mean():.6f} ({cv.std():.6f})")

plt.figure(figsize=(7, 4.5))
plt.boxplot(results, tick_labels=[n for n, _ in models])
plt.title("Algorithm Comparison (10-fold CV accuracy)")
plt.tight_layout(); plt.savefig(OUT / "04_algorithm_comparison.png", dpi=110); plt.close("all")

# ---------------------------------------------------------------------------
# 4. Prediksi validation set (30 sampel) dengan SVM (model final di slide)
# ---------------------------------------------------------------------------
header("3. PREDIKSI VALIDATION SET DENGAN SVM")
svm = SVC(gamma="auto").fit(X_train, Y_train)
pred = svm.predict(X_validation)
print("accuracy:", accuracy_score(Y_validation, pred))
print(confusion_matrix(Y_validation, pred))
print(classification_report(Y_validation, pred, digits=4))

# ---------------------------------------------------------------------------
# 5. CHALLENGE: metrik manual one-vs-rest untuk 6 algoritma x 3 kelas
# ---------------------------------------------------------------------------
CLASSES = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]


def manual_metrics(y_true, y_pred, cls):
    """Kelas `cls` = positif, dua kelas lainnya digabung menjadi non-A."""
    t = np.asarray(y_true) == cls
    p = np.asarray(y_pred) == cls
    TP = int(np.sum(t & p))
    TN = int(np.sum(~t & ~p))
    FP = int(np.sum(~t & p))
    FN = int(np.sum(t & ~p))
    acc = (TP + TN) / (TP + TN + FP + FN)
    prec = TP / (TP + FP) if TP + FP else 0.0
    rec = TP / (TP + FN) if TP + FN else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return TP, TN, FP, FN, acc, prec, rec, f1


header("4. CHALLENGE: METRIK MANUAL (one-vs-rest) vs SKLEARN, validation set 30 sampel")
rows = []
for name, model in models:
    yp = model.fit(X_train, Y_train).predict(X_validation)
    # metrik sklearn per kelas (average=None)
    sk_p = precision_score(Y_validation, yp, labels=CLASSES, average=None, zero_division=0)
    sk_r = recall_score(Y_validation, yp, labels=CLASSES, average=None, zero_division=0)
    sk_f = f1_score(Y_validation, yp, labels=CLASSES, average=None, zero_division=0)
    for i, cls in enumerate(CLASSES):
        TP, TN, FP, FN, acc, prec, rec, f1 = manual_metrics(Y_validation, yp, cls)
        # accuracy biner sklearn: ubah ke label A / non-A
        sk_acc = accuracy_score(np.asarray(Y_validation) == cls, np.asarray(yp) == cls)
        rows.append({
            "model": name, "class": cls.replace("Iris-", ""),
            "TP": TP, "TN": TN, "FP": FP, "FN": FN,
            "acc": acc, "prec": prec, "rec": rec, "F1": f1,
            "sk_acc": sk_acc, "sk_prec": sk_p[i], "sk_rec": sk_r[i], "sk_F1": sk_f[i],
        })
    rows.append({"model": name, "class": "(overall)",
                 "acc": accuracy_score(Y_validation, yp),
                 "prec": precision_score(Y_validation, yp, average="macro"),
                 "rec": recall_score(Y_validation, yp, average="macro"),
                 "F1": f1_score(Y_validation, yp, average="macro")})

table = pd.DataFrame(rows)
per_class = table[table["class"] != "(overall)"].copy()
cols_m = ["acc", "prec", "rec", "F1"]
cols_s = ["sk_acc", "sk_prec", "sk_rec", "sk_F1"]
max_diff = np.abs(per_class[cols_m].values - per_class[cols_s].values.astype(float)).max()

print(per_class[["model", "class", "TP", "TN", "FP", "FN"] + cols_m + cols_s]
      .to_string(index=False, float_format=lambda v: f"{v:.4f}",
                 formatters={c: "{:.0f}".format for c in ["TP", "TN", "FP", "FN"]}))
print(f"\nSelisih terbesar manual vs sklearn: {max_diff:.2e}  -> "
      + ("IDENTIK" if max_diff < 1e-12 else "BERBEDA"))

header("5. RINGKASAN PER MODEL (overall accuracy, macro precision/recall/F1)")
overall = table[table["class"] == "(overall)"][["model"] + cols_m]
overall.columns = ["model", "accuracy", "macro_precision", "macro_recall", "macro_F1"]
print(overall.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

table.to_csv(OUT / "challenge_metrics.csv", index=False, float_format="%.6f")

# Tabel markdown untuk laporan
with open(OUT / "challenge_table.md", "w", encoding="utf-8") as f:
    f.write("| Model | Kelas | TP | TN | FP | FN | Accuracy | Precision | Recall | F1 |\n")
    f.write("|---|---|---|---|---|---|---|---|---|---|\n")
    for _, r in per_class.iterrows():
        f.write(f"| {r.model} | {r['class']} | {r.TP:.0f} | {r.TN:.0f} | {r.FP:.0f} | "
                f"{r.FN:.0f} | {r.acc:.4f} | {r.prec:.4f} | {r.rec:.4f} | {r.F1:.4f} |\n")
    f.write(f"\nSelisih terbesar perhitungan manual vs sklearn: {max_diff:.1e}\n\n")
    f.write("| Model | Accuracy | Macro precision | Macro recall | Macro F1 |\n|---|---|---|---|---|\n")
    for _, r in overall.iterrows():
        f.write(f"| {r.model} | {r.accuracy:.4f} | {r.macro_precision:.4f} | "
                f"{r.macro_recall:.4f} | {r.macro_F1:.4f} |\n")

print(f"\nOutput disimpan di {OUT}")
