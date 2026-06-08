# scripts-ejecucion/ - Herramientas rápidas

## tabla-referencia-rapida.md

# TABLA REFERENCIA RÁPIDA BSLC

## Dimensionamiento Express

| Parámetro | Fórmula | Resultado para 1 ha |
|-----------|---------|---------------------|
| Panels solar | kWh/día ÷ 5h sol | 6-8 paneles 300W |
| Baterías | kWh/día × 2 días | 20-30 kWh LFP |
| Biochar | 10-20 ton/ha | 10 m³ capa 50cm |
| Mallas | 10 mallas/ha | 500 m² captación |
| Nopal plantado | 200 plantas/ha | 2,000 m² cubierta |

## Cálculo Express Agua

```
Agua_día = Fog_harvest (L/m² × 100 malla) +
           Pozo_profundo (100 L/día bomba) +
           Condensación_nox (5 L/malla)
           
Ejemplo: 15 L + 100 L + 5 L = 120 L/día 1 ha
```

## Cálculo Express Energía

```
Energía_día = Paneles (6×300W×5h) +
              Viento_micro (2×300W×3h)
              
Ejemplo: 9,000 Wh + 1,800 Wh = 10,800 Wh/día
```

## Cálculo Express Cultivo

```
Rendimiento = Área_m² × Factor×
              Factor_suelo_vivo
              
Día árido (suelo_normal): 0.1 kg/m²
Día árido (suelo_vivo): 0.3 kg/m²
Con vertical: ×3-5 multiplicador
```

---

## quick-checklist-instalacion.txt

QUICKE CHECKLIST INSTALACIÓN NODO (1 HA)

□ Coordenadas GPS tomadas
□ Sitio nivelado y preparado
□ Cisterna enterrada instalada
□ Bomba solar operativa
□ Paneles montados (6 uds)
□ Baterías conectadas (4 uds)
□ Inversor configurado
□ Mallas 2x2m desplegadas
□ Biochar aplicado (10 m³)
□ Semillas nopal plantadas (200)
□ Semillas mijo (1 kg)
□ Sensor humedad instalado
□ Arduino + LoRa configurado
□ Sistema riego conectado
□ Iluminación LED nodo OK

TIEMPO ESTIMADO: 2-3 días 4 personas

---

## comandos-arduino-lora.sh

```bash
#!/bin/bash
# Comandos para Arduino + LoRa

# Monitor serie
arduino --port /dev/ttyUSB0 --baud 9600

# Flashear sketch
arduino --upload nodo_sensor.ino

# Test comunicación
echo "SEND_TEST" > /dev/ttyUSB0
cat /dev/ttyUSB0 &

# Backup datos SD
mkdir -p backup/$(date +%Y%m%d)
cp /dev/ttyUSB0 backup/$(date +%Y%m%d)/datos.txt
```

---

## script-sql-nodos.sql

```sql
-- Consultas rápidas para gestión nodos

-- Nodos con baja humedad (<20%)
SELECT id, lat, lon FROM nodos 
WHERE id IN (SELECT nodo_id FROM mediciones 
WHERE humedad_suelo < 20 
ORDER BY timestamp DESC LIMIT 1);

-- Nodos sin reporte 48h
SELECT id FROM nodos EXCEPT 
SELECT DISTINCT nodo_id FROM mediciones 
WHERE timestamp > datetime('now', '-48 hours');

-- Producción total mensual
SELECT strftime('%Y-%m', timestamp) as mes,
SUM(produccion_agua) as total_agua
FROM mediciones GROUP BY mes;
```

---

## api-endpoint-ejemplo.md

# API BSLC - Endpoints

## GET /api/nodos
```json
[{"id":"MALI-001","lat":15.5,"lon":-2.5,"estado":"activo"}]
```

## GET /api/nodos/{id}/mediciones
```json
[{"timestamp":"2024-06-07T12:00","humedad":25.3,"temp":32.1}]
```

## POST /api/mediciones
```json
{
  "nodo_id": "MALI-001",
  "humedad_suelo": 28.5,
  "temperatura": 31.2,
  "produccion_agua": 15.0
}
```

## GET /api/simulacion/expansion
```json
{"año_10":100,"año_25":350,"año_50":650}
```