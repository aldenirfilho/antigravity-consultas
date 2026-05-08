# Especificação técnica — fórmula dose ↔ mL/h

Este documento define a lógica básica para calculadoras de infusão contínua.

---

# 1. Fórmula para drogas em mcg/kg/min

```text
mL/h = (dose_mcg_kg_min × peso_kg × 60) / concentração_mcg_mL
```

## Inverso

```text
dose_mcg_kg_min = (mL_h × concentração_mcg_mL) / (peso_kg × 60)
```

---

# 2. Fórmula para drogas em mcg/min

```text
mL/h = (dose_mcg_min × 60) / concentração_mcg_mL
```

## Inverso

```text
dose_mcg_min = (mL_h × concentração_mcg_mL) / 60
```

---

# 3. Fórmula para vasopressina em UI/min

```text
mL/h = (dose_UI_min × 60) / concentração_UI_mL
```

## Inverso

```text
dose_UI_min = (mL_h × concentração_UI_mL) / 60
```

---

# 4. Cálculo de concentração

## mg em mL

```text
concentração_mcg_mL = (mg_totais × 1000) / volume_final_mL
```

## UI em mL

```text
concentração_UI_mL = UI_totais / volume_final_mL
```

---

# 5. Regra crítica para norepinefrina/noradrenalina

No Brasil, muitas ampolas exibem:

```text
Hemitartarato de norepinefrina 8 mg/4 mL
```

Mas isso frequentemente equivale a:

```text
Norepinefrina base 4 mg/4 mL = 1 mg/mL
```

A calculadora deve permitir escolher:

- calcular por **norepinefrina base**;
- calcular pelo **rótulo/sal**;
- exibir alerta de conferência institucional.

## Texto do alerta

> Atenção: confirme se o serviço prescreve noradrenalina como norepinefrina base ou hemitartarato. Muitas apresentações 8 mg/4 mL correspondem a 4 mg/4 mL de norepinefrina base.
