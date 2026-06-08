# HARDWARE SPEC - BSLC NODE ELECTRÓNICO

## Arquitectura Sistema Eléctrico

```
┌─────────────────────────────────────┐
│         NÚCLEO NODO BSLC            │
├─────────────────────────────────────┤
│ ☀️ PANEL SOLAR 300W (2 uds)         │
│         ↓                          │
│ 🔌 MPPT CONTROLLER 48V 60A         │
│         ↓                          │
│ 🔋 BATERÍA LFP 12V 100Ah (4 uds)  │
│         ↓                          │
│ ⚡ BUS DC 48V BACKBONE            │
│         ↓                          │
│ 🧠 INVERSOR BIDireccional 3kW      │
│         ↓                          │
│ ├── Bomba agua 48V 500W           │
│ ├── LED alumbrado (10 uds)         │
│ ├── Motor vertical cultivo 24V      │
│ └── Puerto carga external           │
└─────────────────────────────────────┘
```

---

## Lista Componentes Electrónicos

### Panel Solar (300W × 2)
| Componente | Especificación | Precio (€) |
|------------|----------------|------------|
| Panel fotovoltaico | Monocristalino 300W, 36 celdas | 80-120 |
| Soporte montaje | Aluminio ángulo 15° inclinado | 30-50 |
| Cable solar | 6mm² DC, 10m | 25-40 |
| Conector MC4 | Macho/hembra | 5-10 |
| **SUBTOTAL** | | **220-280 €** |

### Controlador MPPT
| Componente | Especificación | Precio (€) |
|------------|----------------|------------|
| Controlador MPPT | 48V 60A, LCD display | 150-200 |
| Fusible DC | 40A 500V | 15-25 |
| Termorretractil | Tubo 100mm | 10-15 |
| **SUBTOTAL** | | **175-240 €** |

### Batería LFP (48V sistema)
| Componente | Especificación | Precio (€) |
|------------|----------------|------------|
| Batería LFP | 12V 100Ah 4 uds | 350-450 |
| BMS | 48V 100A protection | 50-80 |
| Rack montaje | Acero galvanizado | 40-60 |
| **SUBTOTAL** | | **440-590 €** |

### Inversor Trifásico
| Componente | Especificación | Precio (€) |
|------------|----------------|------------|
| Inversor híbrido | 48V→380V 3kW | 200-300 |
| Contactores | 3 fases | 30-50 |
| Fusibles AC | 16A 400V | 20-30 |
| **SUBTOTAL** | | **250-380 €** |

### Carga Nodo
| Componente | Especificación | Precio (€) |
|------------|----------------|------------|
| Bomba sumergible | 48V DC 500W | 180-250 |
| LED nodo | 1-5W 12V con sensor | 15-25 × 10 = 150-250 |
| Motor cultivo | 24V BLDC 300W | 80-120 |
| Sensor humedad | Capacitivo 0-100% | 25-40 |
| Arduino Mega | + RTC + SD + LoRa | 35-50 |
| **SUBTOTAL** | | **470-700 €** |

### Gateway LoRa
| Componente | Especificación | Precio (€) |
|------------|----------------|------------|
| ESP32 LoRa | Heltec/Wemos | 20-30 |
| Gateway Raspberry | Pi 4 + ic880a | 80-120 |
| Antena 868MHz | 5dBi ganancia | 15-25 |
| **SUBTOTAL** | | **115-175 €** |

---

## Esquema Eléctrico Detallado

### Cableado DC 48V
```
Paneles (300W × 2):
  (+) MC4 --┬-- 6mm² -- Fuse 30A --+-- MPPT (+)
            │                       │
  (-) MC4 --┴-----------------------┴-- MPPT (-)
                                ↓
MPPT Controller 48V 60A:
  (+) Battery --+-- BMS (+) -- Battery Pack LFP
                │
  (-) Battery --┴-- BMS (-) -- Battery Pack LFP
                ↓
Battery Pack (4×12V 100Ah):
  (+) 48V -- Fuse 100A --+-- Inversor (+)
                         │
  (-) 48V ----------------┴-- Inversor (-)
```

### Cableado AC 380V
```
Inversor 3kW:
  (L1) ──┬── Bomba agua 500W
        │
  (L2) ──┼── Motor cultivo 300W
        │
  (L3) ──┼── Carga general
        │
  (N) ───┴── Neutro tierra
        ↓
  16A Disyuntor cada línea
```

---

## PCB Design Node Controller (KiCad)

### Layer Stack
```
Layer 1 (Top): Componentes activos
Layer 2 (GND): Plano tierra
Layer 3 (Power): +48V distribución
Layer 4 (Bottom): Componentes pasivos
```

### Componentes PCB
| Ref | Componente | Valor | Package |
|-----|------------|-------|---------|
| U1 | ESP32-WROOM | 38 pines | LQFP |
| U2 | SSR-40DA | 40A 600V | PCB |
| U3 | INA219 | Corriente 25A | SOIC |
| R1 | Resistencia | 10k | 0805 |
| R2 | Resistencia | 1k | 0805 |
| C1 | Condensador | 100µF | Radial |
| C2 | Condensador | 100nF | 0805 |
| D1 | LED | Rojo | 1206 |
| X1 | LoRa | SX1278 | SMA |
| J1 | Terminal | 48V DC | 2.54mm |
| J2 | Terminal | Sensor | 2.54mm |
| J3 | Terminal | Relay out | 3.5mm |

---

## Firmware Arduino (Código Base)

### main.ino
```cpp
#include <Wire.h>
#include <Adafruit_INA219.h>

#define RELAY_PUMP 22
#define RELAY_FAN 23
#define LED_STATUS 13
#define WATER_SENSOR A0

Adafruit_INA219 ina219;

void setup() {
  Serial.begin(115200);
  ina219.begin();
  pinMode(RELAY_PUMP, OUTPUT);
  pinMode(RELAY_FAN, OUTPUT);
  pinMode(LED_STATUS, OUTPUT);
  digitalWrite(LED_STATUS, HIGH);
}

void loop() {
  float voltage = ina219.getBusVoltage_V();
  float current = ina219.getCurrent_mA();
  int water_level = analogRead(WATER_SENSOR);
  
  // Control bomba si batería > 44V
  if (voltage > 44.0) {
    digitalWrite(RELAY_PUMP, HIGH);
  } else {
    digitalWrite(RELAY_PUMP, LOW);
  }
  
  // Enviar datos Serial + LoRa
  Serial.printf("V:%.1f,I:%.1fmA,W:%d\n", voltage, current, water_level);
  
  delay(60000); // 1 minuto
}
```

---

## Lista Compra Proveedores (EU/Africa)

### Proveedores Europa
| Componente | Distribuidor | Link |
|------------|--------------|------|
| Panel solar | SolarWorld/OpelSolar | www.solar-shop.eu |
| Batería LFP | BYD/CATL | www.battery-hub.de |
| Inversor | Victron/SMA | www.photovoltaics-store.com |
| Arduino | Distrelec/Conrad | www.distrelec.es |

### Proveedores África (Mali/Dakar)
| Componente | Distribuidor | Ciudad |
|------------|--------------|--------|
| Panel solar | SOLARCO | Bamako |
| Batería | BATSA | Dakar |
| Componentes electrónicos | ELECTROLAB | Bamako |
| Cableados | SOTRAC | Tombouctou |

---

## Manual Ensamblaje Hardware

### Paso 1 - Box Control
```
1. Cortar PCB 10×15 cm
2. Soldar ESP32 + conexiones
3. Instalar SSR + relé
4. Montar INA219 + cables
5. Conectar terminales
6. Test con multímetro
```

### Paso 2 - Cableado
```
1. Cable panel → MPPT (6mm² rojo/negro)
2. Cable MPPT → batería (6mm²)
3. Cable batería → inversor (35mm²)
4. Cable inversor → cargas (3×2.5mm²)
5. Instalar fusibles + etiquetas
```

### Paso 3 - Test Final
```
1. Verificar 48V sin cortocircuito
2. Test MPPT carga batería
3. Test inversor 220V bomba
4. Verificar comunicación LoRa
5. Registro funcionamiento 24h
```

---

## Coste Hardware Total (€)

| Categoría | Importe |
|-----------|---------|
| Solar + MPPT | 400-550 € |
| Batería LFP | 450-600 € |
| Inversor + AC | 250-400 € |
| Cargas + sensores | 500-750 € |
| Gateway LoRa | 120-200 € |
| **TOTAL HARDWARE** | **1,720-2,450 €** |