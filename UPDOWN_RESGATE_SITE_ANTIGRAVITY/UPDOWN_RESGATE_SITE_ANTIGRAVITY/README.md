# 🚑 RESGATE DO SITE UPDOWN — pacote de recuperação

Este pacote é para corrigir a desintegração do site após reorganização de rotas/links.

## Diagnóstico provável

O problema provavelmente ocorreu porque a última atualização **substituiu ou mudou a estrutura de links** sem preservar:

- a página da Biblioteca com PDFs/Word;
- links dos Markdown/HTML já gerados;
- rotas antigas dos módulos UpDown;
- caminhos relativos entre páginas;
- páginas de índice intermediárias.

## Regra de emergência

Não reescrever o site inteiro agora.

Primeiro, restaurar acesso com uma camada de navegação segura:

1. criar um `index.html` de resgate;
2. recriar `/biblioteca/index.html`;
3. recriar `/updown/index.html`;
4. recriar `/imagens/index.html`;
5. recriar `/apps/index.html`;
6. mapear arquivos existentes sem mover nada;
7. só depois melhorar visual.

## Arquivos deste pacote

```text
00_LEIA_PRIMEIRO/PLANO_DE_RESGATE.md
01_RESTAURAR_ROTAS/index_resgate.html
01_RESTAURAR_ROTAS/mapa_de_rotas.md
02_BIBLIOTECA/biblioteca_index_recovery.md
03_UPDOWN/updown_index_recovery.md
04_IMAGENS/imagens_index_recovery.md
05_APPS/apps_index_recovery.md
06_ANTIGRAVITY/PROMPT_RESGATE_ANTIGRAVITY.md
06_ANTIGRAVITY/CHECKLIST_NAO_QUEBRAR_LINKS.md
manifest_resgate.json
```

## Uso

Cole a pasta no repositório e peça ao Antigravity para seguir o arquivo:

```text
06_ANTIGRAVITY/PROMPT_RESGATE_ANTIGRAVITY.md
```

