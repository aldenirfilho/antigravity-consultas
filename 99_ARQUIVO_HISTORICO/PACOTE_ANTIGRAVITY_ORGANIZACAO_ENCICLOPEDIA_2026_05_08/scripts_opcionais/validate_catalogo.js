const fs = require('fs');

const file = 'data/catalogo.json';

if (!fs.existsSync(file)) {
  console.error('❌ data/catalogo.json não encontrado.');
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(file, 'utf8'));
const required = ['id', 'title', 'path', 'status', 'type', 'theme', 'caption'];

let ok = true;

for (const item of data.items || []) {
  for (const key of required) {
    if (!item[key]) {
      console.error(`❌ Item sem ${key}:`, item);
      ok = false;
    }
  }
}

if (ok) {
  console.log(`✅ Catálogo válido: ${(data.items || []).length} itens.`);
} else {
  process.exit(1);
}
