const fs = require("fs");

const files = ["data/topics.json", "data/connections.json", "assets/js/graph.js"];
let ok = true;

for (const file of files) {
  if (!fs.existsSync(file)) {
    console.error("❌ Arquivo ausente:", file);
    ok = false;
  } else {
    console.log("✅ Arquivo encontrado:", file);
  }
}

try {
  const topics = JSON.parse(fs.readFileSync("data/topics.json", "utf8"));
  const connections = JSON.parse(fs.readFileSync("data/connections.json", "utf8"));
  const nodeIds = new Set((connections.nodes || []).map(n => n.id));
  for (const edge of connections.edges || []) {
    if (!nodeIds.has(edge.from) || !nodeIds.has(edge.to)) {
      console.error("❌ Edge inválida:", edge);
      ok = false;
    }
  }
  console.log(`✅ Topics: ${topics.length}`);
  console.log(`✅ Nodes: ${(connections.nodes || []).length}`);
  console.log(`✅ Edges: ${(connections.edges || []).length}`);
} catch (err) {
  console.error("❌ JSON inválido:", err.message);
  ok = false;
}

if (!ok) process.exit(1);
console.log("✅ Mapa Vivo validado.");
