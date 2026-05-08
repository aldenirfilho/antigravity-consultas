# Catálogo do Projeto — Enciclopédia Médica Intensiva & Medicina Interna

**Atualizado em:** 2026-05-08  
**Autor:** Dr. Aldenir Rocha  
**Repositório:** `aldenirfilho/antigravity-consultas`  
**Objetivo:** organizar módulos clínicos, Banco TEMI, Calculadoras UTI, Biblioteca IA, Card Feed e mapa vivo em uma arquitetura escalável para GitHub Pages e Antigravity.

---

## 1. Visão geral

Este catálogo serve como **mapa central do projeto**.  
Ele deve ser usado pelo Antigravity para:

- localizar arquivos ativos;
- manter links relativos;
- classificar novos materiais;
- criar legendas;
- atualizar `data/catalogo.json`;
- conectar módulos no mapa vivo;
- organizar cards e imagens por tema.

---

## 2. Catálogo operacional

| Módulo | Caminho | Status | Tipo | Tema | Legenda |
|---|---|---:|---|---|---|
| Portal Principal | `index.html` | ativo | portal | projeto | 🏠 Página-mãe da Enciclopédia Médica Intensiva & Medicina Interna, com acesso aos módulos clínicos, Banco TEMI, Calculadoras UTI, Biblioteca IA e Card Feed. |
| AVC Agudo | `01_Modulos_Clinicos/AVC_Agudo/avc.html` | ativo | hub clínico | neuro-uti | 🧠 Módulo inaugural TEMI/UTI com emergência, reperfusão, neuroimagem, UTI, prevenção secundária, dashboard e material extenso. |
| Banco de Questões Padrão TEMI | `02_Banco_Questoes_TEMI/index.html` | ativo | banco de questões | temi | 🏆 Simulador expansível para prova TEMI, com módulos temáticos, questões comentadas e conexão automática aos temas clínicos. |
| AVC Agudo — Questões TEMI | `02_Banco_Questoes_TEMI/avc_agudo_questoes.html` | ativo | questões comentadas | temi | 🧠 Banco inicial com 30 questões comentadas de AVC Agudo, conectado a neuroimagem, PA, reperfusão e Neuro UTI. |
| Central de Calculadoras UTI PRO | `03_Calculadoras_UTI/index.html` | ativo | calculadora | uti-geral | 🧮 Ferramenta beira-leito para cálculos de drogas, diluições, ventilação, eletrólitos, renal e gasometria com alertas de segurança. |
| Biblioteca IA | `05_Biblioteca_IA/index.html` | ativo | biblioteca | ia-produtividade | 📚 Repositório de materiais médicos em PDF, Word e HTML, com curadoria IA + revisão médica para UTI, Clínica Médica e TEMI. |
| Card Feed Médico | `06_Card_Feed_Medico/index.html` | ativo | feed visual | uti-geral | 🖼️ Feed visual de cards e wallpapers médicos com temas, tags, comentários, favoritos, status de revisão e backup JSON. |
| KDIGO 2026 AKI na UTI em 10 passos | `06_Card_Feed_Medico/assets/cards/nefro-aki-trs/kdigo_2026_aki_uti_10_passos_1080x1920.png` | novo | card visual | nefro-aki-trs | 🧪 Card de revisão rápida para AKI/TRS na UTI: diagnóstico, estratificação, indicações de TRS, complicações e pontos TEMI. |
| Diabetes: orientações visuais para cuidador/família | `06_Card_Feed_Medico/assets/cards/familia-paciente/diabetes_orientacoes_mae_1080x1920.png` | pendente-imagem | card visual | familia-paciente | 👨‍👩‍👧 Card de orientação para paciente/família: linguagem simples, horários, insulina, glicemia, segurança medicamentosa e sinais de alerta. |
| Ventilação protetora na SDRA — card de plantão | `06_Card_Feed_Medico/assets/cards/vm-sdra/vm_sdra_ventilacao_protetora_1080x1920.png` | pendente-imagem | card visual | vm-sdra | 🫁 Card de plantão para VM/SDRA: metas protetoras, mecânica respiratória, gasometria, resgate e erros críticos. |

---

## 3. Próximas ações recomendadas

1. Renderizar este catálogo na home usando `data/catalogo.json`.
2. Classificar imagens pendentes em `06_Card_Feed_Medico/assets/cards/inbox/`.
3. Atualizar `06_Card_Feed_Medico/data/cards.json`.
4. Atualizar `data/topics.json` e `data/connections.json`.
5. Criar uma rotina de revisão semanal do projeto.

---

## 4. Regra editorial

Todo novo item deve ter:

- `id` único em slug;
- título claro;
- caminho relativo;
- status;
- tipo;
- tema;
- legenda;
- tags;
- relações com outros temas;
- aviso de segurança clínica quando aplicável.

---

## 5. Status permitidos

- `ativo`
- `ativo/parcial`
- `planejado`
- `novo`
- `pendente-imagem`
- `inbox`
- `revisar`
- `arquivado`

---

## 6. Tipos permitidos

- `portal`
- `hub clínico`
- `calculadora`
- `banco de questões`
- `questões comentadas`
- `biblioteca`
- `feed visual`
- `card visual`
- `dashboard`
- `documento`
- `imagem`
- `dados`
- `script`
