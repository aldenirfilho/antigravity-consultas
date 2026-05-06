# 🧠 Enciclopédia Médica Intensiva & Medicina Interna

Projeto-base para abrir no **Google Antigravity** e evoluir como uma enciclopédia médica interativa, continuamente atualizada e focada em:

- 🚑 Medicina Intensiva / UTI / Emergência
- 🏥 Medicina Interna Avançada / Enfermaria / Diagnóstico diferencial
- 🏆 Preparação TEMI e prática de alto desempenho
- 🧠 Aprendizagem TDAH-friendly: mapas, checklists, flashcards, questões, imagens e algoritmos
- 🤖 Assimilação de conteúdos de múltiplas IAs, PDFs, Word, HTML, diretrizes e artigos

## 🚀 Como usar no Antigravity

1. Abra o Antigravity.
2. Crie ou selecione a pasta do projeto.
3. Copie esta pasta inteira para dentro do workspace.
4. Abra `index.html`.
5. Use o arquivo `antigravity.rules.md` como instrução do projeto.
6. Para criar novos temas, duplique `templates/template-tema-medico.md` ou `templates/template-tema-medico.html`.

## 🌳 Estrutura principal

```txt
enciclopedia-medica-antigravity/
├── index.html
├── README.md
├── antigravity.rules.md
├── temas/
│   ├── index.html
│   └── avc-agudo/
│       ├── index.html
│       ├── avc-agudo.md
│       └── avc-agudo.json
├── assets/
│   ├── css/
│   │   ├── base.css
│   │   ├── home.css
│   │   └── tema.css
│   ├── js/
│   │   ├── app.js
│   │   ├── graph.js
│   │   └── search.js
│   ├── img/
│   └── icons/
├── data/
│   ├── topics.json
│   ├── connections.json
│   ├── navigation.json
│   └── references.json
├── components/
│   ├── navbar.html
│   ├── footer.html
│   ├── topic-card.html
│   ├── safety-banner.html
│   └── breadcrumb.html
├── templates/
│   ├── template-tema-medico.md
│   ├── template-tema-medico.html
│   └── checklist-insercao-novo-tema.md
└── docs/
    ├── arquitetura.md
    ├── plano-editorial.md
    └── seguranca-curadoria.md
```

## 🧩 Primeiro tema conectado

O módulo inicial já incluído é:

- `temas/avc-agudo/index.html`
- `temas/avc-agudo/avc-agudo.md`
- `temas/avc-agudo/avc-agudo.json`

Ele deve ser expandido com o conteúdo completo do AVC Agudo seguindo o template oficial do projeto.
