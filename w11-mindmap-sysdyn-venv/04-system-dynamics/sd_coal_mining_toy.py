"""
Contoh model system dynamics (stock-flow) sederhana, terinspirasi slide 22-25
"system dynamics model" (S. Viridi, https://osf.io/z5vn2): ecological environmental
management di area tambang batubara (Shi dkk., IJERPH 2020).

PERHATIAN: ini model MAINAN untuk memahami konsep stock, flow, loop positif
(reinforcing) dan loop negatif (balancing). Nilai parameter dipilih sendiri,
TIDAK diambil dari paper.

Stock (level):
  GDP  : ekonomi daerah tambang
  P    : polusi udara terakumulasi (indeks)
Variabel bantu:
  I_env = alpha * GDP           investasi lingkungan (fraksi GDP)
  AQ    = 1 / (1 + P)           kualitas udara (0..1)
  cost  = c * P                 biaya penanggulangan polusi
Flow:
  dGDP/dt = g * GDP * AQ - cost           (pertumbuhan; terhambat polusi)
  dP/dt   = e * GDP - k * I_env * P       (emisi dari produksi - pembersihan)

Loop positif (slide 24): GDP naik -> investasi lingkungan naik -> polusi turun
  -> kualitas udara naik & biaya polusi turun -> GDP naik lagi.
Loop negatif (slide 25): investasi lingkungan naik -> polusi turun -> ...
  -> kebutuhan investasi berkurang (di sini: laju pembersihan k*I_env*P ikut turun
  ketika P turun), sehingga sistem menuju keseimbangan.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)


def simulate(alpha, T=60.0, dt=0.05, g=0.08, c=0.02, e=0.05, k=0.6, gdp0=10.0, p0=1.0):
    n = int(T / dt) + 1
    t = np.linspace(0, T, n)
    GDP = np.empty(n); P = np.empty(n); AQ = np.empty(n)
    GDP[0], P[0] = gdp0, p0
    for i in range(n - 1):          # integrasi Euler, seperti di software SD (Vensim/Stella)
        I_env = alpha * GDP[i]
        AQ[i] = 1 / (1 + P[i])
        dGDP = g * GDP[i] * AQ[i] - c * P[i]
        dP = e * GDP[i] - k * I_env * P[i]
        GDP[i + 1] = max(GDP[i] + dGDP * dt, 0.0)
        P[i + 1] = max(P[i] + dP * dt, 0.0)
    AQ[-1] = 1 / (1 + P[-1])
    return t, GDP, P, AQ


scenarios = [(0.0, "tanpa investasi lingkungan (alpha=0)"),
             (0.02, "investasi 2% GDP"),
             (0.10, "investasi 10% GDP")]

fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
print(f"{'skenario':<40}{'GDP(60)':>10}{'Polusi(60)':>12}{'AQ(60)':>9}")
for alpha, label in scenarios:
    t, GDP, P, AQ = simulate(alpha)
    axes[0].plot(t, GDP, label=label)
    axes[1].plot(t, P, label=label)
    axes[2].plot(t, AQ, label=label)
    print(f"{label:<40}{GDP[-1]:>10.2f}{P[-1]:>12.3f}{AQ[-1]:>9.3f}")
for ax, title in zip(axes, ["Stock: GDP", "Stock: polusi udara", "Kualitas udara AQ = 1/(1+P)"]):
    ax.set_title(title); ax.set_xlabel("waktu (tahun)"); ax.grid(alpha=0.3)
axes[0].legend(fontsize=8)
fig.suptitle("Model SD mainan: pengaruh investasi lingkungan di area tambang")
fig.tight_layout()
fig.savefig(OUT / "sd_simulation.png", dpi=120)
print(f"\nGambar: {OUT / 'sd_simulation.png'}")
