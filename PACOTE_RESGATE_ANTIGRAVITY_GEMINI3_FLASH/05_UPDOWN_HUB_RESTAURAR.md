# 05 — Restaurar UpDown Hub

## Objetivo

Restaurar o hub UpDown como área pública de leitura, sem expor prompts internos, sugestões privadas ou bastidores.

## Arquivos principais

```txt
07_Estudos_Markdown/index.html
07_Estudos_Markdown/registry.json
07_Estudos_Markdown/assets/estudos.js
07_Estudos_Markdown/content/
updown/index.html
```

## Correções obrigatórias

### 1. Contador não pode mostrar zero se há documentos

Se `registry.json.documents.length > 0`, atualizar:

```txt
metricDocs
metricThemes
docsGrid
themeFilter
statusFilter
```

### 2. Resolver caminhos relativos

Para cada documento do registry:

- se `path` termina em `.html`, abrir direto;
- se `path` termina em `.md`, abrir via `viewer.html?src=...` ou abrir direto se GitHub Pages renderizar como texto;
- preservar `relatedUrl` se existir.

### 3. Separar público e privado

Não exibir na página pública arquivos:

```txt
_private/
antigravity_instructions.md
sugestoes_imagens_*.md
PROMPT_*
```

Esses podem ficar disponíveis para o usuário, mas não no leitor público.

### 4. Triângulo de conexão

Inserir em cada módulo:

```txt
[↕️ Ler UpDown] [📚 Fontes/Biblioteca] [🖼️ Imagens] [🧮 Apps relacionados]
```

### 5. Módulos atuais conhecidos

Garantir que apareçam:

- UPDOWN #001 — LES: Manifestações e Diagnóstico
- UPDOWN #002 — LES: Manejo e Prognóstico
- Exemplo: VM protetora e SDRA
- Template seguro para estudo

## Critérios de sucesso

- `/07_Estudos_Markdown/` mostra cards reais.
- `/updown/` aponta para o hub correto.
- Cada card abre.
- Não aparece conteúdo interno de produção na página pública.
