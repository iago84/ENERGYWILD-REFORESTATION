# BSLC Magnetic Generator — Ficha Técnica Conceptual

> Documento de síntesis del diseño conceptual.  
> No constituye especificación de producto ni garantiza viabilidad física.  
> Para handoff a especialista, ver `prompt-revision-especialista.md`.

---

## 1. Definición del Sistema

**Nombre:** BSLC Magnetic Generator  
**Tipo:** Sistema de generación eléctrica por conmutación magnética controlada  
**Arquitectura:** Rotor de imanes permanentes + estator de bobinas conmutadas por Arduino  
**Potencia objetivo:** 50 — 100 W de salida continua  
**Consumo de control:** ≤ 10 W (panel solar 10-20 W)  
**Relación entrada/salida pretendida:** 5:1 a 10:1 (factor de multiplicación energética declarado, no justificado numéricamente)

---

## 2. Principio de Funcionamiento (Hipótesis)

1. Un panel solar de baja potencia alimenta exclusivamente el sistema de control (Arduino) y la conmutación de campos magnéticos.
2. Las bobinas del estator generan campos magnéticos variables sincronizados con la posición del rotor.
3. El rotor, equipado con imanes de neodimio en geometría Halbach asimétrica, experimenta torque neto en todo momento sin puntos muertos.
4. La energía de giro residual (inercia rotórica) se convierte en electricidad mediante inducción secundaria en un generador acoplado.
5. El objetivo es que la energía generada supere a la consumida en la conmutación.

---

## 3. Componentes Principales

### 3.1 Rotor

| Parámetro | Valor |
|---|---|
| Radio exterior | 50 mm |
| Ancho axial | 20 mm |
| Peso estimado | 250 g |
| Inercia estimada | 1×10⁻⁴ kg·m² |
| Material imanes | Neodimio NdFeB N52 |
| Campo residual | 1.4 T |
| Geometría | Halbach asimétrica, 3 sectores |

**Distribución de sectores:**

| Sector | Radio efectivo | Polaridad inicio | Polaridad fin |
|---|---|---|---|
| 1 | 40 mm (80%) | N | S |
| 2 | 30 mm (60%) | S | N |
| 3 | 20 mm (40%) | N | S |

### 3.2 Estator (bobinas de conmutación)

| Parámetro | Valor |
|---|---|
| Número de bobinas | 3 (fase A, B, C) |
| Vueltas por bobina | 500 |
| Sección conductor | 1 mm² |
| Resistencia | ~5 Ω |
| Corriente de operación | 2 — 4 A |
| Campo objetivo en entrehierro | 0.1 — 0.3 T (estimado) |

### 3.3 Controlador

| Parámetro | Valor |
|---|---|
| Microcontrolador | Arduino Nano / Uno |
| Entrada | 12 V DC |
| Sensor posición | Sensor Hall (A3144) |
| Actuadores | 3× MOSFET IRLZ44N |
| Estrategia conmutación | 3 fases, 60° por paso |
| Frecuencia PWM | 50 — 200 Hz |

---

## 4. Diagrama de Arquitectura

```
Panel Solar 10-20W [12V]
        │
        ▼
   Arduino Nano
   ├── PWM control (50-200 Hz)
   ├── Sensor Hall (posición rotor)
   └── Control de histeresis
        │
        ▼
   Conmutador 3 fases
   ├── Bobina A → MOSFET + Diodo flyback
   ├── Bobina B → MOSFET + Diodo flyback
   └── Bobina C → MOSFET + Diodo flyback
        │
        ▼
   Rotor BSLC (3 imanes NdFeB N52, Halbach asimétrico)
        │
        ▼
   Generador secundario (inducción)
        │
        ▼
   Salida AC → Rectificador → Batería / Carga DC
```

---

## 5. Fórmulas Empleadas (Modelo Conceptual)

**Campo magnético total:**
```
B_total(t) = B_permanente + Σ B_inducido(t)
B_permanente = 1.4 T (neodimio N52)
B_inducido = μ₀ · N · I(t)  (simplificación)
```

**Torque electromagnético:**
```
τ = r × (B × I × L)
r = 50 mm (radio rotor)
L = 20 mm (ancho axial)
```

**Voltaje inducido:**
```
V = -N × dΦ/dt  (Ley de Faraday)
Φ = B × A × N
```

**Eficiencia instantánea:**
```
η = P_generada / P_consumo
P_consumo = Σ I² × R  (para cada bobina)
```

---

## 6. Parámetros de simulación (modelo Python actual)

| Parámetro | Valor por defecto |
|---|---|
| Paso temporal | 0.001 s |
| Ventana simulación | 1.0 — 5.0 s |
| Carga mecánica | 0.0 N·m (sin carga) |
| Estrategias conmutación | simple, optimizada, off |

**Estrategia "simple":** Activa bobinas cada 60° con corriente 2-3 A  
**Estrategia "optimizada":** Conmutación adelantada 15°, corrientes 1.5-4 A  
**Estrategia "off":** Sin corriente (freewheeling)

---

## 7. Curvas Características Pretendidas (No Validadas)

### 7.1 Arranque

```
Tiempo   Acción
0-0.5s   A ON (500 ms) → aceleración inicial
0.5-0.8s B ON (300 ms) → impulso adicional
0.8-1.0s C ON (200 ms) → estabilización
>1.0s    Ciclo repetitivo hasta RPM objetivo
```

### 7.2 Operación auto-sostenida

```
Objetivo RPM: 300 — 1000 RPM  
Torque mínimo mantenimiento: sin definir (pendiente de cálculo)  
Potencia generada objetivo: 50 — 100 W  
Potencia consumo estimada: 5 — 10 W  
Balance energético: +40 a +90 W (hipotético)
```

---

## 8. Incertidumbres y Riesgos Principales

| # | Riesgo | Descripción | Estado |
|---|---|---|---|
| 1 | Balance energético | 20 W entrada vs 50-100 W salida | No justificado |
| 2 | Torque de arranque | ¿Basta con 2-4 A para vencer inercia? | Sin cálculo revisado |
| 3 | Calentamiento bobinas | 2-4 A en 5 Ω → 20-80 W disipados | No modelado térmicamente |
| 4 | Sincronización rotor | Sensor Hall A3144 → resolución limitada | No caracterizado |
| 5 | Eficiencia global | Pérdidas por histéresis, Eddy currents, fricción | Desconocidas |
| 6 | Multiplicación energética | ¿Dónde entra la energía "extra"? | Concepto no fundamentado |

---

## 9. Lista de Materiales (Conceptual)

| Componente | Cantidad | Referencia | Comentario |
|---|---|---|---|
| Imán NdFeB N52, 40×10 mm | 1 | N52-40x10 | Sector 1 |
| Imán NdFeB N52, 30×10 mm | 1 | N52-30x10 | Sector 2 |
| Imán NdFeB N52, 20×10 mm | 1 | N52-20x10 | Sector 3 |
| Cable cobre 1 mm² | ~100 m | AWG 18 | 500 vueltas × 3 bobinas |
| Bobinas (prefabricadas) | 3 | Alternativa a arrollar | Simplifica construcción |
| Arduino Nano | 1 | ATmega328P | Control + PWM |
| Sensor Hall A3144 | 1 | Digital | Detección posición |
| MOSFET IRLZ44N | 3 | N-channel | Conmutación bobinas |
| Diodo flyback 1N4007 | 3 | — | Protección bobinas |
| Capacitor electrolítico | 1 | 1000 µF / 25V | Filtrado entrada |
| Panel solar 10-20 W | 1 | 12V | Entrada energética |
| Batería 12V | 1 | 7-10 Ah | Almacenamiento |
| Estructura rotor | 1 | Fibra de carbono / aluminio | Soportar imanes |
| Rodamiento | 2 | 618zz | Eje rotor |

---

## 10. Próximos Pasos Pendientes

1. Remitir `prompt-revision-especialista.md` a especialista en electromagnetismo.
2. Obtener veredicto de viabilidad (opción a/b/c/d).
3. Si viable con rediseño: actualizar especificaciones según recomendaciones.
4. Definir prototipo de validación experimental mínimo.
5. Modelar pérdidas térmicas y eficiencia global.
6. Caracterizar sensor Hall y latencia Arduino para conmutación.

---

## Documentos Relacionados

- `diagramas-concepto-bslc.md` — Diagramas visuales del sistema
- `prompt-revision-especialista.md` — Prompt estructurado para handoff
- `generador-bslc-magnetico.md` — Documento original de diseño
- `motor_imantado.py` — Modelo conceptual Python
- `generador_patrones_imantado.py` — Generador de geometrías Halbach
