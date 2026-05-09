# 📁 Novo padrão de diretórios da Enciclopédia v3

## Estrutura principal

```text
antigravity-consultas/
├── index.html
├── data/
│   └── catalogo.json
├── 01_Modulos_Clinicos/
├── 02_Banco_Questoes_TEMI/
├── 03_Calculadoras_UTI/
├── 05_Biblioteca_IA/
├── 06_Card_Feed_Medico/
└── 07_Estudos_Markdown/
    ├── index.html
    ├── viewer.html
    ├── registry.json
    ├── assets/
    │   ├── estudos.css
    │   ├── estudos.js
    │   └── markdown-viewer.js
    └── content/
        ├── modelos/
        │   └── template_estudo_seguro.md
        └── intensiva/
            └── vm_sdra_nota_didatica.md
```

## Papel de cada camada

### `07_Estudos_Markdown/`
Central de conteúdo novo. Cada estudo entra como Markdown com metadados.

### `registry.json`
Lista todos os documentos Markdown que aparecem no catálogo.

### `viewer.html`
Leitor estático que abre qualquer `.md` pelo parâmetro `?doc=`.

### `content/`
Armazena os estudos transformados por tema.

Sugestão de subpastas:

```text
content/intensiva/
content/medicina-interna/
content/emergencia/
content/infectologia/
content/nefrologia/
content/cardiologia/
content/neurologia/
content/endocrino/
content/modelos/
```

## Regra de ouro

> O conteúdo público deve ser análise própria, síntese transformada e material didático original. Não arquivar cópias integrais de capítulos, artigos pagos ou textos proprietários.
