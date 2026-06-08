# ESQUEMA PCB - NODO BSLC (GERBER FILES)

## Archivos Gerber Lista

### capas_pcb/
- `top_copper.gbr` - Capa superior componentes
- `bottom_copper.gbr` - Capa inferior pasivos
- `top_silkscreen.gbr` - Serigrafía componentes
- `bottom_silkscreen.gbr` - Serigrafía conectores
- `top_mask.gbr` - Máscara soldadura
- `bottom_mask.gbr` - Máscara inferior
- `drill_file.drl` - Taladro vías
- `outline.gbr` - Contorno PCB

### Componentes Base64 (para fabricación)

#### ESP32 Pinout
```
GPIO ┌─────────────────────────────┐
┌────┤ RX2  TX2  D14  D27  D26  D25   │
│    │ D22  D21  D23  D22  D21  D19   │
│    │ D18  D5   D17  D16  D4   DN   │
│    │ D2   D15  D8   D7   D6   D1   │
│    │ D0   D9   D10  D11  D12  D13   │
└────┤ GND  EN   3V3  USB  Vin  GND   │
     └─────────────────────────────┘
```

---

## Firmware Completo Arduino

### nodo_bslc.ino
```cpp
/*
 * BSLC Node Controller v1.0
 * ESP32 + LoRa + Sensores
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_INA219.h>

// WiFi credentials
const char* ssid = "BSLC_WIFI";
const char* password = "bslc_nodo_2024";

// MQTT broker
const char* mqtt_server = "192.168.1.100";

// Pins
#define RELAY_PUMP    22
#define RELAY_FAN     23
#define RELAY_LED     21
#define WATER_SENSOR  34
#define SOIL_SENSOR   35

// Objects
Adafruit_INA219 ina219;
WiFiClient espClient;
PubSubClient client(espClient);

// Node config
const char* node_id = "BSLC-001";

void setup() {
  Serial.begin(115200);
  
  // Initialize pins
  pinMode(RELAY_PUMP, OUTPUT);
  pinMode(RELAY_FAN, OUTPUT);
  pinMode(RELAY_LED, OUTPUT);
  
  // Initialize sensors
  ina219.begin();
  analogReadResolution(12);
  
  // Connect WiFi
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();
  
  // Read sensors
  float voltage = ina219.getBusVoltage_V();
  float current = ina219.getCurrent_mA();
  int water_raw = analogRead(WATER_SENSOR);
  int soil_raw = analogRead(SOIL_SENSOR);
  
  // Convert readings
  float water_level = water_raw * 3.3 / 4095.0;
  float soil_moisture = soil_raw * 100.0 / 4095.0;
  
  // Publish to MQTT
  char payload[200];
  sprintf(payload, 
    "{\"voltage\":%.2f,\"current\":%.1f,\"water\":%.2f,\"soil\":%.1f}",
    voltage, current, water_level, soil_moisture);
  
  client.publish("bslc/nodes/BSLC-001/status", payload);
  
  // Control logic
  if (voltage > 46.0 && water_level < 2.5) {
    digitalWrite(RELAY_PUMP, HIGH);
  } else {
    digitalWrite(RELAY_PUMP, LOW);
  }
  
  delay(30000); // 30 segundos
}

void setup_wifi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect(node_id)) {
      client.subscribe("bslc/nodes/BSLC-001/commands");
    }
    delay(5000);
  }
}
```

---

## BOM Lista Fabricación PCB

### Componentes Surface Mount (SMD)
| Ref | Valor | Package | Cantidad |
|-----|-------|---------|----------|
| C1 | 100µF | Radial 6.3mm | 2 |
| C2 | 100nF | 0805 | 4 |
| R1 | 10k | 0805 | 2 |
| R2 | 1k | 0805 | 2 |
| D1 | LED | 1206 | 2 |
| U1 | ESP32-WROOM | LQFP-38 | 1 |
| U2 | INA219 | SOIC-8 | 1 |

### Componentes Through Hole
| Ref | Descripción | Package | Cantidad |
|-----|-------------|---------|----------|
| J1 | Terminal 48V | 2.54mm 4p | 1 |
| J2 | Terminal sensor | 2.54mm 6p | 1 |
| J3 | LoRa antenna | SMA | 1 |
| J4 | USB-C program | USB-C | 1 |
| K1 | SSR-40DA | PCB mount | 2 |

### PCB Specifications
- Dimensiones: 10cm × 15cm
- Capas: 2 (Top + Bottom)
- Espesor: 1.6mm FR4
- Terminado: HASL lead-free
- Mascarilla: Verde

---

## Firmware Bootloader

### platformio.ini
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200

lib_deps =
    adafruit/Adafruit INA219
    knolleary/PubSubClient
    sandeepmistry/arduino-LoRa
```

---

## Test Procedure Hardware

### Test 1 - Power Supply
```bash
# Multímetro check
VIN = 48V DC ±5%
GND = 0V relativo
3V3 = 3.3V ±2%
```

### Test 2 - Communication
```bash
# Serial monitor
AT
OK -- ESP32 responde
```

### Test 3 - Sensors
```bash
# INA219 query
INA219.begin()
Shunt voltage: 0.025V
Bus voltage: 48.7V
```

---

## Archivo Gerber Descarga

```bash
# Generar desde KiCad:
File > Fabrication Outputs > Gerber
  - Format: 4.6 (Gerber)
  - Layer: All layers
  - Output: ./gerber/

# Zip para fabricación:
zip gerber_bslc_node.zip gerber/*
```

---

## Lista Proveedores PCB Europe

| Servicio | Precio 10 uds | Tiempo |
|----------|---------------|--------|
| JLCPCB | 25-40 € | 7-14 días |
| PCBWay | 30-50 € | 5-10 días |
| EuroCircuits | 50-80 € | 3-5 días |