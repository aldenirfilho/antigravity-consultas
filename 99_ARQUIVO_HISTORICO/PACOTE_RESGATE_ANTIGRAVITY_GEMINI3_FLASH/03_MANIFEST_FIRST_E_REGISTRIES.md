# 03 — Estratégia Manifest-First

## Problema

O projeto cresceu rápido e passou a depender de múltiplas páginas hard-coded. Isso quebra quando um arquivo muda de pasta ou quando uma página aponta para um JSON vazio.

## Solução

Criar uma camada central de dados:

```txt
data/site_manifest.json
data/route_aliases.json
data/connections.json
05_Biblioteca_IA/data/biblioteca_catalogo.json
05_Biblioteca_IA/data/biblioteca_inbox_manifest_auto.json
07_Estudos_Markdown/registry.json
07_Estudos_Markdown/registry_biblioteca.json
```

## `site_manifest.json` mínimo

```json
{
  "updatedAt": "2026-05-08",
  "project": "Enciclopédia Médica Intensiva & Medicina Interna",
  "version": "resgate-manifest-first-1.0",
  "routes": [],
  "modules": [],
  "hubs": {
    "home": "index.html",
    "updown": "07_Estudos_Markdown/index.html",
    "biblioteca": "biblioteca/index.html",
    "imagens": "imagens/index.html",
    "apps": "apps/index.html",
    "mapa": "data/connections.json"
  }
}
```

## Regra técnica

Todas as páginas principais devem renderizar cards a partir de JSON quando possível.

Evitar:

```js
const arquivos = [];
```

Preferir:

```js
fetch('data/site_manifest.json')
fetch('../05_Biblioteca_IA/data/biblioteca_catalogo.json')
fetch('registry.json')
```

## Fallback obrigatório

Se o JSON falhar:

1. mostrar mensagem útil;
2. mostrar links estáticos de emergência;
3. não deixar a página vazia.
