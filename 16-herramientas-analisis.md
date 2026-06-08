# HERRAMIENTAS DE ANÁLISIS - ESTRATEGIA BSLC

## Herramienta 1: Cálculo de Balance Hídrico

```
Fórmula: ΔW = P + C + G - E - T - U

Donde:
P = precipitación (mm/año) - DATO ESMALTLADO
C = condensación atmosférica (L/m²/día × 365) - CALCULAR
G = aporte subterráneo (L/año) - PERFORACIÓN + MEDICIÓN
E = evaporación - DATOS CLIMÁTICOS
T = transpiración vegetal - USAR COEFICIENTES
U = uso humano/agro - ESTIMAR CONSUMO

Objetivo: ΔW ≥ 0 (sistema estable)
```

### Cálculo Condensación Fog Harvesting
```
Rendimiento = Humedad_relativa × Velocidad_viento × Área_malla

Ejemplo:
- Humedad: 60%
- Viento: 5 m/s
- Malla: 100 m²
- Resultado: ~10 L/día
```

---

## Herramienta 2: Dimensionamiento Solar + Batería

```
Energía requerida = (Potencia_nodo × Horas_uso) + Pérdidas_sistema

Ejemplos:
- Bomba 2kW × 4h = 8 kWh
- LED 5W × 10 nodos × 12h = 0.6 kWh
- Total día: ~10 kWh

Paneles necesarios: 10 kWh ÷ 5h_insolación × 1.2 margen = 2.4 kW
Baterías: 10 kWh × 2 días_reserva = 20 kWh
```

---

## Herramienta 3: Cálculo Biochar + Retención Hídrica

```
Incremento_retención = Biochar_kg × Factor_retención

Factor_retención:
- Arena fina: 0.3 L/kg
- Arcilla: 0.5 L/kg
- Biochar: 0.8-1.2 L/kg (MEJOR opción)

Requerimiento: 10 ton/ha biochar → +300% retención hídrica
```

---

## Herramienta 4: Modelo de Expansión de Nodos

```
dN/dt = rN(1 - N/K)

Variables:
- r = tasa crecimiento (0.1-0.3 para zonas áridas)
- K = capacidad carrega (nodos máximos viables)
- N = nodos actuales

Tiempo doblado = ln(2) / r
```

---

## Herramienta 5: Cálculo Agricultura Vertical

```
Producción_m²_tradicional = X kg/m²/año
Producción_m²_vertical = X × 3-5 (multiplicador)

Agua_requerida_tradicional = Y L/kg
Agua_requerida_vertical = Y × 0.3 (reducción evaporación)

ROI_vertical = (Producción ↑ × 3) ÷ (Coste_instalación)
```

---

## Herramienta 6: Evaluación Costo-Beneficio Mallas

```
Coste_total = Material + Instalación + Vida_útil

Ahorro_suelo = Erosión_evitada × Valor_vegetación_recuperada

Payback_years = Coste_total ÷ Ahorro_anual_suelo
```

---

## Herramienta 7: Análisis Microclima

```
ΔT_superficie = -0.5°C × Densidad_vegetación (%)
ΔH_relativa = +10% × Corredores_verdes

Fórmulas:
- Temperatura reducida en zona sombregada
- Humedad aumentada por evapotranspiración controlada
```

---

## Herramienta 8: ROI Proyecto Completo

```
CAPEX_total = Σ(componentes) × Hectáreas

Flujo_ingresos_año = 
  Producción_agricola (€/ha × ha) +
  Créditos_carbono (€/ton_CO2 × toneladas) +
  Servicios_agua (+5-10%)

ROI_años = CAPEX_total ÷ Flujo_neto_año
```