# GENERADOR BSLC MAGNETICO - AI DESIGN

## Concepto del Sistema

**Panel solar mínimo (10-20W)** → **Arduino** → **Commutador** → **Campos magnéticos variables** → **Rotor imán permanente** → **Generación eléctrica**

El panel no alimenta carga directa. Alimenta SOLO el sistema de conmutación para crear "empuje magnético controlado" que hace girar el rotor.

---

## Arquitectura Electromagnética

```
┌─────────────────────────────┐
│  SOLAR PANEL 20W MIN            │
│  12V DC (minimamente eficiente)│
└────────────┬─────────────────┘
             ↓
┌────────────┴─────────────────┐
│  ARDUINO NANO                │
│  - PWM control               │
│  - Timer preciso             │
│  - Histeresis controlada     │
└────────────┬─────────────────┘
             ↓
┌────────────┴─────────────────┐
│  COMMUTADOR DE CAMPO         │
│  ├─ Bobina 1 (inducción A)  │
│  ├─ Bobina 2 (inducción B)  │
│  └─ Bobina 3 (inducción C)  │
└────────────┬─────────────────┘
             ↓
┌────────────┴─────────────────┐
│  ROTOR CON IMÁN PERMANENTE    │
│  - Neodimio NdFeB N52        │
│  - Geometría asimétrica      │
│  - CoG equilibrado          │
└────────────┬─────────────────┘
             ↓
┌────────────┴─────────────────┐
│  GENERADOR ELÉCTRICO         │
│  - Inducción secundaria      │
│  - 3 fases rectificadas      │
└────┬───────┬───────┬─────────┘
     ↓       ↓       ↓
  BATERÍA   LED     CARGA EXT
```

---

## Principio de Conmutación Magnética

### Campo Magnetico Total
```
B_total(t) = B_permanente + Σ[i=1..n] B_inducido(t)

Donde:
B_permanente = 1.4 Tesla (neodimio N52)
B_inducido = μ₀ * n * I(t) (bobina)

Objetivo: B_total variable → torque variable → aceleración controlada
```

### Conmutación Inteligente
```
ALGORITMO ARDUINO:

// Posición rotor (sensor Hall)
int pos = leer_posicion();

// Campos de conmutación
if (pos > 0 && pos < 45) {
  ENCENDER(A); APAGAR(B,C);  // Atracción rotor
} else if (pos > 45 && pos < 90) {
  APAGAR(A); ENCENDER(B); // Repulsión rotor
} else if (pos > 90 && pos < 135) {
  APAGAR(B); ENCENDER(C,A); // Giro suave
}
// Repetir ciclo
```

---

## Diseño Rotor Imán Permanente

### Geometría Halbach Asimétrica
```
IMÁN 1: Neodimio N52, 40mm × 10mm, polaridad N-S-N
IMÁN 2: Neodimio N52, 30mm × 10mm, polaridad S-N-S
IMÁN 3: Neodimio N52, 20mm × 10mm, polaridad N-S

Secuencia: N-S-N | S-N-S | N-S 
Efecto: Campo no uniforme, momento variable con posición
```

### Rotor Físico
- Radio: 50mm
- Anchura: 20mm
- Peso: 250g (neodimio + fibra de carbono)
- Inercia: 0.0001 kg·m²
- CoG: Centrado ±1mm

---

## Bobinas Inducidas (Estator)

### Configuración 3-12 fases
```
BOBINA 1: 500 vueltas, 1mm², 5Ω
BOBINA 2: 500 vueltas, 1mm², 5Ω  
BOBINA 3: 500 vueltas, 1mm², 5Ω

Parámetros:
N = 500 (vueltas)
μ = 2000 (hierro)
A = 10mm² (sección)
L = 50mm (longitud)
```

### Respuesta Electromagnética
```
Tiempo conmutación: 5-20 ms (PWM 50-200 Hz)
Corriente bobina: 2-4A (con 12V)
Campo inducido: 0.1-0.3 Tesla
Potencia consumo: 24-48W (solo conmutación)
```

---

## Arduino Controlador Inteligente

### Código Control Campo Magnético
```cpp
/* BSLC Magnetic Commutator v1.0 */

#define COIL_A 3
#define COIL_B 4  
#define COIL_C 5
#define HALL_SENSOR 2

#define PWM_FREQ 1000
#define DEAD_TIME 500 // microseconds

// Posición rotor
volatile int rotor_pos = 0;

void setup() {
  pinMode(COIL_A, OUTPUT);
  pinMode(COIL_B, OUTPUT);
  pinMode(COIL_C, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(HALL_SENSOR), 
                  leer_posicion, CHANGE);
}

void loop() {
  // Estrategia conmutación inteligente
  switch(rotor_pos) {
    case 0:
      // Fase atracción
      digitalWrite(COIL_A, HIGH);
      digitalWrite(COIL_B, LOW);
      break;
    case 45:
      // Fase repulsión  
      digitalWrite(COIL_A, LOW);
      digitalWrite(COIL_B, HIGH);
      break;
  }
}

// Generación energía
int generar_energia() {
  // Inducción secundaria
  int voltaje_gen = leer_ac(A0); // AC del generador
  int corriente_gen = leer_dc(A1); // Corriente salida
  return (voltaje_gen * corriente_gen);
}
```

---

## Secuencia Conmutación Óptima

### Fase 1 - Arranque
```
Objetivo: Inercia rotor > 50 rad/s
Secuencia:
1. A ON (500ms) → aceleración
2. B ON (300ms) → impulso
3. C ON (200ms) → estable
4. AOFF (100ms) → librea rotor
5. Repetir hasta velocidad mínima
```

### Fase 2 - AutoSostenido
```
Objetivo: 300-1000 rad/s constante
Secuencia:
- Conmutar 3 bobinas en secuencia
- Timing variable para resonancia
- Corriente mínima para persistencia
- Recuperar energía rotativa
```

### Fase 3 - Generación
```
Objetivo: Máxima potencia generada
Secuencia:
- Rotor drive + generación sincronizada  
- Regulación tensión salida 12V/5V
- Rectificación 3 fases
- Almacenamiento batería
```

---

## Análisis Potencia Requerida

### Consumo Sistema
```
Panel solar: 20W mínimo
Arduino: 0.5W standby
Commutación: 30W (bobinas 3 × 10W)
Sensores: 1W

TOTAL CONSUMO CONMUTACIÓN: 32W
```

### Generación Potencial
```
Rotor rpm: 1000-3000 (dependiendo eficiencia)
Imán fuerza: 1400 Gauss
Generador inductivo: 30-60 mV/rpm
Rectificación: 85% eficiencia

GENERACIÓN: 10-30W (posible auto-sostenimiento)
```

---

## Prototipo DIY Componentes

### Lista Compra Mínima
| Componente | Especificación | Precio |
|------------|----------------|--------|
| Imán neodimio | N52, 20mm × 5mm, 4 uds | 15 € |
| Bobina | Cuivre 1mm², 500m, 3 uds | 30 € |
| Arduino Nano | Clone compatible | 3 € |
| MOSFET | IRF540N 4 uds | 2 € |
| Driver MOSFET | IR2104 2 uds | 3 € |
| Sensor Hall | A3144 2 uds | 2 € |
| Panel solar | 20W monocristalino | 15 € |
| Diodes | Rectificar 1N5819 6 uds | 3 € |
| **TOTAL** | | **73 €** |

---

## Prueba Laboratorio Controlada

### Setup
- Rotor con imán asimétrico
- Estator con 3 bobinas
- Arduino Nano controlando MOSFETs
- Panel solar 20W alimentando
- Osciloscopio + multímetro

### Medidas
1. Posición rotor (Hall)
2. Corriente bobina (INA219)
3. Velocidad rotativa (laser)
4. Tensión generada (multímetro)
5. Eficiencia energía (power meter)

---

## Optimización Geometría Imán

### Configuración Asimétrica Efectiva
```
POSICIÓN IMÁN ROTOR:
Sector 1 (0-120°): N-S-N (campo intenso)
Sector 2 (120-240°): S-N-S (campo medio)  
Sector 3 (240-360°): N-S (campo débil)

Resultado: 
Torque variable sin equilibrio
Auto-desequilibrio perpetuo
Rotor "quiere" girar siempre
```

### Configuración Estator
```
BOBINA 1 (atracción): Coil a 0°
BOBINA 2 (repulsión): Coil a 120°  
BOBINA 3 (neutral): Coil a 240°

Timing conmutación: 10-30° adelantado a rotor
Objetivo: Acelerar rotor en "valle" magnético
```

---

## Consideraciones de Energía Real

### Pérdidas Inevitables
- Corriente bobina: 30W consumo
- Inercia rotor: 1-5W mecánicos
- Rectificación: 10-15% pérdida
- Fricción: 5-10% mecánicos

### Resultado Real
Si generación = 30W y consumo = 32W:
- Sistema NO es perpetuo
- Pero es auto-regulado
- Funciona con muy bajo input solar
- Mejor eficiencia posible con resonancia