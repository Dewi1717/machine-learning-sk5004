// Deck presentasi progres RBL (w15). Jalankan dari folder ML: npm install && npm run deck:w15
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { applyTheme } = require("../tools/apply_theme.js");
const OUT = process.argv[2];

// --- angka dari output/ pipeline (data sintetis) ---
const bq = fs.readFileSync(__dirname + "/output/beam_quality.csv", "utf8").trim().split(/\r?\n/).slice(1).map(l => l.split(",").map(Number));
const cls = fs.readFileSync(__dirname + "/output/classification_per_particle.csv", "utf8").trim().split(/\r?\n/).slice(1).map(l => l.split(","));

const THEME = {
  name: "Beam Physics", headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: "14212B", lt1: "FFFFFF", dk2: "0B2A3C", lt2: "EEF3F5", accent1: "F2A541", accent2: "1F7A8C",
    accent3: "5FA8B8", accent4: "C8553D", accent5: "8AA29E", accent6: "3D5A6C", hlink: "1F7A8C", folHlink: "3D5A6C" },
};
const HEX = THEME.colors;
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "RBL Final - Klasifikasi Phase Space IAEA";
const C = pres.SchemeColor;
const W = 13.33, H = 7.5, M = 0.6;

pres.defineSlideMaster({ title: "DARK", background: { color: C.background1 },
  objects: [{ rect: { x: 0, y: 0, w: W, h: H, fill: { color: C.text2 } } }],
  slideNumber: { x: W - 1.1, y: H - 0.55, w: 0.6, h: 0.3, fontSize: 11, color: C.accent3, align: "right" } });
pres.defineSlideMaster({ title: "CONTENT", background: { color: C.background1 },
  objects: [
    { text: { text: "SK5004 · RBL Final", options: { x: M, y: H - 0.55, w: 4, h: 0.3, fontSize: 11, color: C.accent6, margin: 0 } } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.45, w: W - 2 * M, h: 0.9, fontSize: 36, bold: true, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: W - 1.1, y: H - 0.55, w: 0.6, h: 0.3, fontSize: 11, color: C.accent6, align: "right" } });

const t = (s, text, o) => s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontSize: 16, color: C.text1, valign: "top" }, o));
const beam = (s, tag) => {
  for (let i = 0; i < 9; i++) {
    const sp = (i - 4) * 0.55;
    s.addShape(pres.shapes.LINE, { x: sp >= 0 ? 9.6 : 9.6 + sp, y: 0, w: Math.abs(sp), h: H, flipH: sp < 0,
      line: { color: C.accent1, width: 1.25, transparency: 55 + Math.abs(i - 4) * 9 }, objectName: `${tag}beam${i}` });
  }
  s.addShape(pres.shapes.OVAL, { x: 9.45, y: -0.15, w: 0.3, h: 0.3, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: `${tag}src` });
};
const tag = (s, x, y) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.2, h: 0.4, rectRadius: 0.08, fill: { color: C.accent4 }, line: { color: C.accent4 }, objectName: "synthTag" });
  t(s, "DATA SINTETIS", { x, y, w: 2.2, h: 0.4, fontSize: 13, bold: true, color: C.background1, align: "center", valign: "middle" });
};
const card = (s, x, y, w, h, dark, name) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12,
  fill: { color: dark ? C.text2 : C.background2 }, line: { color: dark ? C.text2 : C.background2 }, objectName: name });
const chartBase = () => ({ catAxisLabelColor: HEX.accent6, valAxisLabelColor: HEX.accent6, catAxisLabelFontFace: "+mn-lt",
  valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", titleFontFace: "+mn-lt", legendFontFace: "+mn-lt",
  catAxisLabelFontSize: 13, valAxisLabelFontSize: 12, dataLabelFontSize: 13, titleFontSize: 15, titleColor: HEX.dk2,
  valGridLine: { color: "D5DEE2", size: 0.75 }, catGridLine: { style: "none" }, showTitle: true });

// 1. Judul + tim
pres.addSection({ title: "Pembuka" });
let s = pres.addSlide({ masterName: "DARK", sectionTitle: "Pembuka" });
beam(s, "a");
t(s, "RBL FINAL · PRESENTASI PROGRES", { x: M, y: 0.9, w: 8, h: 0.4, fontSize: 14, bold: true, color: C.accent1, charSpacing: 2 });
t(s, "Klasifikasi Data Phase Space IAEA: Pengaruh Field Size terhadap Kualitas Berkas X-Ray Varian Clinac 600C 6 MV",
  { x: M, y: 1.45, w: 8.3, h: 2.4, fontSize: 32, bold: true, color: C.background1, fontFace: THEME.headFontFace });
t(s, "Tim", { x: M, y: 4.3, w: 3, h: 0.4, fontSize: 16, bold: true, color: C.accent3 });
t(s, [
  { text: "[Nama 1] ([NIM])", options: { breakLine: true } }, { text: "[Nama 2] ([NIM])", options: { breakLine: true } },
  { text: "[Nama 3] ([NIM])", options: { breakLine: true } }, { text: "[Nama 4] ([NIM])" },
], { x: M, y: 4.75, w: 8, h: 1.6, fontSize: 16, color: C.background1, paraSpaceAfter: 4 });
s.addNotes("Selamat pagi/siang. Kami tim [nama tim] akan menyampaikan progres proyek klasifikasi data phase space IAEA untuk menilai pengaruh field size terhadap kualitas berkas Varian Clinac 600C 6 MV. Anggota tim: [sebutkan]. (±20 detik)");

// 2. Ringkasan proyek
pres.addSection({ title: "Proyek" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Proyek" });
s.addText("Ringkasan proyek", { placeholder: "title" });
const ov = [
  ["Sumber data", "IAEA Phase-space Database, Varian Clinac 600C foton 6 MV, beberapa field size (format .IAEAheader + .IAEAphsp)"],
  ["Metode", "Reader phase space Python → fitur partikel (E, r, θ, jenis) → klasifikasi RF, SVM, NB, KNN → indikator kualitas berkas"],
  ["Kategori ML", "Supervised learning: klasifikasi multikelas (label = field size)"],
  ["Estimasi waktu", "4 minggu: pipeline (selesai) → data asli → analisis → 4 luaran"],
];
ov.forEach(([h, d], i) => {
  const x = M + (i % 2) * 6.17, y = 1.6 + Math.floor(i / 2) * 2.3;
  card(s, x, y, 5.95, 2.05, i === 2, `ov${i}`);
  t(s, h, { x: x + 0.3, y: y + 0.25, w: 5.35, h: 0.45, fontSize: 20, bold: true, color: i === 2 ? C.accent1 : C.text2 });
  t(s, d, { x: x + 0.3, y: y + 0.8, w: 5.35, h: 1.1, fontSize: 17, color: i === 2 ? C.background1 : C.text1 });
});
s.addNotes("Ringkasan: datanya dari IAEA Phase-space Database untuk Clinac 600C 6 MV. Metodenya membaca phase space dengan Python, membuat fitur per partikel, lalu klasifikasi dengan empat algoritma. Kategorinya supervised learning, klasifikasi multikelas dengan label field size. Estimasi waktunya empat minggu. (±40 detik)");

// 3. Masalah & solusi
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Proyek" });
s.addText("Masalah dan usulan solusi", { placeholder: "title" });
card(s, M, 1.6, 5.95, 3.9, false, "probCard");
t(s, "Masalah", { x: M + 0.35, y: 1.85, w: 5.3, h: 0.5, fontSize: 22, bold: true, color: C.accent4 });
t(s, [
  { text: "Saat field size diperbesar, hamburan kepala linac dan kontaminasi elektron bertambah, sehingga spektrum dan dosis berubah", options: { bullet: true, breakLine: true } },
  { text: "Phase space berisi jutaan partikel. Efek field size tersembunyi di distribusi E, posisi, dan arah", options: { bullet: true, breakLine: true } },
  { text: "Belum jelas ciri partikel mana yang paling membedakan field size", options: { bullet: true } },
], { x: M + 0.35, y: 2.5, w: 5.3, h: 3.5, fontSize: 16, paraSpaceAfter: 10 });
card(s, M + 6.17, 1.6, 5.95, 3.9, true, "solCard");
t(s, "Usulan solusi", { x: M + 6.52, y: 1.85, w: 5.3, h: 0.5, fontSize: 22, bold: true, color: C.accent1 });
t(s, [
  { text: "Pipeline Python yang membaca format IAEA langsung (memory-mapped, aman untuk file GB)", options: { bullet: true, breakLine: true } },
  { text: "Klasifikasi field size dari ciri partikel. Feature importance menunjukkan ciri yang paling berpengaruh", options: { bullet: true, breakLine: true } },
  { text: "Indikator kualitas berkas: spektrum, E rata-rata, softening off-axis, fraksi hamburan dan elektron", options: { bullet: true } },
], { x: M + 6.52, y: 2.5, w: 5.3, h: 3.5, fontSize: 16, color: C.background1, paraSpaceAfter: 10 });
s.addNotes("Masalahnya: perubahan field size mengubah komposisi partikel dan spektrum, tetapi efeknya tersembunyi di jutaan partikel. Solusinya: pipeline Python yang membaca format IAEA, klasifikasi field size dengan feature importance, dan indikator kualitas berkas. (±40 detik)");

// 4. Progres
pres.addSection({ title: "Progres" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Progres" });
s.addText("Progres: pipeline siap dan teruji", { placeholder: "title" });
const prog = [
  ["Reader format IAEA", "header + record biner, uji round-trip identik (float32)", "selesai"],
  ["Generator phase space sintetis", "untuk menguji pipeline sebelum data asli tersedia", "selesai"],
  ["Fitur + klasifikasi 4 algoritma", "10-fold stratified CV, feature importance", "selesai"],
  ["Indikator kualitas berkas", "spektrum, E rata-rata vs r, fraksi non-primer", "selesai"],
  ["Unduh data asli IAEA Clinac 600C", "terhambat proteksi bot situs + ukuran file", "berjalan"],
  ["TPR20,10, PDD, dosis Monte Carlo", "butuh transport di fantom air (EGSnrc/TOPAS)", "belum"],
];
const stCol = { selesai: C.accent2, berjalan: C.accent1, belum: C.accent5 };
prog.forEach(([a, b, st], i) => {
  const y = 1.55 + i * 0.78;
  card(s, M, y, W - 2 * M, 0.66, false, `prog${i}`);
  t(s, a, { x: M + 0.3, y: y + 0.13, w: 4.6, h: 0.42, fontSize: 17, bold: true, color: C.text2, valign: "middle" });
  t(s, b, { x: M + 5.0, y: y + 0.13, w: 5.1, h: 0.42, fontSize: 15, color: C.text1, valign: "middle" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: W - M - 1.85, y: y + 0.14, w: 1.6, h: 0.38, rectRadius: 0.08, fill: { color: stCol[st] }, line: { color: stCol[st] }, objectName: `st${i}` });
  t(s, st, { x: W - M - 1.85, y: y + 0.14, w: 1.6, h: 0.38, fontSize: 14, bold: true, color: st === "berjalan" ? C.text2 : C.background1, align: "center", valign: "middle" });
});
s.addNotes("Progres kami: reader format IAEA sudah selesai dan lolos uji round-trip. Karena data asli belum bisa diunduh, kami membuat generator phase space sintetis untuk menguji pipeline. Klasifikasi dan indikator kualitas berkas sudah berjalan. Yang masih berjalan: mengunduh data asli. Yang belum: TPR, PDD, dan dosis, karena memerlukan simulasi transport di fantom air. (±50 detik)");

// 5. Hasil awal klasifikasi
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Progres" });
s.addText("Hasil awal: klasifikasi field size", { placeholder: "title" });
tag(s, W - M - 2.2, 0.7);
s.addChart(pres.charts.BAR, [{ name: "Akurasi", labels: cls.map(r => r[0]), values: cls.map(r => +(+r[1]).toFixed(3)) }],
  Object.assign(chartBase(), { x: M, y: 1.55, w: 6.6, h: 4.6, barDir: "col", chartColors: [HEX.accent2], showValue: true,
    dataLabelPosition: "outEnd", dataLabelFormatCode: "0.00", dataLabelColor: HEX.dk2, valAxisMinVal: 0, valAxisMaxVal: 1,
    valAxisLabelFormatCode: "0.0", title: "Akurasi per partikel (10-fold CV, 3 kelas)", showLegend: false, objectName: "accChart" }));
card(s, 7.6, 1.55, 5.13, 2.1, true, "statCard1");
t(s, "1.00", { x: 7.9, y: 1.7, w: 2.0, h: 1.0, fontSize: 48, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
t(s, "akurasi bila diklasifikasi per kelompok 500 partikel (fitur histogram)", { x: 9.9, y: 1.85, w: 2.65, h: 1.6, fontSize: 15, color: C.background1, valign: "middle" });
card(s, 7.6, 3.9, 5.13, 2.25, false, "statCard2");
t(s, "≈ 0", { x: 7.9, y: 4.05, w: 2.0, h: 1.0, fontSize: 48, bold: true, color: C.accent4, fontFace: THEME.headFontFace });
t(s, "recall 10×10 dan 20×20 untuk partikel dekat sumbu: di sana partikel semua field size hampir identik", { x: 9.9, y: 4.05, w: 2.65, h: 1.95, fontSize: 15, color: C.text1, valign: "middle" });
s.addNotes("Hasil awal dengan data sintetis. Akurasi per partikel keempat algoritma sekitar 0,75 sampai 0,77, jauh di atas tebakan acak 0,33, tetapi tidak sempurna. Penyebabnya, partikel dekat sumbu berkas hampir identik untuk semua field size: recall 10×10 dan 20×20 di wilayah itu hampir nol. Bila diklasifikasi per kelompok 500 partikel dengan fitur histogram, akurasinya 1,00. Ini menjadi keputusan desain untuk data asli. (±50 detik)");

// 6. Diskusi
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Progres" });
s.addText("Diskusi: tantangan dan keputusan", { placeholder: "title" });
const disc = [
  ["Tantangan", C.accent4, [
    "Situs IAEA memakai proteksi bot; file phase space berukuran GB",
    "Satu partikel saja tidak cukup informatif (ambigu di dekat sumbu)",
    "Data sintetis belum mewakili linac sungguhan, jadi angkanya belum boleh disimpulkan",
  ]],
  ["Keputusan", C.accent2, [
    "Reader memory-mapped + sub-sampel acak per field size",
    "Tambah klasifikasi per kelompok partikel (histogram E, r, θ)",
    "Rencana: uji tanpa fitur posisi, apakah model hanya ‘mengukur lebar lapangan’?",
    "Bobot statistik phsp dipakai pada indikator kualitas berkas",
  ]],
];
disc.forEach(([h, col, items], i) => {
  const x = M + i * 6.17;
  card(s, x, 1.55, 5.95, 4.7, false, `disc${i}`);
  s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: 1.8, w: 0.5, h: 0.5, fill: { color: col }, line: { color: col }, objectName: `discDot${i}` });
  t(s, h, { x: x + 0.95, y: 1.8, w: 4.6, h: 0.5, fontSize: 22, bold: true, color: C.text2, valign: "middle" });
  t(s, items.map((it, k) => ({ text: it, options: { bullet: true, breakLine: k < items.length - 1 } })),
    { x: x + 0.3, y: 2.55, w: 5.35, h: 3.5, fontSize: 16, paraSpaceAfter: 10 });
});
s.addNotes("Tantangannya: akses dan ukuran data, partikel tunggal yang ambigu, dan data sintetis yang belum mewakili linac sungguhan. Keputusannya: reader memory-mapped dengan sub-sampel, klasifikasi per kelompok partikel, uji terpisah fitur posisi agar model tidak sekadar mengukur lebar lapangan, dan pemakaian bobot statistik. (±45 detik)");

// 7. Pemahaman
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Progres" });
s.addText("Pemahaman fisis efek field size", { placeholder: "title" });
tag(s, W - M - 2.2, 0.7);
const fsl = bq.map(r => `${r[0]}×${r[0]}`);
s.addChart(pres.charts.BAR, [
  { name: "Foton terhambur", labels: fsl, values: bq.map(r => +r[6].toFixed(2)) },
  { name: "Elektron", labels: fsl, values: bq.map(r => +r[2].toFixed(2)) },
], Object.assign(chartBase(), { x: M, y: 1.55, w: 6.2, h: 4.6, barDir: "col", barGrouping: "stacked", chartColors: [HEX.accent2, HEX.accent1],
  showValue: true, dataLabelPosition: "ctr", dataLabelFormatCode: "0.0", dataLabelColor: "FFFFFF", showLegend: true, legendPos: "b",
  legendFontSize: 13, title: "Komponen non-primer (%) per field size (cm)", valAxisLabelFormatCode: "0", objectName: "bqChart" }));
const und = [
  ["Hamburan kepala linac", "flattening filter dan jaw yang lebih terbuka menambah foton terhambur berenergi rendah"],
  ["Kontaminasi elektron", "naik dengan field size dan menaikkan dosis permukaan"],
  ["Pelunakan spektrum", `E rata-rata foton turun: ${bq[0][4].toFixed(2)} → ${bq[bq.length - 1][4].toFixed(2)} MeV (data sintetis)`],
];
und.forEach(([h, d], i) => {
  const y = 1.55 + i * 1.6;
  card(s, 7.2, y, 5.53, 1.4, false, `und${i}`);
  t(s, h, { x: 7.5, y: y + 0.18, w: 5.0, h: 0.4, fontSize: 18, bold: true, color: C.text2 });
  t(s, d, { x: 7.5, y: y + 0.62, w: 5.0, h: 0.7, fontSize: 15, color: C.text1 });
});
s.addNotes("Pemahaman fisis kami: saat field size membesar, foton terhambur dari kepala linac bertambah, kontaminasi elektron naik, dan spektrum foton melunak. Grafik ini dari data sintetis yang dibuat mengikuti pola tersebut. Dengan data asli, kami akan mengecek apakah besarnya sesuai literatur. (±40 detik)");

// 8. Pembagian tugas
pres.addSection({ title: "Penutup" });
s = pres.addSlide({ masterName: "DARK", sectionTitle: "Penutup" });
beam(s, "b");
t(s, "Pembagian tugas", { x: M, y: 0.8, w: 8, h: 0.6, fontSize: 32, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
const tasks = [["Medium story", "[Nama 1]"], ["YouTube video", "[Nama 2]"], ["Gist code", "[Nama 3]"], ["OSF slides", "[Nama 4]"]];
tasks.forEach(([a, b], i) => {
  const y = 1.75 + i * 0.95;
  s.addShape(pres.shapes.OVAL, { x: M, y: y + 0.05, w: 0.55, h: 0.55, fill: { color: C.accent2 }, line: { color: C.accent2 }, objectName: `tk${i}` });
  t(s, String(i + 1), { x: M, y: y + 0.05, w: 0.55, h: 0.55, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle" });
  t(s, a, { x: M + 0.8, y: y + 0.08, w: 3.4, h: 0.5, fontSize: 20, bold: true, color: C.background1, valign: "middle" });
  t(s, b, { x: M + 4.3, y: y + 0.08, w: 3.8, h: 0.5, fontSize: 18, color: C.accent3, valign: "middle" });
});
t(s, "Berikutnya: data asli IAEA → ulangi pipeline → TPR20,10 / PDD → empat luaran", { x: M, y: 5.75, w: 8.3, h: 0.5, fontSize: 16, italic: true, color: C.background2 });
t(s, "Terima kasih", { x: M, y: 6.3, w: 8, h: 0.6, fontSize: 24, bold: true, color: C.background1, fontFace: THEME.headFontFace });
s.addNotes("Pembagian tugas: Medium [nama], YouTube [nama], Gist [nama], OSF [nama]. Langkah berikutnya: mengunduh data asli IAEA, menjalankan ulang pipeline, menghitung TPR20,10 dan PDD, lalu menyusun keempat luaran. Terima kasih. (±30 detik)");

(async () => { await pres.writeFile({ fileName: OUT }); await applyTheme(OUT, THEME); console.log("written", OUT); })();
