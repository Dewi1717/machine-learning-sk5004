"""
Assignment w12 - Genetic Algorithm (slide 17_ga_short_intro.pdf, https://osf.io/c87ka)

Dua contoh GA yang DITULIS ULANG dan DIUJI, mengikuti 7 langkah di slide 52-59:
  1 Initialization  2 Evaluation  3 Selection  4 Crossover  5 Mutation  6 Replacement  7 Repeat

Contoh A  (encoding real, mirip ide contoh DataCamp di slide 69-70 / 65):
  Cari a, b, c pada y = a x^2 + b x + c agar kurva melewati titik-titik data
  (curve fitting). Data dibuat dari a=2, b=-3, c=1 + noise, jadi jawabannya diketahui.
  Operator: tournament selection, blend crossover (BLX-alpha), Gaussian mutation, elitism.

Contoh B  (encoding permutasi, mirip ilustrasi slide 62-66 / contoh MLInsightsCentral):
  Rute dari supply point 0 mengunjungi 15 toko lalu kembali (TSP).
  Operator: tournament selection, order crossover (OX, seperti ilustrasi slide 63),
  swap mutation (gen ditukar, BUKAN diganti huruf baru), elitism.

Jalankan: python ga_examples.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)


def tournament(fitness, k=3):
    """Pilih 1 indeks: ambil k individu acak, menangkan yang fitness-nya tertinggi."""
    idx = rng.choice(len(fitness), size=k, replace=False)
    return idx[np.argmax(fitness[idx])]


# ===========================================================================
# Contoh A: curve fitting a, b, c
# ===========================================================================
A_TRUE = np.array([2.0, -3.0, 1.0])
x = np.linspace(-2, 3, 25)
y = A_TRUE[0] * x**2 + A_TRUE[1] * x + A_TRUE[2] + rng.normal(0, 0.5, x.size)
LOW, HIGH = -10.0, 10.0


def fitness_a(pop):
    """Fitness = -MSE (lebih tinggi = lebih baik). pop: (N, 3)."""
    pred = pop[:, [0]] * x**2 + pop[:, [1]] * x + pop[:, [2]]
    return -np.mean((pred - y) ** 2, axis=1)


def ga_real(pop_size=60, generations=80, p_cx=0.9, p_mut=0.2, sigma=0.5, elite=2):
    pop = rng.uniform(LOW, HIGH, (pop_size, 3))                 # 1. initialization
    history = []
    for g in range(generations):
        fit = fitness_a(pop)                                     # 2. evaluation
        order = np.argsort(fit)[::-1]
        history.append((g, *pop[order[0]], fit[order[0]], fit.mean()))
        new = [pop[i].copy() for i in order[:elite]]             # elitism
        while len(new) < pop_size:
            p1, p2 = pop[tournament(fit)], pop[tournament(fit)]  # 3. selection
            if rng.random() < p_cx:                              # 4. crossover BLX-0.5
                lo, hi = np.minimum(p1, p2), np.maximum(p1, p2)
                d = hi - lo
                c1 = rng.uniform(lo - 0.5 * d, hi + 0.5 * d)
                c2 = rng.uniform(lo - 0.5 * d, hi + 0.5 * d)
            else:
                c1, c2 = p1.copy(), p2.copy()
            for c in (c1, c2):                                   # 5. mutation (Gaussian)
                mask = rng.random(3) < p_mut
                c[mask] += rng.normal(0, sigma, mask.sum())
                new.append(np.clip(c, LOW, HIGH))
        pop = np.array(new[:pop_size])                           # 6. replacement
    fit = fitness_a(pop)                                         # 7. repeat (loop di atas)
    best = pop[np.argmax(fit)]
    return best, fit.max(), np.array(history)


print("=" * 70 + "\nCONTOH A: GA encoding real untuk curve fitting y = a x^2 + b x + c\n" + "=" * 70)
best, best_fit, hist = ga_real()
ls = np.polyfit(x, y, 2)   # pembanding: least squares (solusi eksak untuk data ini)
print(f"{'gen':>4}{'a':>10}{'b':>10}{'c':>10}{'best -MSE':>12}{'mean -MSE':>14}")
for row in hist[[0, 1, 2, 5, 10, 20, 40, 79]]:
    print(f"{int(row[0]):>4}{row[1]:>10.4f}{row[2]:>10.4f}{row[3]:>10.4f}{row[4]:>12.4f}{row[5]:>14.2f}")
print(f"\nGA            : a={best[0]:.4f}  b={best[1]:.4f}  c={best[2]:.4f}  MSE={-best_fit:.4f}")
mse_ls = np.mean((np.polyval(ls, x) - y) ** 2)
print(f"Least squares : a={ls[0]:.4f}  b={ls[1]:.4f}  c={ls[2]:.4f}  MSE={mse_ls:.4f}")
print(f"Nilai asli    : a={A_TRUE[0]:.4f}  b={A_TRUE[1]:.4f}  c={A_TRUE[2]:.4f}")

fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
for j, (lbl, col) in enumerate(zip("abc", ["tab:blue", "tab:green", "tab:red"])):
    axes[0].plot(hist[:, 0], hist[:, j + 1], color=col, label=lbl)
    axes[0].axhline(ls[j], color=col, ls=":", lw=1)
axes[0].set_title("Konvergensi parameter (titik-titik = least squares)")
axes[0].set_xlabel("generasi"); axes[0].legend()
axes[1].semilogy(hist[:, 0], -hist[:, 4], label="terbaik")
axes[1].semilogy(hist[:, 0], -hist[:, 5], label="rata-rata populasi")
axes[1].set_title("MSE per generasi"); axes[1].set_xlabel("generasi"); axes[1].legend()
xx = np.linspace(x.min(), x.max(), 200)
axes[2].scatter(x, y, s=15, color="k", label="data")
axes[2].plot(xx, np.polyval(best, xx), color="tab:orange", label="GA")
axes[2].plot(xx, np.polyval(ls, xx), "--", color="tab:blue", label="least squares")
axes[2].set_title("Hasil fitting"); axes[2].legend()
fig.tight_layout(); fig.savefig(OUT / "A_curve_fitting.png", dpi=120); plt.close(fig)

# ===========================================================================
# Contoh B: TSP (supply point + 15 toko)
# ===========================================================================
N_STORE = 15
pts = rng.uniform(-2, 2, (N_STORE + 1, 2))
pts[0] = [-2, 2]                                    # supply point (merah di slide 66)
D = np.linalg.norm(pts[:, None] - pts[None], axis=2)


def route_length(perm):
    r = np.concatenate([[0], perm, [0]])
    return D[r[:-1], r[1:]].sum()


def order_crossover(p1, p2):
    """OX: salin segmen p1, isi sisanya dengan urutan gen p2 (tanpa duplikat)."""
    n = len(p1)
    i, j = sorted(rng.choice(n, 2, replace=False))
    child = -np.ones(n, dtype=int)
    child[i:j + 1] = p1[i:j + 1]
    rest = [g for g in p2 if g not in child[i:j + 1]]
    child[[k for k in range(n) if child[k] < 0]] = rest
    return child


def swap_mutation(perm, p=0.2):
    perm = perm.copy()
    if rng.random() < p:
        i, j = rng.choice(len(perm), 2, replace=False)
        perm[i], perm[j] = perm[j], perm[i]
    return perm


def ga_tsp(pop_size=100, generations=300, elite=2):
    pop = [rng.permutation(np.arange(1, N_STORE + 1)) for _ in range(pop_size)]
    hist, snaps = [], {}
    for g in range(generations):
        lengths = np.array([route_length(p) for p in pop])
        fit = -lengths
        order = np.argsort(lengths)
        hist.append((lengths.min(), lengths.mean()))
        if g in (0, 10, 50, generations - 1):
            snaps[g] = pop[order[0]].copy()
        new = [pop[i].copy() for i in order[:elite]]
        while len(new) < pop_size:
            p1, p2 = pop[tournament(fit)], pop[tournament(fit)]
            new.append(swap_mutation(order_crossover(p1, p2)))
        pop = new
    return np.array(hist), snaps


print("\n" + "=" * 70 + "\nCONTOH B: GA encoding permutasi untuk rute 15 toko (TSP)\n" + "=" * 70)
hist_b, snaps = ga_tsp()
for g, perm in snaps.items():
    print(f"generasi {g:>3}: panjang rute terbaik = {route_length(perm):.3f}")
print("rute terbaik akhir: 0 -> " + " -> ".join(map(str, snaps[max(snaps)])) + " -> 0")

# Pembanding: nearest neighbour + 2-opt (heuristik klasik) untuk menilai kualitas GA
def nn_2opt():
    unvisited, route = set(range(1, N_STORE + 1)), [0]
    while unvisited:
        nxt = min(unvisited, key=lambda k: D[route[-1], k]); route.append(nxt); unvisited.remove(nxt)
    r = np.array(route[1:]); improved = True
    while improved:
        improved = False
        for i in range(len(r) - 1):
            for j in range(i + 1, len(r)):
                cand = r.copy(); cand[i:j + 1] = cand[i:j + 1][::-1]
                if route_length(cand) < route_length(r) - 1e-12:
                    r, improved = cand, True
    return r
ref = nn_2opt()
print(f"pembanding nearest-neighbour + 2-opt: {route_length(ref):.3f}")

fig, axes = plt.subplots(1, 5, figsize=(22, 4.3))
for ax, (g, perm) in zip(axes[:4], snaps.items()):
    r = np.concatenate([[0], perm, [0]])
    ax.plot(pts[r, 0], pts[r, 1], "r-", lw=1)
    ax.scatter(pts[1:, 0], pts[1:, 1], c="b", s=20)
    ax.scatter(*pts[0], c="r", s=80)
    ax.set_title(f"generasi {g}: panjang {route_length(perm):.2f}")
axes[4].plot(hist_b[:, 0], label="terbaik"); axes[4].plot(hist_b[:, 1], label="rata-rata")
axes[4].axhline(route_length(ref), color="gray", ls="--", label="NN + 2-opt")
axes[4].set_title("Panjang rute per generasi"); axes[4].set_xlabel("generasi"); axes[4].legend()
fig.tight_layout(); fig.savefig(OUT / "B_tsp_route.png", dpi=110); plt.close(fig)

print(f"\nGambar disimpan di {OUT}")
