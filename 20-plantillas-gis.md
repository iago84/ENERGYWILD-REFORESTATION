# PLANTILLAS SIG Y VISUALIZACIÓN - ESTRATEGIA BSLC

## Plantilla 1: Script Python - Análisis de Nodos

```python
#!/usr/bin/env python3
"""Análisis de red de nodos BSLC"""

import json
import math

def calcular_expansion_nodos(nodos_iniciales, r, anos):
    """Calcula expansión logística de nodos"""
    K = 1000  # capacidad carrega zona
    nodos_finales = (K * nodos_iniciales * math.exp(r * anos)) / \
                     (K + nodos_iniciales * (math.exp(r * anos) - 1))
    return nodos_finales

def balance_hidrico(p, c, g, e, t, u):
    """Calcula balance hídrico del suelo"""
    return p + c + g - e - t - u

# Lectura datos JSON desde sensores
datos = {
    "nodo_id": "MALI-001",
    "humedad_suelo": 25.3,
    "temperatura": 32.1,
    "velocidad_viento": 4.5,
    "produccion_agua": 12.5
}
```

---

## Plantilla 2: Plantilla GeoJSON - Mapa de Nodos

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "nodo_id": "MALI-001",
        "estado": "activo",
        "humedad_suelo": 32.5,
        "produccion_agua": 15,
        "cultivos": ["nopal", "mijo", "moringa"]
      },
      "geometry": {
        "type": "Point",
        "coordinates": [-2.5, 15.5]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "corredor_id": "CORR-01",
        "tipo": "cortaviento",
        "densidad": 0.7,
        "orientacion": "NE-SW"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [[-2.5, 15.5], [-2.4, 15.4]]
      }
    }
  ]
}
```

---

## Plantilla 3: Script Arduino - Sensor Húmedad

```cpp
// Sensor de humedad suelo + temperatura
// Con SD logging y LoRa transmisión

#include <SD.h>
#include <SPI.h>

#define SENSOR_HUMEDAD A0
#define SENSOR_TEMP A1
#define SD_CS_PIN 4

File dataFile;

void setup() {
  Serial.begin(9600);
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("SD fail");
    return;
  }
}

void loop() {
  int humedad = analogRead(SENSOR_HUMEDAD);
  int temp = analogRead(SENSOR_TEMP);
  
  // Convertir a unidades reales
  float humedad_real = humedad * 100.0 / 1023.0;
  float temp_real = temp * 50.0 / 1023.0;
  
  // Registro SD
  dataFile = SD.open("datos.csv", FILE_WRITE);
  dataFile.println(millis() + "," + humedad_real + "," + temp_real);
  dataFile.close();
  
  delay(3600000); // 1 hora
}
```

---

## Plantilla 4: Configuración QGIS - Capas Sistema

```
CAPAS RECOMENDADAS:

1. VIENTO
   - Archivo: viento_harmattan.tif
   - Estilo: lineas de dirección + velocidad color
   - Simbología: grosor ∝ velocidad

2. AGUA
   - Archivo: acuiferos_mali.geojson
   - Estilo: puntos azules + nubes humedad
   - Atributos: profundidad, potencial

3. NODOS
   - Archivo: nodos_bslc.geojson
   - Estilo: círculos por estado (rojo=nuevo, verde=estable)
   - Atributos: producción, humedad, energía

4. CORREDORES
   - Archivo: corredores_verdes.geojson
   - Estilo: líneas verdes anchas
   - Atributos: densidad, especies

5. EROSIÓN
   - Archivo: riesgo_erosion.tif
   - Estilo: rojo (alto) → verde (bajo)
   - Clasificación: crítica, media, baja
```

---

## Plantilla 5: Dashboard Grafana - Visualización

```
QUERIES PROMEDIO:

1. AGUA
   SELECT mean(produccion_agua) FROM nodos WHERE time > now() - 7d

2. ENERGÍA
   SELECT mean(carga_bateria) FROM nodos WHERE time > now() - 1d  

3. SUELO
   SELECT mean(humedad_suelo) FROM sensores GROUP BY time(1h)

4. CULTIVO
   SELECT sum(cosecha_kg) FROM cultivos WHERE time > now() - 30d

PANEL GRÁFICOS:
- Temperatura/humedad tiempo real (gauge)
- Producción agua diaria (bar chart)
- Estado nodos mapa (geo panel)
- ROI acumulado (stat)
- Expansión nodos (time series)
```

---

## Plantilla 6: Formato CSV - Base de Datos Histórica

```csv
fecha,hora,nodo_id,humedad_suelo,temperatura_c,viento_mps,agua_captada_l,energia_wh,bateria_carga_pct,cultivo_tipo,cultivo_kg,mallas_kg,erosion_g
2026-06-07,12:00,MALI-001,25.3,32.1,4.5,12.5,250,85,nopal,5.2,100,0.1
2026-06-07,13:00,MALI-001,25.1,32.3,4.2,11.8,320,87,mijo,0,100,0
```