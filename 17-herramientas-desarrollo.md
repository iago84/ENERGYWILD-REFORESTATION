# scripts-bslc/ - Herramientas Python para análisis

## simulacion_nodos.py
```python
#!/usr/bin/env python3
"""Simulación de expansión de nodos BSLC"""

import math
import json

def modelo_logistico(t, n0=10, r=0.2, K=1000):
    """Modelo logístico de crecimiento de nodos"""
    N = (K * n0 * math.exp(r * t)) / (K + n0 * (math.exp(r * t) - 1))
    return int(N)

def balance_hidrico(P, C, G, E, T, U):
    """Balance hídrico simplificado"""
    return P + C + G - E - T - U

def roi_calculo(capex, ingresos_anuales):
    """ROI anual"""
    return round(capex / ingresos_anuales, 1)

if __name__ == "__main__":
    # Tabla expansión 100 años
    print("EXPANSIÓN NODOS POR AÑOS")
    print("-" * 30)
    for anos in [0, 5, 10, 15, 20, 25, 50, 75, 100]:
        nodos = modelo_logistico(anos)
        print(f"{anos:3d} años: {nodos:4d} nodos")
```

## calculo_suelo.py
```python
#!/usr/bin/env python3
"""Cálculo retención hídrica con biochar"""

def retencion_biochar(area_ha, biochar_ton):
    """Calcula mejora de retención hídrica"""
    base_retencion = 50  # L/m² sin biochar área árida
    mejora_biochar = biochar_ton * 0.8  # L/kg aproximado
    nueva_retencion = base_retencion + mejora_biochar * 1000  # L/ha
    return nueva_retencion

# Ejemplo: 1 ha con 20 ton biochar
print(f"Retención: {retencion_biochar(1, 20):.0f} L/ha extra")
```

## interfaz_lora.py
```python
#!/usr/bin/env python3
"""Interfaz LoRa para nodos remotos"""

import serial
import json

def leer_nodo(serial_port="/dev/ttyUSB0"):
    """Lee datos de nodo remoto"""
    ser = serial.Serial(serial_port, 9600)
    line = ser.readline().decode()
    try:
        datos = json.loads(line)
        return datos
    except:
        return None

def enviar_comando(nodo_id, comando):
    """Envía comando a nodo específico"""
    paquete = {"nodo": nodo_id, "cmd": comando, "id": hash(comando)}
    # Envío por LoRa
    return json.dumps(paquete)
```

## generar_reporte.py
```python
#!/usr/bin/env python3
"""Generador de reportes semanales"""

import csv
from datetime import datetime

def generar_csv(datos_lista, archivo="reporte_semanal.csv"):
    """Genera CSV con datos de campo"""
    with open(archivo, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['fecha', 'nodo', 'humedad', 'temp', 'agua', 'energia'])
        for fila in datos_lista:
            writer.writerow(fila)
```

---

# SQL - Base de datos nodos

## schema_nodos.sql
```sql
CREATE TABLE nodos (
    id TEXT PRIMARY KEY,
    lat REAL,
    lon REAL,
    fecha_instalacion DATE,
    estado TEXT CHECK(estado IN ('activo', 'inactivo', 'mantenimiento'))
);

CREATE TABLE mediciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nodo_id TEXT REFERENCES nodos(id),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    humedad_suelo REAL,
    temperatura REAL,
    viento REAL,
    produccion_agua REAL,
    energia_wh REAL,
    FOREIGN KEY (nodo_id) REFERENCES nodos(id)
);

CREATE TABLE cultivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nodo_id TEXT,
    tipo TEXT,
    plantado_m2 REAL,
    cosechado_kg REAL,
    agua_usada_l REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO nodos VALUES 
('MALI-001', 15.5, -2.5, '2024-06-01', 'activo'),
('MALI-002', 15.3, -2.7, '2024-06-15', 'activo');
```

---

# Plantilla dashboard web (HTML/CSS/JS)

## index.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>BSLC - Dashboard Mali</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div id="mapa-nodos"></div>
    <canvas id="grafica-humedad"></canvas>
    <script>
        // Conectar a API REST de nodos
        fetch('/api/nodos')
            .then(r => r.json())
            .then(data => actualizarMapa(data));
    </script>
</body>
</html>
```