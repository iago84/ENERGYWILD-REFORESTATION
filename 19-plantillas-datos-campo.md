# PLANTILLAS Y PROTOCOLOS DE DATOS DE CAMPO
## PIRS-1 - Sistema de recolección, almacenamiento y análisis

---

## 1. OBJETIVO
- Estandarizar la toma de datos en campo para todos los nodos PIRS-1.
- Garantizar comparabilidad entre zonas, temporadas y comunidades.
- Generar series históricas fiables para modelo PIRS-1 y ML.

---

## 2. VARIABLES CORE (mínimo indispensable)

| Variable | Unidad | Frecuencia | Método / Herramienta |Fuente referencia |
|-----------|--------|------------|----------------------|-------------------|
| Fecha | ISO 8601 | Cada visita | App / formulario | - |
| Nodo ID | alfanumérico | Cada visita | Código nodo | - |
| Humedad suelo 0-40 cm | % | Semanal | Sensor capacitivo + sonda manual | protocolos sensores |
| Temperatura aire | °C | Diaria | Estación meteorológica básica | - |
| Lluvia acumulada 24 h | mm | Diaria | Pluviómetro manual | - |
| Fog harvesting captado | L/día | Diaria | Caudalímetro + registro | fog-harvesting-sahel-mali.md |
| Nivel cisterna | % | Diaria | Sensor nivel / sonda | - |
| Carga batería | % | Diaria | Monitor inversor / Arduino | - |
| Supervivencia cultivos | % | Quincenal | Conteo visual por especie | - |
| Producción agrícola | kg | Cosecha | Báscula + registro | - |
| Erosión observada | escala 1-5 | Mensual | Foto punto fijo + plantilla | - |
| Observaciones libres | texto | Cada visita | App / cuaderno campo | - |

---

## 3. FORMULARIO BASE (CSV / App)

```csv
fecha,nodo_id,humedad_0_40,temp_aire,lluvia_24h,fog_L,nivel_cisterna_pct,bateria_pct,supervivencia_pct,produccion_kg,erosion_1_5,observaciones
2025-06-01,MALI-001,22,31,0,45,78,85,92,12.5,2,"riego goteo ok"
2025-06-02,MALI-001,20,33,0,38,75,82,92,0,2,"sin lluvia"
```

---

## 4. PROTOCOLO DE TOMA DE DATOS

### 4.1 Responsable por nodo
- **Monitor comunitario**: 1 persona por nodo, formada.
- **Supervisor regional**: 1 persona cada 20 nodos.
- **Backup técnico**: soporte remoto vía app.

### 4.2 Frecuencia y rigor
| Tipo dato | Frecuencia | Ventana temporal | Rigor |
|-----------|------------|------------------|-------|
| Meteorología básica | Diaria | 08:00 local | Alta |
| Humedad suelo | Semanal | Mismo día/hora | Alta |
| Supervivencia | Quincenal | Mismo operador | Media |
| Producción | Por cosecha | Exacta fecha | Alta |
| Erosión | Mensual | Mismo punto | Media |

### 4.3 Control de calidad
- Verificación semanal supervisor (10% aleatorio).
- Limpieza mensual (duplicados, outliers).
- Backup automático en servidor regional.

---

## 5. SISTEMA DE ALERTAS

| Condición | Alerta | Acción |
|-----------|--------|--------|
| Humedad < 15% 3 días | Naranja | Riego de emergencia |
| Fog < 5 L/día semana | Amarilla | Revisar malla |
| Batería < 20% | Roja | Inspección panel/cable |
| Supervivencia < 60% | Roja | Reporte técnico |

---

## 6. BASE DE DATOS CENTRAL (schema ejemplo)

```sql
CREATE TABLE nodos (
  nodo_id VARCHAR PRIMARY KEY,
  lat FLOAT,
  lon FLOAT,
  fecha_alta DATE,
  comunidad VARCHAR,
  zona VARCHAR
);

CREATE TABLE mediciones (
  id SERIAL PRIMARY KEY,
  nodo_id VARCHAR REFERENCES nodos,
  fecha DATE,
  humedad FLOAT,
  temp FLOAT,
  lluvia FLOAT,
  fog_litros FLOAT,
  bateria_pct FLOAT,
  supervivencia_pct FLOAT,
  produccion_kg FLOAT,
  erosion INT,
  observaciones TEXT
);
```

---

## 7. USO EN MODELO PIRS-1 Y ML

### Features para modelo ML
```python
features = [
  "humedad_suelo_media_7d",
  "fog_ultimos_7d",
  "bateria_promedio_7d",
  "supervivencia_especie",
  "lluvia_acumulada_30d",
  "temp_media_30d",
  "tasa_crecimiento",
]
target = [
  "produccion_kg_estimada",
  "riesgo_erosion",
  "recomendacion_riego",
]
```

### Dataset mínimo
- 100 nodos × 365 días = 36.500 filas/año.
- Mínimo viable: 1 año completo + 1 año de validación.

---

## 8. REFERENCIAS EN PROYECTO
- `checklists-detallados.md` → monitoreo inicial y avanzado.
- `plantillas-gis.md` → plantillas QGIS y Grafana.
- `protocolos-implementacion.md` → protocolo 3 (monitoreo remoto IoT).
