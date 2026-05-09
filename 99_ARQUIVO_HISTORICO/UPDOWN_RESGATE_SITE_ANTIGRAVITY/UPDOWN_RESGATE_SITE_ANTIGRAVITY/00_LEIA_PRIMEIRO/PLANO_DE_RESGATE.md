# Plano de resgate do site UpDown

## 1. Pare a reorganização visual

Antes de mexer em layout, restaurar acesso aos arquivos.

## 2. Não apagar nada

O Antigravity deve ser instruído a:

- não deletar PDFs;
- não deletar `.docx`;
- não deletar `.md`;
- não deletar `.html`;
- não mover arquivos sem atualizar todos os links;
- não substituir páginas de biblioteca por cards vazios.

## 3. Criar uma camada de rotas estáveis

Criar estas páginas mesmo que algumas fiquem simples inicialmente:

```text
/index.html
/updown/index.html
/biblioteca/index.html
/imagens/index.html
/apps/index.html
```

## 4. Restaurar a Biblioteca

A Biblioteca precisa listar todos os arquivos reais existentes no repositório:

- PDFs;
- Word `.docx`;
- Markdown `.md`;
- HTML leitor;
- ZIPs, se existirem.

Cada item deve ter link direto e descrição curta.

## 5. Restaurar UpDowns

A página `/updown/index.html` deve ter cards para:

- UPDOWN #001 — LES manifestações e diagnóstico;
- UPDOWN #002 — LES manejo e prognóstico;
- UPDOWN #003 — autoanticorpos anti-dsDNA, anti-Sm e anti-U1 RNP.

Cada card deve apontar preferencialmente para `index.html` do módulo, não para `.md`.

## 6. Restaurar Imagens

A página `/imagens/index.html` deve existir mesmo sem todas as imagens prontas.

Ela deve agrupar:

- imagens geradas;
- prompts privados não devem aparecer;
- placeholders podem aparecer como “em breve”.

## 7. Restaurar Apps

A página `/apps/index.html` deve listar:

- calculadora de drogas vasoativas;
- mapa de FAN;
- CAM-ICU/delirium;
- sepse/SOFA/qSOFA;
- Wells;
- Glasgow;
- SAPS3;
- Adrogué-Madias;
- NaCl mEq/mL.

## 8. Depois de restaurar, melhorar

Somente depois de todos os links funcionarem:

- melhorar cards;
- melhorar layout;
- melhorar busca;
- melhorar responsividade;
- organizar metadados.

