# 00 — SUPERCOMANDO ANTIGRAVITY: Organizar Mapa Vivo

Você está no repositório:

`aldenirfilho/antigravity-consultas`

## Objetivo

Organizar o Mapa Vivo da Enciclopédia para funcionar como um cérebro visual conectando:

- Portal principal
- Biblioteca IA
- Card Feed Médico
- Banco TEMI
- Calculadoras UTI
- AVC Agudo
- VM/SDRA
- Sepse/Choque
- AKI/TRS
- Infectologia UTI
- Endócrino/Metabólico
- Farmacologia/Doses
- POCUS
- Família/Paciente
- IA/Produtividade

## Arquivos a aplicar

Copiar/substituir com backup lógico:

- `data/topics.json`
- `data/connections.json`
- `assets/js/graph.js`
- `assets/css/graph-vivo.css`

## Antes de substituir

1. Fazer backup dos arquivos atuais:
   - `data/topics.json`
   - `data/connections.json`
   - `assets/js/graph.js`

2. Registrar backup no relatório:

`08_Documentacao_Projeto/RELATORIO_MAPA_VIVO_2_0.md`

## Atualizar index.html

Adicionar no `<head>`:

```html
<link rel="stylesheet" href="assets/css/graph-vivo.css" />
```

Manter os scripts já existentes.

## Validar

1. Abrir `index.html`.
2. Ir até seção `#mapa`.
3. Confirmar que os nós aparecem.
4. Confirmar que as linhas/arestas aparecem.
5. Clicar em nós.
6. Confirmar drawer.
7. Testar links.
8. Testar mobile.

## Critério de sucesso

O mapa deve deixar de ser apenas um desenho AVC-cêntrico e virar um hub visual da Enciclopédia inteira, com nós ativos e planejados.
