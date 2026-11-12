// Deck pitching RBL (w14). Jalankan dari folder ML: npm install && npm run deck:w14
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("../tools/apply_theme.js");

const OUT = process.argv[2];

const THEME = {
  name: "Beam Physics",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "14212B", lt1: "FFFFFF", dk2: "0B2A3C", lt2: "EEF3F5",
    accent1: "F2A541", accent2: "1F7A8C", accent3: "5FA8B8", accent4: "C8553D",
    accent5: "8AA29E", accent6: "3D5A6C", hlink: "1F7A8C", folHlink: "3D5A6C",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Pitching RBL - Klasifikasi Phase Space IAEA";
pres.author = "SK5004";
const C = pres.SchemeColor;
const W = 13.33, H = 7.5, M = 0.6;

// ---------- Layouts ----------
pres.defineSlideMaster({
  title: "DARK",
  background: { color: C.background1 },
  objects: [
    { rect: { x: 0, y: 0, w: W, h: H, fill: { color: C.text2 } } },
  ],
  slideNumber: { x: W - 1.1, y: H - 0.55, w: 0.6, h: 0.3, fontSize: 11, color: C.accent3, align: "right" },
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  objects: [
    { text: { text: "SK5004 · Pitching RBL", options: { x: M, y: H - 0.55, w: 4, h: 0.3, fontSize: 11, color: C.accent6, margin: 0 } } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.45, w: W - 2 * M, h: 0.9, fontSize: 36, bold: true, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: W - 1.1, y: H - 0.55, w: 0.6, h: 0.3, fontSize: 11, color: C.accent6, align: "right" },
});

const t = (slide, text, o) => slide.addText(text, Object.assign({ isTextBox: true, margin: 0, fontSize: 16, color: C.text1, valign: "top" }, o));

// ---------- 1. Title ----------
pres.addSection({ title: "Pembuka" });
let s = pres.addSlide({ masterName: "DARK", sectionTitle: "Pembuka" });
// beam motif: concentric fan of lines from a "source"
for (let i = 0; i < 9; i++) {
  const spread = (i - 4) * 0.55;
  s.addShape(pres.shapes.LINE, { x: spread >= 0 ? 9.6 : 9.6 + spread, y: 0.0, w: spread >= 0 ? spread : -spread, h: H, flipH: spread < 0,
    line: { color: C.accent1, width: 1.25, transparency: 55 + Math.abs(i - 4) * 9 }, objectName: `beam${i}` });
}
s.addShape(pres.shapes.OVAL, { x: 9.45, y: -0.15, w: 0.3, h: 0.3, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: "source" });
t(s, "RESEARCH-BASED LEARNING · PITCHING IDE", { x: M, y: 1.2, w: 8, h: 0.4, fontSize: 14, bold: true, color: C.accent1, charSpacing: 2 });
t(s, "Klasifikasi Data Phase Space IAEA untuk Menilai Pengaruh Field Size terhadap Kualitas Berkas dan Dosis Serap",
  { x: M, y: 1.8, w: 8.2, h: 2.6, fontSize: 36, bold: true, color: C.background1, fontFace: THEME.headFontFace, valign: "top" });
t(s, "Varian Clinac 600C · foton 6 MV · Machine Learning", { x: M, y: 4.55, w: 8, h: 0.45, fontSize: 20, color: C.accent3 });
t(s, "[Nama] · [NIM]\nSK5004 Machine Learning and Artificial Intelligence", { x: M, y: 5.6, w: 8, h: 0.9, fontSize: 16, color: C.background2 });
s.addNotes("Selamat pagi/siang. Saya akan mempresentasikan ide proyek RBL: klasifikasi data phase space IAEA untuk menilai pengaruh field size terhadap kualitas berkas X-ray dan dosis serap pada Varian Clinac 600C 6 MV. (±20 detik)");

// ---------- 2. Masalah & pertanyaan riset ----------
pres.addSection({ title: "Ide" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Ide" });
s.addText("Field size mengubah berkas, seberapa jauh?", { placeholder: "title" });
t(s, "Saat kolimator dibuka lebih lebar, hamburan dari kepala linac dan kontaminasi elektron ikut bertambah. Spektrum energi, kualitas berkas, dan dosis di pasien pun berubah.",
  { x: M, y: 1.55, w: 5.2, h: 2.2, fontSize: 18, color: C.text1 });
t(s, "Phase space IAEA mencatat setiap partikel yang keluar dari kepala linac, jadi data yang dibutuhkan untuk menjawabnya sudah tersedia.",
  { x: M, y: 3.85, w: 5.2, h: 1.6, fontSize: 16, italic: true, color: C.accent2 });
const rqs = [
  ["RQ1", "Bagaimana field size memengaruhi spektrum energi, energi rata-rata, TPR20,10, dan PDD10?"],
  ["RQ2", "Seberapa akurat RF, SVM, NB, dan KNN membedakan data phase space dari field size yang berbeda?"],
  ["RQ3", "Ciri partikel mana yang paling menentukan perbedaan itu, dan apa kaitannya dengan dosis serap?"],
];
rqs.forEach(([k, q], i) => {
  const y = 1.55 + i * 1.6;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.4, y, w: 6.33, h: 1.35, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: `rqCard${i}` });
  s.addShape(pres.shapes.OVAL, { x: 6.6, y: y + 0.3, w: 0.75, h: 0.75, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: `rqDot${i}` });
  t(s, k, { x: 6.6, y: y + 0.3, w: 0.75, h: 0.75, fontSize: 14, bold: true, color: C.text2, align: "center", valign: "middle" });
  t(s, q, { x: 7.55, y: y + 0.15, w: 5.0, h: 1.05, fontSize: 15, color: C.text1, valign: "middle" });
});
s.addNotes("Masalahnya: ketika field size diubah, hamburan dari kepala linac dan kontaminasi elektron ikut berubah, sehingga kualitas berkas dan dosis berubah. Data phase space IAEA mencatat setiap partikel, jadi kita bisa menelitinya. Ada tiga pertanyaan riset: RQ1 tentang kualitas berkas, RQ2 tentang akurasi klasifikasi ML, RQ3 tentang ciri yang paling berpengaruh dan kaitannya dengan dosis. (±50 detik)");

// ---------- 3. Sumber data ----------
pres.addSection({ title: "Rencana" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Rencana" });
s.addText("Sumber data: IAEA Phase-space Database", { placeholder: "title" });
t(s, "www-nds.iaea.org/phsp/photon1  ·  Varian Clinac 600C, foton 6 MV", { x: M, y: 1.45, w: 12, h: 0.4, fontSize: 16, color: C.accent2, bold: true });
// record diagram
t(s, "Satu baris = satu partikel di bidang phase space", { x: M, y: 2.15, w: 8, h: 0.4, fontSize: 16, bold: true, color: C.text2 });
const fields = [["jenis", "γ / e⁻ / e⁺"], ["E", "MeV"], ["x, y", "cm"], ["u, v, w", "cos arah"], ["bobot", "statistik"]];
fields.forEach(([a, b], i) => {
  const x = M + i * 1.62;
  s.addShape(pres.shapes.RECTANGLE, { x, y: 2.65, w: 1.52, h: 1.1, fill: { color: i % 2 ? C.accent2 : C.text2 }, line: { color: C.background1, width: 1 }, objectName: `field${i}` });
  t(s, a, { x, y: 2.75, w: 1.52, h: 0.5, fontSize: 18, bold: true, color: C.background1, align: "center" });
  t(s, b, { x, y: 3.25, w: 1.52, h: 0.4, fontSize: 12, color: C.background2, align: "center" });
});
t(s, [
  { text: "Format: file .IAEAheader (metadata) + .IAEAphsp (biner)", options: { bullet: true, breakLine: true } },
  { text: "Label kelas: field size, misalnya 5×5, 10×10, 20×20 cm² (sesuai yang tersedia di database)", options: { bullet: true, breakLine: true } },
  { text: "File berisi jutaan partikel (ukuran GB), jadi dipakai sub-sampel acak", options: { bullet: true } },
], { x: M, y: 4.1, w: 8, h: 2.2, fontSize: 16, paraSpaceAfter: 8 });
// stat callout
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 9.3, y: 2.15, w: 3.43, h: 4.15, rectRadius: 0.15, fill: { color: C.text2 }, line: { color: C.text2 }, objectName: "statCard" });
t(s, "10⁶–10⁸", { x: 9.5, y: 2.6, w: 3.03, h: 1.0, fontSize: 40, bold: true, color: C.accent1, align: "center", fontFace: THEME.headFontFace });
t(s, "partikel per file phase space", { x: 9.5, y: 3.6, w: 3.03, h: 0.6, fontSize: 14, color: C.background2, align: "center" });
t(s, "Data publik dan terstandar, tidak perlu simulasi kepala linac dari awal", { x: 9.6, y: 4.5, w: 2.83, h: 1.5, fontSize: 14, color: C.background1, align: "center", italic: true });
s.addNotes("Datanya berasal dari IAEA Phase-space Database untuk Varian Clinac 600C 6 MV. Setiap baris berisi satu partikel: jenis, energi, posisi, arah, dan bobot. Labelnya adalah field size. File phase space sangat besar sehingga akan dipakai sub-sampel. Catatan: field size yang tersedia akan dicek ulang di database. (±50 detik)");

// ---------- 4. Metode ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Rencana" });
s.addText("Metode: dari partikel ke kualitas berkas", { placeholder: "title" });
const steps = [
  ["1", "Baca phase space", "reader Python (numpy) untuk format IAEA"],
  ["2", "Rekayasa fitur", "E, r = √(x²+y²), sudut θ, jenis partikel"],
  ["3", "Klasifikasi", "RF · SVM · Naive Bayes · KNN, 10-fold CV"],
  ["4", "Evaluasi", "accuracy, precision, recall, F1, feature importance"],
  ["5", "Kualitas berkas & dosis", "spektrum, E rata-rata, TPR20,10, PDD10; dosis via Monte Carlo (opsional)"],
];
const bw = 2.3, gap = 0.18;
steps.forEach(([n, h, d], i) => {
  const x = M + i * (bw + gap);
  const dark = i === 2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.75, w: bw, h: 3.3, rectRadius: 0.12, fill: { color: dark ? C.text2 : C.background2 }, line: { color: dark ? C.text2 : C.background2 }, objectName: `step${i}` });
  s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: 2.0, w: 0.7, h: 0.7, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: `stepNum${i}` });
  t(s, n, { x: x + 0.25, y: 2.0, w: 0.7, h: 0.7, fontSize: 20, bold: true, color: C.text2, align: "center", valign: "middle" });
  t(s, h, { x: x + 0.25, y: 2.9, w: bw - 0.5, h: 0.8, fontSize: 17, bold: true, color: dark ? C.background1 : C.text2 });
  t(s, d, { x: x + 0.25, y: 3.7, w: bw - 0.5, h: 1.25, fontSize: 14, color: dark ? C.background2 : C.text1 });
  if (i < steps.length - 1) s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x: x + bw + 0.0, y: 3.33, w: 0.18, h: 0.14, rotate: 90, fill: { color: C.accent2 }, line: { color: C.accent2 }, objectName: `arrow${i}` });
});
t(s, "Alat: Python 3.11 · numpy · pandas · scikit-learn · matplotlib (venv + requirements.txt). Monte Carlo: EGSnrc/DOSXYZnrc atau TOPAS bila waktu memungkinkan.",
  { x: M, y: 5.45, w: W - 2 * M, h: 0.8, fontSize: 15, color: C.accent6, italic: true });
s.addNotes("Metodenya lima tahap. Pertama, phase space dibaca dengan reader Python. Kedua, dibuat fitur seperti energi, jarak radial, sudut, dan jenis partikel. Ketiga, klasifikasi field size dengan Random Forest, SVM, Naive Bayes, dan KNN memakai 10-fold cross validation. Keempat, evaluasi dengan accuracy, precision, recall, F1, dan feature importance. Kelima, menghitung indikator kualitas berkas; dosis serap dengan Monte Carlo menjadi target tambahan bila waktu cukup. (±60 detik)");

// ---------- 5. Timeline ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Rencana" });
s.addText("Estimasi waktu: 4 minggu", { placeholder: "title" });
const weeks = ["Minggu 1", "Minggu 2", "Minggu 3", "Minggu 4"];
const gx = 4.3, gw = (W - M - gx) / 4;
weeks.forEach((wk, i) => t(s, wk, { x: gx + i * gw, y: 1.55, w: gw, h: 0.4, fontSize: 14, bold: true, color: C.accent6, align: "center" }));
const tasks = [
  ["Unduh data, reader phase space, EDA", 0, 1, C.accent2],
  ["Fitur + klasifikasi 4 algoritma", 1, 2, C.text2],
  ["Kualitas berkas (spektrum, TPR, PDD)", 1.5, 3, C.accent3],
  ["Dosis Monte Carlo (opsional)", 2, 3.5, C.accent5],
  ["Medium · YouTube · Gist · OSF", 3, 4, C.accent1],
];
tasks.forEach(([name, a, b, col], i) => {
  const y = 2.15 + i * 0.78;
  t(s, name, { x: M, y: y + 0.08, w: 3.6, h: 0.45, fontSize: 15, color: C.text1 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: gx + a * gw + 0.05, y, w: (b - a) * gw - 0.1, h: 0.55, rectRadius: 0.1, fill: { color: col }, line: { color: col }, objectName: `bar${i}` });
});
t(s, "Bagian dosis Monte Carlo menjadi target tambahan, sehingga inti proyek (RQ1–RQ2) tetap selesai dalam 3 minggu.", { x: M, y: 6.15, w: W - 2 * M, h: 0.5, fontSize: 14, italic: true, color: C.accent6 });
s.addNotes("Estimasinya 4 minggu. Minggu pertama: data dan reader. Minggu kedua: fitur dan klasifikasi. Minggu kedua-ketiga: kualitas berkas. Dosis Monte Carlo opsional. Minggu keempat: menyiapkan keempat luaran. (±40 detik)");

// ---------- 6. Luaran & tim ----------
pres.addSection({ title: "Penutup" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Penutup" });
s.addText("Target luaran dan tim", { placeholder: "title" });
const outs = [
  ["Medium story", "Cerita populer: apa itu phase space dan mengapa field size penting", "[Anggota 1]"],
  ["YouTube video", "Video 5–10 menit: alur riset dan hasil klasifikasi", "[Anggota 2]"],
  ["Gist code", "Kode reader phase space + klasifikasi yang bisa dijalankan ulang", "[Anggota 3]"],
  ["OSF slides", "Slide hasil lengkap + DOI untuk disitasi", "[Anggota 4]"],
];
const cw = (W - 2 * M - 3 * 0.3) / 4;
outs.forEach(([h, d, who], i) => {
  const x = M + i * (cw + 0.3);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.65, w: cw, h: 3.9, rectRadius: 0.15, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: `outCard${i}` });
  s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: 1.95, w: 0.6, h: 0.6, fill: { color: C.accent2 }, line: { color: C.accent2 }, objectName: `outDot${i}` });
  t(s, String(i + 1), { x: x + 0.3, y: 1.95, w: 0.6, h: 0.6, fontSize: 18, bold: true, color: C.background1, align: "center", valign: "middle" });
  t(s, h, { x: x + 0.3, y: 2.75, w: cw - 0.6, h: 0.5, fontSize: 20, bold: true, color: C.text2 });
  t(s, d, { x: x + 0.3, y: 3.3, w: cw - 0.6, h: 1.4, fontSize: 15, color: C.text1 });
  t(s, "PJ: " + who, { x: x + 0.3, y: 4.85, w: cw - 0.6, h: 0.45, fontSize: 14, bold: true, color: C.accent4 });
});
t(s, "Tim maksimal 4 orang, masing-masing bertanggung jawab atas satu luaran.", { x: M, y: 5.85, w: W - 2 * M, h: 0.45, fontSize: 15, italic: true, color: C.accent6 });
s.addNotes("Proyek ini akan menghasilkan empat luaran: cerita Medium, video YouTube, kode di Gist, dan slide di OSF. Setiap anggota tim bertanggung jawab atas satu luaran. (±30 detik)");

// ---------- 7. Closing ----------
s = pres.addSlide({ masterName: "DARK", sectionTitle: "Penutup" });
for (let i = 0; i < 9; i++) {
  const spread = (i - 4) * 0.55;
  s.addShape(pres.shapes.LINE, { x: spread >= 0 ? 9.6 : 9.6 + spread, y: 0.0, w: spread >= 0 ? spread : -spread, h: H, flipH: spread < 0,
    line: { color: C.accent1, width: 1.25, transparency: 55 + Math.abs(i - 4) * 9 }, objectName: `beamEnd${i}` });
}
s.addShape(pres.shapes.OVAL, { x: 9.45, y: -0.15, w: 0.3, h: 0.3, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: "sourceEnd" });
t(s, "Yang diharapkan", { x: M, y: 1.3, w: 8, h: 0.6, fontSize: 28, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
t(s, [
  { text: "Peta kuantitatif pengaruh field size pada spektrum dan indeks kualitas berkas 6 MV", options: { bullet: true, breakLine: true } },
  { text: "Model ML yang mengenali field size dari ciri partikel, beserta fitur yang paling menentukan", options: { bullet: true, breakLine: true } },
  { text: "Pipeline Python terbuka untuk membaca dan menganalisis data phase space IAEA", options: { bullet: true } },
], { x: M, y: 2.1, w: 8, h: 2.6, fontSize: 18, color: C.background1, paraSpaceAfter: 10 });
t(s, "Terima kasih · Pertanyaan dan masukan?", { x: M, y: 5.3, w: 8, h: 0.7, fontSize: 26, bold: true, color: C.background1, fontFace: THEME.headFontFace });
s.addNotes("Hasil yang diharapkan: peta pengaruh field size pada kualitas berkas, model ML yang mengenali field size beserta fitur pentingnya, dan pipeline Python terbuka. Terima kasih, saya terbuka untuk pertanyaan dan masukan. (±30 detik)");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
