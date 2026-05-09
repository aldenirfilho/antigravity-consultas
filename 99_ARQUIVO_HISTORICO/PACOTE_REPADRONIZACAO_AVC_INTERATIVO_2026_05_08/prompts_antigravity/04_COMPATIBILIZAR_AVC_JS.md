# 04 — Compatibilizar AVC JS

Abrir:

`01_Modulos_Clinicos/AVC_Agudo/avc.js`

## Objetivo

Preservar lógica, conteúdo e funções. Alterar somente classes visuais se necessário.

## Não alterar

- `globalDB`
- `renderMatriz`
- `renderCalculadoras`
- `calcLAMS`
- `calcNIHSS`
- `renderFlashcardsGrid`
- `renderQuizEngine`
- `setupScrollSpy`

## Permitido alterar

Classes Tailwind muito destoantes dentro de templates HTML para classes institucionais:

- `avc-section`
- `avc-accordion`
- `avc-accordion-summary`
- `avc-section-icon`
- `avc-list`
- `avc-list-item`
- `avc-card`
- `avc-form-control`

## Estratégia segura

Preferir manter `avc.js` intacto e resolver visual por CSS em `avc-theme.css`.

Só editar `avc.js` se algum bloco continuar muito fora do padrão após o CSS.
