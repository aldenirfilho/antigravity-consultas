# ⚙️ Regras do Projeto — Enciclopédia Médica Intensiva & Medicina Interna

## Identidade do projeto

Você está trabalhando em uma enciclopédia médica viva, interativa, continuamente atualizada, voltada para:

1. Medicina Intensiva / UTI / Emergência.
2. Medicina Interna Avançada / Enfermaria / Diagnóstico diferencial.
3. Preparação para a prova TEMI.
4. Aprendizagem médica TDAH-friendly.
5. Integração de materiais gerados por múltiplas IAs e fontes científicas.

## Princípios obrigatórios

- Priorize segurança clínica.
- Separe claramente: evidência, opinião, extrapolação e protocolo local.
- Todo tema deve ter referências completas ao final.
- Todo conteúdo extra deve ser marcado como: `🔎 Informação extra`.
- Sempre criar links cruzados entre temas relacionados.
- Sempre favorecer linguagem didática, metódica, visual, com emojis úteis e destaque de pontos de prova.
- Todo tema deve conter versão profunda e versão beira-leito.
- Todo tema deve conter seção de UTI quando aplicável.
- Todo tema deve conter pontos TEMI quando aplicável.

## Estrutura obrigatória de cada tema

Ao criar ou atualizar um tema, seguir os blocos do arquivo:

`templates/template-tema-medico.md`

## Regras para novos arquivos

- Novos temas devem ficar em: `temas/nome-do-tema/`.
- Cada tema deve ter:
  - `index.html`
  - `nome-do-tema.md`
  - `nome-do-tema.json`
- Atualizar `data/topics.json`.
- Atualizar `data/connections.json`.
- Inserir links no mapa de conexões quando houver relação clínica.

## Padrão de segurança

Não gerar condutas como substituto de julgamento clínico. Sempre contextualizar:

- Indicação.
- Contraindicação.
- Risco.
- Monitorização.
- Ajustes por cenário.
- Quando pedir ajuda especializada.
- Quando transferir.
- Quando manejar em UTI.

## Estética

- Visual moderno, escuro, limpo, Apple-like, dashboard médico.
- Cards, chips, mapas e seções bem divididas.
- Otimizado para Mac, iPad e iPhone.
- Criar também versões mobile/wallpaper quando solicitado.

## Objetivo final

Criar uma plataforma de estudo e decisão médica que funcione como:

- Enciclopédia médica.
- Sistema de raciocínio clínico.
- Preparatório TEMI.
- Hub de protocolos.
- Base de atualização científica.
- Cérebro externo médico para prática real.
