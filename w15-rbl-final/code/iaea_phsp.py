"""
Reader (dan writer) sederhana untuk format phase space IAEA.

Format (Capote dkk., IAEA INDC(NDS)-0484, 2006):
  <nama>.IAEAheader : teks berisi blok "$KEY:" diikuti nilai di baris-baris berikutnya
  <nama>.IAEAphsp   : biner, record berukuran tetap ($RECORD_LENGTH byte)

Isi tiap record (urutan tetap; field yang konstan tidak ditulis ke record):
  int8    type    jenis partikel: 1=foton, 2=elektron, 3=positron, 4=neutron, 5=proton
                  tanda NEGATIF berarti cosinus arah w < 0
  float32 E       energi kinetik [MeV]; tanda NEGATIF menandai partikel pertama dari
                  history baru
  float32 x, y, z posisi [cm]   (z sering konstan -> tidak ada di record)
  float32 u, v    cosinus arah; w = sign * sqrt(1 - u^2 - v^2)
  float32 weight  bobot statistik (bisa konstan)
  float32 * n     extra floats
  int32   * m     extra longs

Blok header yang dipakai:
  $BYTE_ORDER       1234 = little-endian, 4321 = big-endian
  $RECORD_CONTENTS  7 baris flag 0/1 untuk X Y Z U V W Weight, lalu jumlah extra float
                    dan extra long
  $RECORD_CONSTANT  nilai untuk field yang flag-nya 0 (urutan sama)
  $RECORD_LENGTH    ukuran record [byte]
  $PARTICLES        jumlah partikel

Catatan: field W tidak pernah benar-benar disimpan (dihitung dari u, v dan tanda type),
meskipun flag-nya 1. Reader ini mengikuti konvensi tersebut dan memeriksa bahwa
RECORD_LENGTH sesuai dengan isi record.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

PARTICLE_NAMES = {1: "photon", 2: "electron", 3: "positron", 4: "neutron", 5: "proton"}
_FIELDS = ["X", "Y", "Z", "U", "V", "W", "Weight"]


@dataclass
class IAEAHeader:
    path: Path
    byte_order: str = "<"
    present: dict = field(default_factory=dict)   # nama field -> bool
    constants: dict = field(default_factory=dict) # nama field -> float
    n_extra_float: int = 0
    n_extra_long: int = 0
    record_length: int = 0
    particles: int = 0
    raw: dict = field(default_factory=dict)

    def dtype(self) -> np.dtype:
        f = [("type", "i1"), ("E", "f4")]
        for name in ["X", "Y", "Z", "U", "V"]:
            if self.present.get(name, False):
                f.append((name.lower(), "f4"))
        if self.present.get("Weight", False):
            f.append(("weight", "f4"))
        f += [(f"xf{i}", "f4") for i in range(self.n_extra_float)]
        f += [(f"xl{i}", "i4") for i in range(self.n_extra_long)]
        return np.dtype(f).newbyteorder(self.byte_order)


def _parse_blocks(text: str) -> dict:
    blocks, key = {}, None
    for line in text.splitlines():
        m = re.match(r"\s*\$(\w+):\s*(.*)$", line)
        if m:
            key = m.group(1).upper()
            blocks[key] = [m.group(2)] if m.group(2).strip() else []
        elif key is not None and line.strip():
            blocks[key].append(line)
    return blocks


def _first_number(s: str) -> float:
    m = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", s)
    if not m:
        raise ValueError(f"tidak ada angka di: {s!r}")
    return float(m.group(0))


def read_header(path: str | Path) -> IAEAHeader:
    path = Path(path)
    if path.suffix.lower() != ".iaeaheader":
        path = path.with_suffix(".IAEAheader")
    blocks = _parse_blocks(path.read_text(errors="replace"))
    h = IAEAHeader(path=path, raw=blocks)

    order = int(_first_number(blocks.get("BYTE_ORDER", ["1234"])[0]))
    h.byte_order = "<" if order == 1234 else ">"

    rc = [int(_first_number(l)) for l in blocks["RECORD_CONTENTS"]]
    h.present = {name: bool(v) for name, v in zip(_FIELDS, rc[:7])}
    h.n_extra_float = rc[7] if len(rc) > 7 else 0
    h.n_extra_long = rc[8] if len(rc) > 8 else 0

    consts = [_first_number(l) for l in blocks.get("RECORD_CONSTANT", [])]
    missing = [n for n in _FIELDS if not h.present[n] and n != "W"]
    for name, val in zip(missing, consts):
        h.constants[name] = val

    h.record_length = int(_first_number(blocks["RECORD_LENGTH"][0]))
    h.particles = int(_first_number(blocks["PARTICLES"][0]))

    expected = h.dtype().itemsize
    if expected != h.record_length:
        raise ValueError(f"RECORD_LENGTH header = {h.record_length}, tetapi isi record "
                         f"menghasilkan {expected} byte. Periksa RECORD_CONTENTS.")
    return h


def read_phsp(path: str | Path, max_particles: int | None = None,
              sample_fraction: float | None = None, seed: int = 0) -> dict:
    """Baca phase space menjadi dict kolom numpy (memory-mapped, aman untuk file besar).

    max_particles   : ambil N record pertama
    sample_fraction : ambil sub-sampel acak (0..1) dari seluruh file
    """
    h = read_header(path)
    data_path = h.path.with_suffix(".IAEAphsp")
    n_file = data_path.stat().st_size // h.record_length
    if n_file != h.particles:
        print(f"[peringatan] header: {h.particles} partikel, file: {n_file} record")
    rec = np.memmap(data_path, dtype=h.dtype(), mode="r", shape=(n_file,))
    if sample_fraction is not None:
        rng = np.random.default_rng(seed)
        idx = np.sort(rng.choice(n_file, int(n_file * sample_fraction), replace=False))
        rec = rec[idx]
    elif max_particles is not None:
        rec = rec[:max_particles]
    rec = np.asarray(rec)

    out = {}
    t = rec["type"].astype(np.int16)
    out["type"] = np.abs(t)
    out["new_history"] = rec["E"] < 0
    out["E"] = np.abs(rec["E"]).astype(np.float64)
    for name in ["X", "Y", "Z", "U", "V", "Weight"]:
        key = name.lower()
        if h.present.get(name, False):
            out[key] = rec[key if key != "weight" else "weight"].astype(np.float64)
        else:
            out[key] = np.full(len(rec), h.constants.get(name, 1.0 if name == "Weight" else 0.0))
    w2 = np.clip(1.0 - out["u"] ** 2 - out["v"] ** 2, 0.0, None)
    out["w"] = np.sign(t) * np.sqrt(w2)
    out["header"] = h
    return out


def write_phsp(path: str | Path, cols: dict, z_const: float, title: str = "synthetic") -> None:
    """Tulis phase space format IAEA (record: type, E, x, y, u, v, weight; Z konstan)."""
    path = Path(path)
    dt = np.dtype([("type", "i1"), ("E", "f4"), ("x", "f4"), ("y", "f4"),
                   ("u", "f4"), ("v", "f4"), ("weight", "f4")]).newbyteorder("<")
    n = len(cols["E"])
    rec = np.empty(n, dtype=dt)
    rec["type"] = (cols["type"] * np.where(cols["w"] < 0, -1, 1)).astype(np.int8)
    rec["E"] = np.where(cols["new_history"], -cols["E"], cols["E"])
    for k in ["x", "y", "u", "v", "weight"]:
        rec[k] = cols[k]
    rec.tofile(path.with_suffix(".IAEAphsp"))
    counts = {k: int(np.sum(cols["type"] == v)) for k, v in [("PHOTONS", 1), ("ELECTRONS", 2), ("POSITRONS", 3)]}
    header = f"""$IAEA_INDEX:
   0  // test phase space

$TITLE:
{title}

$FILE_TYPE:
    0

$CHECKSUM:
{rec.nbytes}

$RECORD_CONTENTS:
    1     // X is stored ?
    1     // Y is stored ?
    0     // Z is stored ?
    1     // U is stored ?
    1     // V is stored ?
    1     // W is stored ?
    1     // Weight is stored ?
    0     // Extra floats stored ?
    0     // Extra longs stored ?

$RECORD_CONSTANT:
   {z_const:.4f}   // Constant Z

$RECORD_LENGTH:
{dt.itemsize}

$BYTE_ORDER:
1234

$ORIG_HISTORIES:
{int(np.sum(cols['new_history']))}

$PARTICLES:
{n}

$PHOTONS:
{counts['PHOTONS']}

$ELECTRONS:
{counts['ELECTRONS']}

$POSITRONS:
{counts['POSITRONS']}
"""
    path.with_suffix(".IAEAheader").write_text(header)
