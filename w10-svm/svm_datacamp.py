"""
Assignment w10 - Intro to Support Vector Machine (SK5004)

Bagian A: kode DataCamp persis seperti di slide 60-65
  (A. Navlani, "Support Vector Machines with Scikit-learn Tutorial", DataCamp, 2019)
  Dataset breast cancer, split 70/30 (random_state=109), SVC kernel linear.

Bagian B: tuning hyperparameter yang dibahas di slide 66-69 (kernel, C, gamma).

Bagian C: ilustrasi slide 10-16 (hyperplane, margin, support vectors) dan
  efek kernel pada data yang tidak linear-separable (slide 19-32).

Jalankan di dalam virtual environment:
    python svm_datacamp.py
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sklearn

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

print(f"Python      : {sys.version.split()[0]}")
print(f"Interpreter : {sys.executable}")
print(f"scikit-learn: {sklearn.__version__}")

# ===========================================================================
# A. Kode DataCamp (slide 60-65)
# ===========================================================================
print("\n" + "=" * 70 + "\nA. KODE DATACAMP\n" + "=" * 70)

# Import scikit-learn dataset library
from sklearn import datasets

# Load dataset
cancer = datasets.load_breast_cancer()

# print the names of the 13 features
print("Features: ", cancer.feature_names)

# print the label type of cancer('malignant' 'benign')
print("Labels: ", cancer.target_names)

# print data(feature)shape
print("Shape:", cancer.data.shape)

# print the cancer data features (top 5 records)
print(cancer.data[0:5])

# print the cancer labels (0:malignant, 1:benign)
print(cancer.target)

# Import train_test_split function
from sklearn.model_selection import train_test_split

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, test_size=0.3, random_state=109
)  # 70% training and 30% test

# Import svm model
from sklearn import svm

# Create a svm Classifier
clf = svm.SVC(kernel="linear")  # Linear Kernel

# Train the model using the training sets
clf.fit(X_train, y_train)

# Predict the response for test dataset
y_pred = clf.predict(X_test)

# Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics

# Model Accuracy: how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

# Model Precision: what percentage of positive tuples are labeled as such?
print("Precision:", metrics.precision_score(y_test, y_pred))

# Model Recall: what percentage of positive tuples are labelled as such?
print("Recall:", metrics.recall_score(y_test, y_pred))

print("\nConfusion matrix (baris=aktual, kolom=prediksi) [malignant, benign]:")
print(metrics.confusion_matrix(y_test, y_pred))
print(f"Jumlah support vector per kelas: {clf.n_support_}")

# ===========================================================================
# B. Tuning hyperparameter: kernel, C (regularization), gamma (slide 66-69)
# ===========================================================================
print("\n" + "=" * 70 + "\nB. TUNING HYPERPARAMETER (data di-standardisasi)\n" + "=" * 70)
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

print(f"{'kernel':<8}{'C':>8}{'gamma':>10}{'akurasi uji':>14}{'#SV':>6}")
for kernel, C, gamma in [
    ("linear", 1, "scale"),
    ("poly", 1, "scale"),
    ("rbf", 1, "scale"),
    ("sigmoid", 1, "scale"),
    ("rbf", 0.01, "scale"),
    ("rbf", 100, "scale"),
    ("rbf", 1, 0.001),
    ("rbf", 1, 1.0),
]:
    m = make_pipeline(StandardScaler(), svm.SVC(kernel=kernel, C=C, gamma=gamma))
    m.fit(X_train, y_train)
    acc = metrics.accuracy_score(y_test, m.predict(X_test))
    nsv = m[-1].n_support_.sum()
    print(f"{kernel:<8}{C:>8}{str(gamma):>10}{acc:>14.4f}{nsv:>6}")

grid = GridSearchCV(
    make_pipeline(StandardScaler(), svm.SVC()),
    {"svc__kernel": ["linear", "rbf"],
     "svc__C": [0.01, 0.1, 1, 10, 100],
     "svc__gamma": ["scale", 0.001, 0.01, 0.1]},
    cv=5,
)
grid.fit(X_train, y_train)
best_acc = metrics.accuracy_score(y_test, grid.predict(X_test))
print(f"\nGridSearchCV (5-fold) parameter terbaik: {grid.best_params_}")
print(f"  akurasi CV = {grid.best_score_:.4f}, akurasi uji = {best_acc:.4f}")

# ===========================================================================
# C. Ilustrasi hyperplane, margin, support vectors, dan kernel
# ===========================================================================
from sklearn.datasets import make_blobs, make_circles


def plot_svc(ax, model, X, y, title):
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", s=30, edgecolors="k")
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    xx, yy = np.meshgrid(np.linspace(*xlim, 200), np.linspace(*ylim, 200))
    Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contour(xx, yy, Z, levels=[-1, 0, 1], colors="k",
               linestyles=["--", "-", "--"])
    sv = model.support_vectors_
    ax.scatter(sv[:, 0], sv[:, 1], s=140, facecolors="none", edgecolors="g",
               linewidths=1.5, label=f"support vectors ({len(sv)})")
    ax.set_title(title)
    ax.legend(loc="lower right", fontsize=8)


# C1: hyperplane w.x - b = 0 dan margin (slide 10)
Xb, yb = make_blobs(n_samples=60, centers=2, random_state=6)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, C in zip(axes, [1000, 0.05]):
    m = svm.SVC(kernel="linear", C=C).fit(Xb, yb)
    w, b = m.coef_[0], -m.intercept_[0]
    margin = 2 / np.linalg.norm(w)
    plot_svc(ax, m, Xb, yb, f"Linear SVM, C={C}\nlebar margin 2/||w|| = {margin:.2f}")
fig.suptitle("Hyperplane (garis tegas), batas margin w·x−b=±1 (putus-putus)")
fig.tight_layout()
fig.savefig(OUT / "01_hyperplane_margin.png", dpi=130)
plt.close(fig)

# C2: data lingkaran (tidak linear-separable) -> kernel trick
Xc, yc = make_circles(n_samples=200, factor=0.4, noise=0.08, random_state=0)
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
print("\n" + "=" * 70 + "\nC. KERNEL PADA DATA LINGKARAN (tidak linear-separable)\n" + "=" * 70)
for ax, kernel in zip(axes, ["linear", "poly", "rbf"]):
    kw = {"degree": 2} if kernel == "poly" else {}
    m = svm.SVC(kernel=kernel, C=1, **kw).fit(Xc, yc)
    acc = m.score(Xc, yc)
    print(f"kernel={kernel:<7} akurasi latih = {acc:.3f}")
    plot_svc(ax, m, Xc, yc, f"kernel = {kernel}, akurasi = {acc:.0%}")
fig.tight_layout()
fig.savefig(OUT / "02_kernel_comparison.png", dpi=130)
plt.close(fig)

# C3: efek gamma pada RBF (slide 69)
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for ax, g in zip(axes, [0.1, 1, 50]):
    m = svm.SVC(kernel="rbf", C=1, gamma=g).fit(Xc, yc)
    plot_svc(ax, m, Xc, yc, f"RBF gamma = {g}")
fig.suptitle("Gamma kecil -> batas halus (underfit); gamma besar -> batas berliku (overfit)")
fig.tight_layout()
fig.savefig(OUT / "03_gamma_effect.png", dpi=130)
plt.close(fig)

print(f"\nGambar disimpan di: {OUT}")
