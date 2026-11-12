"""Contoh modul statistics bawaan Python (slide data_science_and_python_env, hlm. 24-28)."""
import statistics

datasets = {
    "dataset_1": [1, 2, 3, 5, 5, 5, 7, 8, 9],
    "dataset_2": [1, 2, 3, 5, 5, 5, 7, 18, 29],
    "dataset_3": [3, 3, 3, 5, 6, 6, 7, 7, 8],
}

print(f"{'dataset':<10}{'mean':>8}{'median':>8}{'mode':>8}{'multimode':>12}{'stdev':>8}")
for name, d in datasets.items():
    print(f"{name:<10}{statistics.mean(d):>8.3f}{statistics.median(d):>8}"
          f"{statistics.mode(d):>8}{str(statistics.multimode(d)):>12}"
          f"{statistics.stdev(d):>8.3f}")

print("\nCatatan:")
print("- dataset_1 dan dataset_2 punya median dan modus sama (5), tetapi mean dataset_2")
print("  jauh lebih besar karena outlier 18 dan 29. Median lebih tahan terhadap outlier.")
print("- dataset_3: angka 3 muncul 3x, sedangkan 6 dan 7 masing-masing 2x, jadi modusnya 3.")
print("  Datanya menumpuk di nilai kecil, sehingga mean (5.333) dan median (6) berbeda.")
