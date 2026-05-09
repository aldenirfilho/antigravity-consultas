# 04 — Conectar arquivos críticos aos módulos clínicos

## Objetivo

Criar conexões entre arquivos catalogados da Biblioteca IA e os módulos clínicos da Enciclopédia.

## Ler

- `05_Biblioteca_IA/data/biblioteca_catalogo.json`
- `05_Biblioteca_IA/data/biblioteca_brain_connections.json`
- `data/topics.json`
- `data/connections.json`

## Arquivos críticos

Considerar críticos os que tiverem:

- priority: alta-uti
- priority: temi
- tags: protocolo, emergência, dose, choque, VM, AKI, sepse, neuro, antibiótico, complicação
- safetyNotes preenchido
- clinicalUse preenchido

## Criar conexões

Para cada arquivo crítico:

1. Criar node em `biblioteca_brain_connections`.
2. Criar edge para tema.
3. Criar edge para Biblioteca IA.
4. Criar edge para módulo clínico se existir:
   - AVC Agudo
   - Ventilação Mecânica
   - Calculadoras UTI
   - Banco TEMI
   - Card Feed
5. Se o módulo ainda não existir, criar entrada planejada em patch.

## Saídas

- `data/topics_patch_biblioteca.json`
- `data/connections_patch_biblioteca.json`
- `05_Biblioteca_IA/data/biblioteca_brain_connections_patch.json`

## Regra

Gerar patch separado. Não sobrescrever arquivos principais sem revisão.
