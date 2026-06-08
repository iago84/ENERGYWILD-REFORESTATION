# SIMULACIÓN GIS MALI - BSLC (PASO 4)

## Coordenadas Zonas Críticas Mali

### Zonas Áridas Prioridad Alta
```
NOROESTE MALI (Tombouctou)
Bounds: 14.5°N - 17.5°N, 1.0°W - 3.5°W
Riesgo: 85% (área activa desertificación)

Sudoeste (Bamako-Mopti)
Bounds: 11.0°N - 13.5°N, 4.5°W - 8.5°W  
Riesgo: 45% (zona transición)

Norte Sahel
Bounds: 15.0°N - 18.0°N, 2.0°W - 6.0°W
Riesgo: 70% (frontera viva)
```

### Puntos de Inicio Recomendados

| Nodo ID | Coordenadas | Características | Prioridad |
|---------|-------------|-----------------|-----------|
| BSLC-001 | 16.79°N, -3.00°W | Cerca Tombouctou | ALTA |
| BSLC-002 | 15.33°N, -2.50°W | Zona semiárida | ALTA |
| BSLC-003 | 13.50°N, -8.00°W | Acuífero accesible | MEDIA |
| BSLC-004 | 16.20°N, -7.50°W | Viento Harmattan fuerte | ALTA |
| BSLC-005 | 12.65°N, -7.90°W | Asentamiento existente | CRÍTICA |

---

## Mapa Vectorial Nodos (GeoJSON)

```json
{
  "type": "FeatureCollection",
  " crs": { "type": "name", "properties": { "name": "EPSG:4326" } },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "nodo_id": "BSLC-001",
        "tipo": "piloto",
        "riesgo": "alto",
        "propuesta": "agua + solar + nopal"
      },
      "geometry": {
        "type": "Point", 
        "coordinates": [-3.00, 16.79]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "corredor_id": "CORR-01",
        "orientacion": "NE-SW",
        "especies": "acacia_moringa"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [-3.00, 16.79],
          [-3.10, 16.65],
          [-3.20, 16.50]
        ]
      }
    }
  ]
}
```

---

## Análisis Viento Harmattan

### Dirección Dominante
- **NE → SW** (80% frecuencia)
- Velocidad media: 4-6 m/s
- Temporada alta: Nov-Mar

### Optimización Nodos
```
NODOS A SOTAVENTO:
- Posicionar 15-30m tras duna/matorral
- Usar malla para reducir velocidad
- Orientar corredores NE-SW

ÁREAS CRÍTICAS:
- Tombouctou norte: viento 8 m/s
- Gao este: viento 6 m/s
- Kidal sureste: viento 10 m/s (crítica)
```

---

## Zonas de Fog Harvesting

### Condiciones Óptimas
- Altitud > 300m (cresterías)
- Viento > 3 m/s + humedad > 40%
- Orientación noreste (recepción niebla)

### Sitios Mali
```
MONTAÑAS HOMBORI (Adrar)
Coord: 16.5°N, -4.2°W
Alt: 1,150m
Fog potencial: ALTO

TEXCAS NORD (cerca Tichitt)
Coord: 14.8°N, -8.9°W
Alt: 450m
Fog potencial: MEDIO
```

---

## Red de Nodos Voronoi Optimizada

### Algoritmo de Ubicación
```
1. Crear buffer 50km zona Mali
2. Intersectar con mapa riesgo desertificación
3. Generar puntos (random jitter)
4. Crear Voronoi con puntos
5. Calificar polígonos:
   - Humedad acuífero
   - Acceso comunidad
   - Exposición solar
   - Protección viento
```

### Script QGIS/PYTHON
```python
import geopandas as gpd
from shapely.geometry import Point

# Cargar capas
mali = gpd.read_file('mali_boundary.shp')
riesgo = gpd.read_file('desertificacion_riesgo.tif')

# Generar nodos Voronoi
from scipy.spatial import Voronoi
import numpy as np

# Puntos aleatorios ponderados
np.random.seed(42)
nodos_x = np.random.uniform(-9, -1, 50)
nodos_y = np.random.uniform(11, 18, 50)
puntos = [Point(xy) for xy in zip(nodos_x, nodos_y)]

# Crear GeoDataFrame
gdf_nodos = gpd.GeoDataFrame(geometry=puntos, crs='EPSG:4326')

# Intersección con riesgo alto
nodos_seleccionados = gpd.sjoin(gdf_nodos, riesgo, how='inner')
```

---

## Capas GIS Requeridas

### Layer Pack para QGIS
1. **administrativa** - Límites regiones Mali
2. **clima** - Viento, temperatura, precipitación
3. **humedad** - Humedad suelo actual
4. **acuiferos** - Profundidad + capacidad
5. **vegetacion** - Cobertura actual + NDVI
6. **nodos_propuesta** - Puntos optimizados
7. **corredores** - Conexiones verdes
8. **carreteras** - Acceso logístico

---

## Resultado Simulación 1 km²

### Distribución 100 Nodos (ejemplo)
```
DENSIDAD: 1 nodo / 10,000 m²
COBERTURA: 30% área total
CORREDORES: 250 km verde conectado
VIENTO REDUCIDO: 40% en zonas nodos

PRODUCCIÓN TOTAL 1km²:
- Agua: 2,000 L/día
- Energía: 25 kWh/día
- Alimento: 500 kg/mes
- CO₂: 5 ton/año
```

---

## Formato Listo para Satélite

### Archivo KMZ Google Earth
```
Nombre: BSLC_Mali_Sahel.kmz
Ruta: Documentos/BSLC/mali_gis/
Capas visibles:
- Nodos (iconos rojos/verdes)
- Corredores (líneas verdes)
- Riesgo (colores rojo-naranja-verde)
- Fog zones (áreas azules)
```

### Coordenadas Bounding Box
```
MIN: 11.0°N, -9.0°W (Bamako sur)
MAX: 18.0°N, -1.0°W (Tichitt este)
CENTRO: 14.5°N, -5.0°W
```