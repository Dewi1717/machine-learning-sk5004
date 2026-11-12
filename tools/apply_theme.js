// Menulis warna dan font tema ke file .pptx buatan pptxgenjs.
// pptxgenjs belum bisa mengatur warna tema; tanpa langkah ini, warna "scheme"
// (accent1, dk2, ...) akan tampil dengan palet bawaan Office.
//
// Pemakaian: const { applyTheme } = require("../tools/apply_theme.js");
//            await applyTheme("deck.pptx", THEME);
// THEME = { name, headFontFace, bodyFontFace, colors: { dk1, lt1, dk2, lt2, accent1..accent6, hlink, folHlink } }
const fs = require("fs");
const JSZip = require("jszip"); // ikut terpasang bersama pptxgenjs

const SLOTS = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"];
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

async function applyTheme(file, theme) {
  for (const k of SLOTS) {
    if (!/^[0-9A-Fa-f]{6}$/.test(theme.colors[k] || "")) throw new Error(`warna ${k} harus hex 6 digit tanpa #`);
  }
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const themeFiles = Object.keys(zip.files).filter((p) => /^ppt\/theme\/theme\d+\.xml$/.test(p));
  for (const p of themeFiles) {
    let xml = await zip.file(p).async("string");
    xml = xml.replace(/<a:clrScheme name="[^"]*">/, `<a:clrScheme name="${esc(theme.name)}">`);
    for (const k of SLOTS) {
      const re = new RegExp(`<a:${k}>[\\s\\S]*?</a:${k}>`);
      xml = xml.replace(re, `<a:${k}><a:srgbClr val="${theme.colors[k].toUpperCase()}"/></a:${k}>`);
    }
    if (theme.headFontFace) xml = xml.replace(/(<a:majorFont>\s*<a:latin typeface=")[^"]*"/, `$1${esc(theme.headFontFace)}"`);
    if (theme.bodyFontFace) xml = xml.replace(/(<a:minorFont>\s*<a:latin typeface=")[^"]*"/, `$1${esc(theme.bodyFontFace)}"`);
    zip.file(p, xml);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

module.exports = { applyTheme };
