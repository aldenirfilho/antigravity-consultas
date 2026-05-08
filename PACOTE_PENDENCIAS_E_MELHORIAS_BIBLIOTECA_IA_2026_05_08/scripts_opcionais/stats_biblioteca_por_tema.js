const fs = require("fs");

const catalogPath = "05_Biblioteca_IA/data/biblioteca_catalogo.json";
if (!fs.existsSync(catalogPath)) {
  console.error("Catálogo não encontrado.");
  process.exit(1);
}

const catalog = JSON.parse(fs.readFileSync(catalogPath, "utf8"));
const files = catalog.files || [];
const stats = {};

for (const item of files) {
  const theme = item.theme || "sem-tema";
  stats[theme] = (stats[theme] || 0) + 1;
}

console.log("📊 Estatísticas por tema:");
console.table(stats);
