const fs = require("fs");

const catalogPath = "05_Biblioteca_IA/data/biblioteca_catalogo.json";
const outPath = "05_Biblioteca_IA/data/biblioteca_duplicados.json";

function norm(s) {
  return String(s || "")
    .toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

if (!fs.existsSync(catalogPath)) {
  console.error("❌ Catálogo não encontrado:", catalogPath);
  process.exit(1);
}

const catalog = JSON.parse(fs.readFileSync(catalogPath, "utf8"));
const files = catalog.files || [];
const groups = {};

for (const item of files) {
  const key = norm(item.title || item.originalFilename || item.newFilename);
  if (!key) continue;
  groups[key] = groups[key] || [];
  groups[key].push(item.id);
}

const duplicates = Object.entries(groups)
  .filter(([_, ids]) => ids.length > 1)
  .map(([key, ids], idx) => ({
    groupId: `dup-${String(idx + 1).padStart(3, "0")}`,
    confidence: "media",
    reason: `Título/nome normalizado semelhante: ${key}`,
    items: ids,
    recommendedAction: "revisar",
    notes: ""
  }));

const payload = {
  updatedAt: new Date().toISOString().slice(0,10),
  duplicates
};

fs.writeFileSync(outPath, JSON.stringify(payload, null, 2));
console.log(`✅ Duplicados prováveis: ${duplicates.length}`);
