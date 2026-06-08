# templates-adicionales/ - Formatos de trabajo

## template-calculo-roi.xlsx (estructura)

```
HOJA 1: CAPEX
|A|B|C|D|
|---|---|---|---|
|Categoría|Item|Coste unidad (€)|Cantidad|
|Agua|Bomba solar|200|1|
|Agua|Cisterna HDPE|1500|1|
|Energía|Panel solar 300W|100|5|
|Energía|Batería LFP|400|4|

HOJA 2: FLUJO INGRESOS
|A|B|C|
|---|---|---|
|Año|Cultivo (€)|Servicios (€)|
|1|500|1000|
|2|1500|2000|
|3|3000|3500|

HOJA 3: ROI
=SUMA(CAPEX!C:D)/SUMA(FLujo!B:C)
=Años para amortizar: 4-7 años
```

---

## template-reporte-tecnico.md

# INFORME TÉCNICO NODO [ID-NODO]
**Período: ____/____/____ al ____/____/____**

## 1. RESUMEN EJECUTIVO
- Objetivo cumplido: ___/___
- Principales logros: ______________
- Problemas detectados: ____________

## 2. ESTADO SISTEMAS
### Agua
- Captación total: ___ L/día
- Almacenamiento: ___ % capacity
- Calidad: ___ (TDS/residual)

### Energía
- Generación solar: ___ Wh/día
- Batería: ___ % charge
- Consumo: ___ Wh/día

### Cultivo
- Superficie cultivada: ___ m²
- Producto principal: ______________
- Rendimiento: ___ kg

## 3. ANÁLISIS TÉCNICO
### Gráficos adjuntos
- [ ] Humedad suelo semanal
- [ ] Producción agua diaria
- [ ] Temperatura microclima
- [ ] Crecimiento vegetal

### Comparativas
- vs zona base: ___% mejora
- vs anterior: ___% evolución

## 4. RECOMENDACIONES
- Inmediatas: ______________
- Mediano plazo: ____________
- Escalado: ______________

---

## template-protocolo-biochar.txt

PROTOCOLO BIOCHAR PRODUCCIÓN - NODO [X]

FECHA INICIO: ____/____/____
OPERADOR: _______________

PASO 1 - CARGA LEÑA
- Volumen leña: ___ m³
- Tipo: ______________ (nopal, moringa, residuos)
- Humedad: ___ %

PASO 2 - CARBONIZACIÓN
- Temperatura máxima: ___ °C
- Tiempo: ___ horas
- Ventilación: ___ L/min

PASO 3 - ACTIVACIÓN
- Enmienda: KOH ___ %
- Tiempo activación: ___ min
- Enjuague final: ___ L

PASO 4 - ANÁLISIS
- pH: ___ (objetivo: 7-9)
- Retención agua: ___ %
- Área específica: ___ m²/g

RESULTADO FINAL: ___ kg biochar activo

---

## template-calculo-nodes.json

{
  "proyecto": "PIRS-1",
  "zona": "Mali-Sahel",
  "parametros": {
    "nodos_iniciales": 10,
    "capacidad_carga_K": 1000,
    "tasa_crecimiento_r": 0.2,
    "densidad_optima": 0.5
  },
  "simulacion": {
    "ano_0": 10,
    "ano_10": 100,
    "ano_25": 350,
    "ano_50": 650,
    "ano_100": 950
  },
  "kpi": {
    "humedad_objetivo": "+40%",
    "erosion_objetivo": "-60%",
    "productividad_objetivo": "x3"
  }
}