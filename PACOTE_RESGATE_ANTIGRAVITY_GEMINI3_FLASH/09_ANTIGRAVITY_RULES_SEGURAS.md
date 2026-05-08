# 09 — `antigravity.rules.md` sugerido para evitar nova quebra

Cole/adapte este conteúdo em `antigravity.rules.md`.

```md
# Regras do Projeto — Enciclopédia Médica Intensiva Antigravity

## Segurança de repositório

- Nunca deletar, mover ou renomear arquivos PDF, DOCX, MD, HTML, PNG, JSON ou ZIP sem autorização explícita.
- Antes de alterações grandes, listar arquivos que serão modificados.
- Preferir mudanças incrementais.
- Sempre manter rotas antigas com wrapper/redirect quando mudar navegação.
- Nunca substituir a home inteira sem preservar links existentes.
- Não alterar conteúdo clínico sem marcar revisão necessária.
- Não inserir dados identificáveis de pacientes.
- Não expor prompts privados, `_private/`, instruções internas ou bastidores em páginas públicas.

## Arquitetura

- Usar estratégia manifest-first.
- Rotas públicas principais:
  - `index.html`
  - `updown/index.html`
  - `biblioteca/index.html`
  - `imagens/index.html`
  - `apps/index.html`
  - `03_Calculadoras_UTI/index.html`
  - `02_Banco_Questoes_TEMI/index.html`
  - `06_Card_Feed_Medico/index.html`
- Fonte canônica do mapa: `data/connections.json`.
- Fonte canônica UpDown: `07_Estudos_Markdown/registry.json`.
- Fonte canônica biblioteca: `05_Biblioteca_IA/data/biblioteca_catalogo.json`.

## Validação

Após qualquer mudança, verificar:
- links principais;
- ausência de 404;
- renderização mobile;
- biblioteca com arquivos;
- UpDown com cards;
- Mapa Vivo com linhas;
- calculadoras com testes numéricos.

## Estilo

- Mobile-first.
- Visual limpo.
- Cards compactos.
- Busca e filtros sempre que houver listas.
- Não esconder materiais importantes atrás de páginas vazias.
```
