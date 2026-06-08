# PLATAFORMA DIGITAL PIRS-1 - PASO 6

## Arquitectura Dashboard

```
Frontend: React + Leaflet + Chart.js
Backend: Node.js + PostgreSQL + Redis
IoT: MQTT broker + LoRa gateway
Mapas: OpenStreetMap + capas personalizadas
Datos: InfluxDB + Grafana
```

---

## API REST Endpoints

### GET /api/nodos
```javascript
Response: [
  {
    "id": "PIRS-001",
    "lat": 16.79,
    "lon": -3.00,
    "estado": "activo",
    "humedad": 25.3,
    "agua_hoy": 15,
    "energia_kwh": 4.2,
    "ultima_actualizacion": "2024-06-07T12:00"
  }
]
```

### GET /api/nodos/{id}/historico
```javascript
Response: [
  {"fecha": "2024-06-01", "humedad": 18.5, "agua": 8, "energia": 2.1},
  {"fecha": "2024-06-02", "humedad": 19.2, "agua": 12, "energia": 3.5},
  ...
]
```

### POST /api/mediciones
```javascript
Request: {
  "nodo_id": "PIRS-001",
  "humedad_suelo": 28.5,
  "temperatura": 34.2,
  "viento_ms": 4.5,
  "agua_litros": 15,
  "energia_wh": 2500
}
```

---

## Dashboard Web (React Component)

```jsx
// App.jsx
import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';

function Dashboard() {
  const [nodos, setNodos] = useState([]);
  
  useEffect(() => {
    fetch('/api/nodos')
      .then(r => r.json())
      .then(setNodos);
  }, []);

  return (
    <div className="dashboard">
      <MapaConNodos nodos={nodos} />
      <GraficoHumedad nodos={nodos} />
      <TablaResumen nodos={nodos} />
    </div>
  );
}

function MapaConNodos({ nodos }) {
  return (
    <MapContainer center={[15, -5]} zoom={7}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {nodos.map(nodo => (
        <Marker position={[nodo.lat, nodo.lon]} key={nodo.id}>
          <Tooltip>{nodo.id}: {nodo.humedad}% humedad</Tooltip>
        </Marker>
      ))}
    </MapContainer>
  );
}
```

---

## App Móvil (React Native)

### Pantalla Nodo
```javascript
// NodoScreen.jsx
<View style={styles.container}>
  <Text>Humedad: {medida.humedad}%</Text>
  <Text>Agua hoy: {medida.agua} L</Text>
  <Text>Energía: {medida.energia} Wh</Text>
  <Button title="Registrar medición" onPress={registrar} />
  <Button title="Alertar problema" onPress={alertar} />
</View>
```

### Funciones Offline
- Almacenamiento SQLite local
- Sincronización automática cuando hay red
- Fotos con GPS integrado
- Exportar CSV semanal

---

## Gateway LoRa + MQTT

### Configuración Raspberry Pi
```bash
# Instalar mosquitto
sudo apt install mosquitto mosquitto-clients

# Configurar puerto serial
sudo stty -F /dev/ttyS0 9600

# Bridge LoRa-MQTT
mosquitto_pub -t "nodos/BSLC-001" -m '{"humedad":25.3}'
```

### Script Python Bridge
```python
#!/usr/bin/env python3
import serial, json, paho.mqtt.publish as publish

ser = serial.Serial('/dev/ttyS0', 9600)

while True:
    line = ser.readline().decode()
    if line.startswith('{'):
        data = json.loads(line)
        publish.single(f"nodos/{data['id']}", json.dumps(data))
```

---

## Base de Datos PostgreSQL

### Schema
```sql
CREATE TABLE nodos (
    id VARCHAR PRIMARY KEY,
    lat DECIMAL(8,6),
    lon DECIMAL(9,6),
    fecha_creacion DATE
);

CREATE TABLE mediciones (
    id SERIAL PRIMARY KEY,
    nodo_id VARCHAR REFERENCES nodos(id),
    fecha TIMESTAMP DEFAULT NOW(),
    humedad DECIMAL,
    temperatura DECIMAL,
    viento DECIMAL,
    agua_litros DECIMAL,
    energia_wh DECIMAL
);

-- Índices para rendimiento
CREATE INDEX idx_mediciones_nodo_fecha ON mediciones(nodo_id, fecha);
CREATE INDEX idx_mediciones_fecha ON mediciones(fecha DESC);
```

### Querys Dashboard
```sql
-- Mediciones últimos 7 días
SELECT nodo_id, AVG(humedad) as humedad_media,
       SUM(agua_litros) as agua_total
FROM mediciones 
WHERE fecha > NOW() - INTERVAL '7 days'
GROUP BY nodo_id;

-- Tendencias crecimiento
SELECT strftime('%Y-%m', fecha) as mes,
       COUNT(DISTINCT nodo_id) as nodos_activos
FROM mediciones 
GROUP BY mes 
ORDER BY mes;
```

---

## Panel Grafana Configuración

### Dashboard JSON Import
```json
{
  "dashboard": {
    "title": "BSLC Mali Monitoring",
    "panels": [
      {
        "title": "Humedad suelo promedio",
        "type": "graphtable",
        "targets": [{"query": "SELECT mean(humedad) FROM mediciones"}]
      },
      {
        "title": "Producción agua diaria",
        "type": "barchart",
        "targets": [{"query": "SELECT sum(agua) FROM mediciones GROUP BY time(1d)"}]
      },
      {
        "title": "Estado nodos",
        "type": "geomap",
        "targets": [{"query": "SELECT lat, lon, humedad FROM nodos"}]
      }
    ]
  }
}
```

---

## Deployment Cloud

### Docker Compose
```yaml
version: '3'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: bslc
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes: ['./data:/var/lib/postgresql/data']

  mqtt:
    image: eclipse-mosquitto
    ports: ['1883:1883']

  grafana:
    image: grafana/grafana
    ports: ['3000:3000']
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  app:
    build: .
    ports: ['5000:5000']
```

### AWS/Azure One-Click
- EC2 t3.micro (1GB RAM)
- PostgreSQL RDS
- Route53 dominio bslc-mali.org
- CloudFront CDN para mapas