const fs = require("fs");

const jsonFiles = [
  "05_Biblioteca_IA/data/biblioteca_catalogo.json",
  "05_Biblioteca_IA/data/biblioteca_brain_connections.json",
  "05_Biblioteca_IA/data/pendencias_biblioteca_ia.json"
];

let ok = true;

for (const file of jsonFiles) {
  if (!fs.existsSync(file)) {
    console.warn("⚠️ Ausente:", file);
    continue;
  }
  try {
    JSON.parse(fs.readFileSync(file, "utf8"));
    console.log("✅ JSON válido:", file);
  } catch (err) {
    console.error("❌ JSON inválido:", file, err.message);
    ok = false;
  }
}

if (!ok) process.exit(1);
console.log("✅ Validação básica concluída.");
