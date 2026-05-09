# Cards de módulos UpDown — modelo padronizado

Use este modelo para listar os módulos já publicados e os próximos.

---

# 1. Card público de módulo

```markdown
## UPDOWN #002 — LES: manejo, monitoramento e prognóstico

**Área:** Reumatologia • Clínica Médica • UTI  
**Nível:** R3/TEMI  
**Status:** publicado  
**Leitura:** 20–30 min  
**Atualização:** 2026

**Resumo:** Manejo longitudinal do LES, metas terapêuticas, hidroxicloroquina, corticoide, biológicos, prevenção e prognóstico.

[Abrir modo leitor](/updown/002-les-manejo/index.html)  
[Ver biblioteca](/biblioteca/002-les-manejo/index.html)  
[Ver imagens](/imagens/002-les-manejo/index.html)  
[Questões](/questoes/002-les-manejo/index.html)
```

---

# 2. Card de módulo futuro

```markdown
## UPDOWN #003 — Nefrite lúpica

**Área:** Nefrologia • Reumatologia • UTI  
**Status:** planejado  
**Prioridade:** alta

**Aplicações relacionadas:** proteinúria, sedimento urinário, creatinina/TFGe, imunossupressão.

[Reservar módulo] [Adicionar fonte] [Criar imagens]
```

---

# 3. Layout de grade

```text
Desktop: 3 cards por linha
Tablet: 2 cards por linha
Mobile: 1 card por linha
```

Campos por card:

```json
{
  "id": "updown-002-les-manejo",
  "numero": 2,
  "titulo": "LES: manejo, monitoramento e prognóstico",
  "area": ["Reumatologia", "Clínica Médica", "UTI"],
  "status": "publicado",
  "leitura": "20–30 min",
  "links": {
    "reader": "/updown/002-les-manejo/index.html",
    "biblioteca": "/biblioteca/002-les-manejo/index.html",
    "imagens": "/imagens/002-les-manejo/index.html",
    "questoes": "/questoes/002-les-manejo/index.html"
  }
}
```
