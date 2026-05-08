# 04 — Restaurar Biblioteca IA e arquivos originais

## Diagnóstico

A listagem mostra **198 itens** em `05_Biblioteca_IA/inbox/`, mas a interface publicada pode mostrar zero arquivos por erro de catálogo/caminho/renderização.

## Objetivo

A Biblioteca deve voltar a exibir todos os materiais com:

- busca textual;
- filtro por extensão: PDF, DOCX, MD, CSV/TSV;
- filtro por tema;
- botão “Abrir arquivo”;
- botão “copiar caminho”;
- status: `inbox-a-classificar`, `catalogado`, `updown-gerado`, `card-gerado`.

## Arquivos a criar/atualizar

```txt
05_Biblioteca_IA/data/biblioteca_inbox_manifest_auto.json
05_Biblioteca_IA/data/biblioteca_catalogo.json
05_Biblioteca_IA/index.html
biblioteca/index.html
07_Estudos_Markdown/registry_biblioteca.json
07_Estudos_Markdown/assets/biblioteca.js
```

## Fonte de verdade inicial

Usar a pasta:

```txt
05_Biblioteca_IA/inbox/
```

Não mover arquivos dessa pasta neste resgate.

## Renderização esperada

Cada card deve conter:

```txt
Título
Tipo: PDF/DOCX/MD/etc
Tema inferido
Status
Caminho
Botão abrir
Botão copiar caminho
Botão sugerir UpDown
Botão sugerir Card/Imagem
```

## Temas iniciais sugeridos

- VM/SDRA
- Sepse/Choque
- Infectologia UTI
- Nefro/AKI/TRS
- Endócrino/Metabólico
- Cardio/Hemodinâmica
- Neuro UTI
- POCUS
- TEMI/R3
- Procedimentos
- Clínica Médica
- IA/Produtividade
- Biblioteca Geral

## Critérios de validação

- Página `/biblioteca/` não pode mostrar “0 arquivos”.
- Página `/05_Biblioteca_IA/` não pode mostrar “0 arquivos”.
- Abrir um PDF/DOCX deve funcionar via link relativo.
- Busca por `CVC`, `KDIGO`, `VM`, `Sepse`, `Hiponatremia`, `POCUS` deve retornar itens.
- Não pode haver 404 em arquivos existentes.
