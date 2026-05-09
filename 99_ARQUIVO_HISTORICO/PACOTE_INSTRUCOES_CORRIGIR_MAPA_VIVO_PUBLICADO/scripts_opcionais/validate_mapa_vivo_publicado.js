const fs = require("fs");

let ok = true;
const required = [
  "index.html",
  "assets/js/graph.js",
  "assets/css/graph-vivo.css",
  "data/connections.json"
];

for (const file of required) {
  if (!fs.existsSync(file)) {
    console.error("❌ Ausente:", file);
    ok = false;
  } else {
    console.log("✅ Encontrado:", file);
  }
}

if (fs.existsSync("index.html")) {
  const index = fs.readFileSync("index.html", "utf8");
  if (!index.includes("assets/css/graph-vivo.css")) {
    console.error("❌ index.html não carrega graph-vivo.css");
    ok = false;
  }
  if (!index.includes("d3.v7.min.js")) {
    console.error("❌ index.html não carrega D3 v7");
    ok = false;
  }
  if (!index.includes("assets/js/graph.js")) {
    console.error("❌ index.html não carrega graph.js");
    ok = false;
  }
}

if (fs.existsSync("data/connections.json")) {
  try {
    const data = JSON.parse(fs.readFileSync("data/connections.json", "utf8"));
    const nodes = Array.isArray(data.nodes) ? data.nodes : [];
    const edges = Array.isArray(data.edges) ? data.edges : [];
    const ids = new Set();
    const duplicates = [];
    let orphanEdges = 0;

    for (const n of nodes) {
      if (!n.id) {
        console.error("❌ Nó sem id:", n);
        ok = false;
      }
      if (ids.has(n.id)) duplicates.push(n.id);
      ids.add(n.id);
    }

    for (const e of edges) {
      if (!ids.has(e.from) || !ids.has(e.to)) orphanEdges++;
    }

    if (duplicates.length) {
      console.error("❌ IDs duplicados:", duplicates);
      ok = false;
    }

    console.log(`📊 Nós: ${nodes.length}`);
    console.log(`📊 Conexões: ${edges.length}`);
    console.log(`📊 Edges órfãs: ${orphanEdges}`);
  } catch (e) {
    console.error("❌ connections.json inválido:", e.message);
    ok = false;
  }
}

if (!ok) process.exit(1);
console.log("✅ Validação estrutural concluída.");
