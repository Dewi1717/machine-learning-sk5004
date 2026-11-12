"""
Membuat file phase space SINTETIS dalam format IAEA untuk menguji pipeline,
sebelum data asli Varian Clinac 600C 6 MV dari IAEA diunduh.

!!! DATA INI BUKAN HASIL SIMULASI MONTE CARLO LINAC !!!
Model mainan dengan pola fisika kualitatif yang umum diketahui:
  - foton primer dari sumber titik (target), menyebar di dalam lapangan + penumbra kecil
  - spektrum bremsstrahlung 6 MV didekati distribusi gamma, dipotong pada 6 MeV
  - pelunakan spektrum di luar sumbu (off-axis softening)
  - foton hamburan kepala (flattening filter/kolimator): energi lebih rendah,
    arah lebih tersebar; fraksinya naik dengan field size
  - kontaminasi elektron: fraksinya naik dengan field size
Semua koefisien dipilih sendiri untuk keperluan uji.

Bidang scoring: z = 30 cm dari target. Field size didefinisikan di isocenter (SSD 100 cm).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from iaea_phsp import write_phsp

Z_PLANE, SSD = 30.0, 100.0
FIELD_SIZES = [5, 10, 20]          # cm x cm di isocenter
N_PER_FIELD = 300_000


def make(fs, n, rng):
    half = 0.5 * fs * Z_PLANE / SSD                         # setengah lebar lapangan di bidang scoring
    f_scat = 0.04 + 0.004 * fs                               # fraksi foton hamburan kepala
    f_elec = 0.003 + 0.0008 * fs                             # fraksi elektron kontaminan
    kind = rng.choice(3, size=n, p=[1 - f_scat - f_elec, f_scat, f_elec])

    x = rng.uniform(-half, half, n) + rng.normal(0, 0.08, n)   # penumbra
    y = rng.uniform(-half, half, n) + rng.normal(0, 0.08, n)
    r = np.hypot(x, y)
    theta = np.arctan(r / Z_PLANE)
    theta_ref = np.arctan(0.5 * 20 * np.sqrt(2) * Z_PLANE / SSD / Z_PLANE)

    # Energi
    scale = 0.95 * (1 - 0.18 * theta / theta_ref)           # off-axis softening
    E = rng.gamma(2.0, scale)
    E_scat = rng.gamma(1.6, 0.55, n)
    E_elec = rng.exponential(1.4, n) + 0.05
    E = np.where(kind == 1, E_scat, E)
    E = np.where(kind == 2, E_elec, E)
    # potong spektrum di 6 MeV dengan mengambil ulang (bukan clip, agar tidak ada lonjakan di 6 MeV)
    bad = E > 6.0
    while bad.any():
        E[bad] = rng.gamma(2.0, scale[bad] if np.ndim(scale) else scale)
        bad = E > 6.0
    E = np.maximum(E, 0.01)

    # Arah: primer dari sumber titik; hamburan & elektron dari sumber tersebar
    dx, dy = x.copy(), y.copy()
    spread = np.where(kind == 0, 0.0, np.where(kind == 1, 3.0, 5.0))
    dx += rng.normal(0, 1, n) * spread
    dy += rng.normal(0, 1, n) * spread
    norm = np.sqrt(dx**2 + dy**2 + Z_PLANE**2)
    u, v, w = dx / norm, dy / norm, Z_PLANE / norm

    ptype = np.where(kind == 2, 2, 1)
    ptype = np.where((kind == 2) & (rng.random(n) < 0.05), 3, ptype)   # sedikit positron
    return {"type": ptype, "E": E, "x": x, "y": y, "u": u, "v": v, "w": w,
            "weight": np.ones(n), "new_history": rng.random(n) < 0.9}


if __name__ == "__main__":
    out = Path(__file__).parent.parent / "data_synthetic"
    out.mkdir(exist_ok=True)
    rng = np.random.default_rng(2025)
    for fs in FIELD_SIZES:
        cols = make(fs, N_PER_FIELD, rng)
        name = out / f"SYNTH_Clinac600C_6MV_{fs}x{fs}"
        write_phsp(name, cols, Z_PLANE, title=f"SYNTHETIC test phsp, 6 MV, {fs}x{fs} cm2 (bukan data IAEA)")
        print(f"{name.name}: {N_PER_FIELD} partikel")
