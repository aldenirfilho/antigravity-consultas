# 🚀 INSTRUÇÕES PARA O ANTIGRAVITY — GEMINI FLASH

Use este arquivo como comando principal no Antigravity quando os créditos estiverem limitados e você estiver usando Gemini Flash.

## Objetivo

Migrar a Enciclopédia para o novo padrão:

- `07_Estudos_Markdown/` como central de análises em Markdown.
- `UPDOWN` como fluxo editorial de entrada/saída.
- Conteúdo didático próprio, sem copiar texto integral de fontes protegidas.
- Catálogo vivo por `registry.json` e `data/catalogo.json`.
- Página principal atualizada com link direto para a nova central.

## Faça exatamente isto

1. Copie a pasta `07_Estudos_Markdown` para a raiz do repositório.
2. Substitua `index.html` pelo `index.html` deste pacote.
3. Substitua `data/catalogo.json` pelo arquivo deste pacote.
4. Não remova módulos antigos: AVC, Banco TEMI, Calculadoras, Biblioteca IA e Card Feed devem continuar funcionando.
5. Preserve os links relativos.
6. Não mencionar fonte proprietária nominalmente nos cards públicos. Use termos como “capítulo de referência”, “material estudado”, “aula”, “artigo” ou “diretriz”.
7. Não inserir transcrição literal extensa de conteúdo protegido. Converter em síntese própria, algoritmo, tabela original, checklist e comentário clínico.
8. Se não souber ajustar o mapa vivo completo, apenas deixe o link do novo módulo na homepage e no catálogo.

## Prompt curto para Gemini Flash

> Integre este pacote na Enciclopédia Médica. Adicione a pasta `07_Estudos_Markdown`, substitua `index.html` e `data/catalogo.json`, preserve todos os módulos antigos e mantenha GitHub Pages estático. O novo padrão é Markdown vivo + UPDOWN + versões + análise didática própria. Não copie textos protegidos. Não mencione fontes proprietárias nominalmente em páginas públicas. Garanta que `07_Estudos_Markdown/index.html` abra e liste os arquivos do `registry.json`.

## Checklist final

- [ ] `https://aldenirfilho.github.io/antigravity-consultas/` abre a nova homepage.
- [ ] Botão “Estudos Markdown” funciona.
- [ ] `07_Estudos_Markdown/index.html` abre a lista.
- [ ] `viewer.html?doc=content/modelos/template_estudo_seguro.md` renderiza o Markdown.
- [ ] Catálogo da homepage mostra “Central de Estudos Markdown”.
- [ ] Nenhum conteúdo protegido foi copiado literalmente.
