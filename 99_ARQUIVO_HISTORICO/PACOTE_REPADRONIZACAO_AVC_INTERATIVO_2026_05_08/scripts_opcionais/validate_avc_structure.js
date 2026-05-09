const fs = require("fs");
const path = require("path");

const requiredFiles = [
  "01_Modulos_Clinicos/AVC_Agudo/avc.html",
  "01_Modulos_Clinicos/AVC_Agudo/avc-theme.css",
  "01_Modulos_Clinicos/AVC_Agudo/avc.js",
  "01_Modulos_Clinicos/AVC_Agudo/db_fundamentos.js",
  "01_Modulos_Clinicos/AVC_Agudo/db_pratica.js",
  "01_Modulos_Clinicos/AVC_Agudo/db_interativo.js",
  "01_Modulos_Clinicos/AVC_Agudo/db_pesquisa.js",
  "01_Modulos_Clinicos/AVC_Agudo/db_cross_ia.js",
  "assets/css/base.css"
];

let ok = true;

for (const file of requiredFiles) {
  if (!fs.existsSync(file)) {
    console.error("❌ Ausente:", file);
    ok = false;
  } else {
    console.log("✅ Encontrado:", file);
  }
}

const htmlPath = "01_Modulos_Clinicos/AVC_Agudo/avc.html";
if (fs.existsSync(htmlPath)) {
  const html = fs.readFileSync(htmlPath, "utf8");
  const ids = ["menuBtn", "sidebar", "overlay", "sidebar-nav", "dynamic-content"];
  for (const id of ids) {
    if (!html.includes(`id="${id}"`) && !html.includes(`id='${id}'`)) {
      console.error("❌ ID essencial ausente:", id);
      ok = false;
    } else {
      console.log("✅ ID preservado:", id);
    }
  }
}

if (!ok) process.exit(1);
console.log("✅ Validação estrutural concluída.");
