# ✅ Checklist para inserir novo tema

## 1. Criar pasta

`temas/nome-do-tema/`

## 2. Criar arquivos mínimos

- `index.html`
- `nome-do-tema.md`
- `nome-do-tema.json`

## 3. Atualizar dados globais

- Adicionar entrada em `data/topics.json`.
- Adicionar nós e conexões em `data/connections.json`.
- Adicionar referências em `data/references.json` quando disponíveis.

## 4. Conferir estrutura obrigatória

Usar `templates/template-tema-medico.md`.

## 5. Conferir segurança

- Há contraindicações?
- Há doses?
- Há risco de dano se aplicado fora de contexto?
- Há menção de protocolo local?
- Há necessidade de especialista?

## 6. Conferir interconexões

Cada tema deve apontar para pelo menos:

- 3 temas fisiopatologicamente relacionados.
- 3 temas de conduta/complicação.
- 1 bloco de prova.
- 1 bloco de segurança.
