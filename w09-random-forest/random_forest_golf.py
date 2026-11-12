"""
Assignment w09 - Intro to Random Forest (SK5004)

Reproduksi contoh di slide "12_random_forest_intro.pdf" (S. Viridi, https://osf.io/hjdf9):
dataset golf (Samy Baladram), 14 data latih + 14 data uji.

Yang dilakukan skrip ini:
  1. Melatih satu Decision Tree (gini) -> slide bagian "decision tree".
  2. Menunjukkan efek parameter kunci: max_depth dan min_samples_split -> slide "key parameters".
  3. Melatih Random Forest (bootstrap + subset fitur acak + voting) -> slide "random forest".
  4. Menunjukkan voting tiap pohon untuk satu data uji -> slide "testing stage" RF.
  5. Membandingkan akurasi tree vs forest -> slide "tree vs forest".

Jalankan:  python random_forest_golf.py
Output   :  teks di terminal + gambar di folder ./output
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

FEATURES = ["sunny", "overcast", "rainy", "temperature", "humidity", "wind"]

# ---------------------------------------------------------------------------
# Data persis dari slide 22-23 (training) dan 23 (testing).
# Kolom: sunny, overcast, rainy, temperature(F), humidity(%), wind, play
# Catatan: baris 9 memiliki humidity = 10, sesuai slide aslinya.
# ---------------------------------------------------------------------------
train_rows = [
    (1, 0, 0, 85, 85, 0, "No"),
    (1, 0, 0, 80, 90, 1, "No"),
    (0, 1, 0, 83, 78, 0, "Yes"),
    (0, 0, 1, 70, 96, 0, "Yes"),
    (0, 0, 1, 68, 80, 0, "Yes"),
    (0, 0, 1, 65, 70, 1, "No"),
    (0, 1, 0, 64, 65, 1, "Yes"),
    (1, 0, 0, 72, 95, 0, "No"),
    (1, 0, 0, 69, 70, 0, "Yes"),
    (0, 0, 1, 75, 10, 0, "Yes"),
    (1, 0, 0, 75, 70, 1, "Yes"),
    (0, 1, 0, 72, 90, 1, "Yes"),
    (0, 1, 0, 81, 75, 0, "Yes"),
    (0, 0, 1, 71, 80, 1, "No"),
]
test_rows = [
    (1, 0, 0, 81, 88, 0, "No"),
    (0, 0, 0, 74, 92, 1, "Yes"),
    (0, 1, 1, 76, 85, 0, "Yes"),
    (1, 0, 0, 78, 75, 0, "No"),
    (1, 0, 0, 82, 92, 0, "No"),
    (0, 1, 1, 67, 90, 1, "No"),
    (0, 0, 0, 85, 85, 1, "Yes"),
    (0, 1, 1, 73, 88, 0, "Yes"),
    (1, 0, 0, 88, 65, 0, "Yes"),
    (0, 0, 0, 77, 70, 0, "Yes"),
    (1, 0, 0, 79, 60, 1, "Yes"),
    (0, 0, 0, 80, 95, 1, "Yes"),
    (0, 1, 1, 66, 70, 0, "No"),
    (0, 0, 0, 84, 78, 1, "Yes"),
]

cols = FEATURES + ["play"]
train = pd.DataFrame(train_rows, columns=cols)
test = pd.DataFrame(test_rows, columns=cols, index=range(14, 28))

X_train, y_train = train[FEATURES], train["play"]
X_test, y_test = test[FEATURES], test["play"]


def line(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


# ---------------------------------------------------------------------------
# 1. Decision Tree
# ---------------------------------------------------------------------------
line("1. DECISION TREE (criterion='gini', tanpa batas kedalaman)")
dt = DecisionTreeClassifier(criterion="gini", random_state=42)
dt.fit(X_train, y_train)
print(export_text(dt, feature_names=FEATURES))
dt_pred = dt.predict(X_test)
dt_acc = accuracy_score(y_test, dt_pred)
print(f"Akurasi Decision Tree pada data uji: {dt_acc:.2%}")

# Contoh perhitungan Gini split di root (seperti slide 29-31)
def gini(labels):
    if len(labels) == 0:
        return 0.0
    p = labels.value_counts(normalize=True)
    return 1 - (p**2).sum()

line("   Contoh Gini impurity split di root node")
for feat, thr in [("overcast", 0.5), ("sunny", 0.5), ("temperature", 77.5)]:
    left = y_train[X_train[feat] <= thr]
    right = y_train[X_train[feat] > thr]
    w = (len(left) * gini(left) + len(right) * gini(right)) / len(y_train)
    print(f"   {feat:<12} <= {thr:<5}: kiri {len(left):2d} (G={gini(left):.3f}), "
          f"kanan {len(right):2d} (G={gini(right):.3f}) -> weighted Gini = {w:.3f}")

fig, ax = plt.subplots(figsize=(14, 7))
plot_tree(dt, feature_names=FEATURES, class_names=dt.classes_, filled=True,
          rounded=True, fontsize=9, ax=ax)
ax.set_title(f"Decision Tree (akurasi uji = {dt_acc:.0%})")
fig.tight_layout()
fig.savefig(OUT / "01_decision_tree.png", dpi=130)
plt.close(fig)

# ---------------------------------------------------------------------------
# 2. Parameter kunci
# ---------------------------------------------------------------------------
line("2. PARAMETER KUNCI DECISION TREE")
print(f"{'parameter':<24}{'kedalaman':>10}{'daun':>7}{'akurasi uji':>14}")
for label, kw in [
    ("default", {}),
    ("max_depth=4", {"max_depth": 4}),
    ("max_depth=2", {"max_depth": 2}),
    ("min_samples_split=5", {"min_samples_split": 5}),
    ("min_samples_split=8", {"min_samples_split": 8}),
    ("criterion='entropy'", {"criterion": "entropy"}),
]:
    m = DecisionTreeClassifier(random_state=42, **kw).fit(X_train, y_train)
    acc = accuracy_score(y_test, m.predict(X_test))
    print(f"{label:<24}{m.get_depth():>10}{m.get_n_leaves():>7}{acc:>14.2%}")

# ---------------------------------------------------------------------------
# 3. Random Forest
# ---------------------------------------------------------------------------
line("3. RANDOM FOREST (100 pohon, bootstrap, max_features='sqrt')")
rf = RandomForestClassifier(n_estimators=100, max_features="sqrt",
                            bootstrap=True, oob_score=True, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)
print(f"Akurasi Random Forest pada data uji: {rf_acc:.2%}")
print(f"OOB score (akurasi pada data yang tidak terambil bootstrap): {rf.oob_score_:.2%}")

print("\nContoh bootstrap sample (indeks data latih) untuk 3 pohon pertama:")
rng_states = [t.random_state for t in rf.estimators_[:3]]
for i, rs in enumerate(rng_states):
    idx = np.random.RandomState(rs).randint(0, len(X_train), len(X_train))
    oob = sorted(set(range(len(X_train))) - set(idx))
    print(f"   pohon {i+1}: sampel = {sorted(idx.tolist())}  | out-of-bag = {oob}")

imp = pd.Series(rf.feature_importances_, index=FEATURES).sort_values()
print("\nFeature importance:")
print(imp.sort_values(ascending=False).round(3).to_string())

# ---------------------------------------------------------------------------
# 4. Voting untuk satu data uji
# ---------------------------------------------------------------------------
line("4. VOTING SEMUA POHON")
classes = rf.classes_
votes = np.array([[classes[int(t.predict(X_test.values)[k])]
                   for t in rf.estimators_] for k in range(len(X_test))])
summary = pd.DataFrame({
    "aktual": y_test.values,
    "vote_Yes": (votes == "Yes").sum(axis=1),
    "vote_No": (votes == "No").sum(axis=1),
    "pred_RF": rf_pred,
    "pred_DT": dt_pred,
}, index=X_test.index)
print(summary.to_string())

k = 0
fig, ax = plt.subplots(figsize=(5, 4))
ax.bar(["Yes", "No"], [summary.iloc[k]["vote_Yes"], summary.iloc[k]["vote_No"]],
       color=["#2a9d8f", "#e76f51"])
ax.set_ylabel("jumlah pohon")
ax.set_title(f"Voting 100 pohon untuk data uji #{X_test.index[k]}\n"
             f"prediksi = {rf_pred[k]}, aktual = {y_test.iloc[k]}")
fig.tight_layout()
fig.savefig(OUT / "03_voting_contoh.png", dpi=130)
plt.close(fig)

# ---------------------------------------------------------------------------
# 5. Tree vs forest
# ---------------------------------------------------------------------------
line("5. TREE VS FOREST")
print(f"Decision Tree : {dt_acc:.2%}")
print(f"Random Forest : {rf_acc:.2%}")
for name, pred in [("Decision Tree", dt_pred), ("Random Forest", rf_pred)]:
    cm = confusion_matrix(y_test, pred, labels=["Yes", "No"])
    print(f"\nConfusion matrix {name} (baris=aktual, kolom=prediksi) [Yes, No]:\n{cm}")

# Akurasi RF vs jumlah pohon (dirata-rata 20 seed agar stabil)
n_list = [1, 3, 5, 10, 20, 50, 100, 200]
mean_acc = []
for n in n_list:
    accs = [accuracy_score(y_test, RandomForestClassifier(
        n_estimators=n, random_state=s).fit(X_train, y_train).predict(X_test))
        for s in range(20)]
    mean_acc.append(np.mean(accs))

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].plot(n_list, mean_acc, "o-", label="Random Forest (rata-rata 20 seed)")
axes[0].axhline(dt_acc, color="gray", ls="--", label="Decision Tree tunggal")
axes[0].set_xscale("log")
axes[0].set_xlabel("jumlah pohon (n_estimators)")
axes[0].set_ylabel("akurasi data uji")
axes[0].set_title("Tree vs Forest")
axes[0].legend()
axes[1].barh(imp.index, imp.values, color="#264653")
axes[1].set_title("Feature importance Random Forest")
fig.tight_layout()
fig.savefig(OUT / "02_tree_vs_forest.png", dpi=130)
plt.close(fig)

# Gambar 3 pohon pertama dari forest
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for i, ax in enumerate(axes):
    plot_tree(rf.estimators_[i], feature_names=FEATURES, class_names=classes,
              filled=True, rounded=True, fontsize=7, ax=ax)
    ax.set_title(f"Pohon ke-{i+1} di Random Forest")
fig.tight_layout()
fig.savefig(OUT / "04_contoh_pohon_forest.png", dpi=110)
plt.close(fig)

summary.to_csv(OUT / "hasil_prediksi.csv")
print(f"\nGambar dan CSV disimpan di: {OUT}")
