const fs = require("fs");

const files = [
  "05_Biblioteca_IA/data/biblioteca_catalogo.json",
  "05_Biblioteca_IA/data/biblioteca_taxonomia_temas.json",
  "05_Biblioteca_IA/data/biblioteca_brain_connections.json",
  "05_Biblioteca_IA/data/biblioteca_inbox_manifest_186.json"
];

let ok = true;

for (const file of files) {
  if (!fs.existsSync(file)) {
    console.error("❌ Ausente:", file);
    ok = false;
    continue;
  }
  try {
    JSON.parse(fs.readFileSync(file, "utf8"));
    console.log("✅ JSON válido:", file);
  } catch (e) {
    console.error("❌ JSON inválido:", file, e.message);
    ok = false;
  }
}

if (fs.existsSync("05_Biblioteca_IA/data/biblioteca_catalogo.json")) {
  const catalog = JSON.parse(fs.readFileSync("05_Biblioteca_IA/data/biblioteca_catalogo.json", "utf8"));
  const ids = new Set();
  for (const item of catalog.files || []) {
    if (!item.id) {
      console.error("❌ Item sem id:", item.title || item.originalFilename);
      ok = false;
    }
    if (ids.has(item.id)) {
      console.error("❌ ID duplicado:", item.id);
      ok = false;
    }
    ids.add(item.id);
    if (item.path && !fs.existsSync(item.path)) {
      console.warn("⚠️ Caminho não encontrado:", item.path);
    }
  }
}

if (!ok) process.exit(1);
console.log("✅ Validação concluída.");
