# PROMPT PARA AI - DISEÑO GENERADOR BSLC

## Prompt Principal para IA - Generador Magnético

```
DISEÑA UN GENERADOR ELECTRICO MAGNETICO BSLC CON ESTAS CARACTERÍSTICAS:

1. ROTOR CON IMÁN PERMANENTE (NEODIMIO N52)
   - 3 sectores asimétricos de polaridad
   - Radio 50mm, anchura 20mm
   - Geometría Halbach parcial para campo variable
   - Inercia mínima para arranque fácil

2. ESTATOR CON BOBINAS INDUCIDAS
   - 12 bobinas distribuidas 360°
   - 500 vueltas cada una, 1mm² cobre
   - Ubicación estratégica frente a rotor
   - Respuesta magnética rápida (<10ms)

3. SISTEMA DE CONMUTACIÓN ARDUINO
   - Arduino Nano + 12 MOSFET IRF540N
   - 3 sensores Hall A3144 para posición
   - PWM 1-10kHz control campo
   - Histeresis controlada 5-15%

4. ALIMENTACIÓN MÍNIMA SOLAR
   - Panel 20W 12V para sistema conmutación
   - Batería buffer 12V 7Ah opcional
   - Consumo total conmutación <50W
   - Auto-sostenimiento si generación > consumo

DISEÑA:
a) Geometría exacta de imanes en rotor
b) Distribución óptima bobinas estator  
c) Código Arduino con sequencia conmutación inteligente
d) Cálculo torque neto esperado (Nm)
e) Estimación RPM mínimo para auto-sostenimiento
f) Diagrama conexión completo (esquemático)
```

---

## Subprompts Específicos

### Prompt 1 - Geometría Imán Rotor
```
OPTIMIZA GEOMETRÍA IMÁN N52 PARA ROTOR BSLC:

- Área efectiva: 50mm radio × 20mm anchura
- 3 sectores con polaridades distintas
- Calcular campo magnético en cada posición
- Minimizar cogging torque (resistencia girar)
- Maximizar torque de arranque (empuje inicial)

INCLUYE:
- Diagrama polaridad rotor
- Campo B(n) en función posición
- Torque medio esperado (mNm)
```

### Prompt 2 - Secuencia Conmutación Inteligente
```
DISEÑA SECUENCIA CONMUTACIÓN PARA 12 BOBINAS (3 FASES):

ENTRADAS:
- Posición rotor (0-360°)
- Velocidad actual (RPM)
- Corriente bobinas (A)

SALIDAS:
- Secuencia conmutación óptima
- Delay entre fases (μs)
- Duración pulso (ms)
- Modo: arranque/auto-sostenido/generación

OBJETIVO:
- Maxima eficiencia energética
- Minima pérdida por conmutación
- Rotor acelera con mínimo input solar
```

### Prompt 3 - Cálculo Resonancia Magnética
```
CALCULA RESONANCIA MAGNETICA DEL SISTEMA:

PARAMETROS CONOCIDOS:
- Inductancia bobina: 5mH estimado  
- Resistencia bobina: 5Ω
- Capacitancia parasitic: 100nF estimado
- Frecuencia conmutación: variable 50-200Hz

FORMULA:
f_resonancia = 1/(2π√(LC))

DISEÑA:
- Circuito RLC paralelo para cada fase
- Condensador sintonización (valor exacto)
- Frecuencia óptima 87-150Hz
- Ganancia Q factor esperada
```

### Prompt 4 - Esquemático Electrónico Completo
```
DISEÑA ESQUEMÁTICO COMPLETO PARA GENERADOR BSLC:

COMPONENTES:
- Arduino Nano (control principal)
- 12 MOSFET IRF540N (conmutación bobinas)
- 12 diodos 1N5819 (protección contraflow)
- 3 sensores Hall A3144 (posición rotor)
- Fuente 12V 5A (panel solar)
- Condensadores filtro 1000μF
- Resistencias pull-up 10kΩ

ESQUEMÁTICO:
- Conexión MOSFET al Arduino (gate-source)
- Driver optoacoplador 4N35 cada fase
- Protección térmica termistor 10k
- Salida AC rectificada con diodo
- LED indicador estado por fase
```

---

## Parámetros de Diseño Clave

### Magnéticos
| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| Fuerza imán Br | 1.4 | Tesla |
| Coercividad Hc | 876 | kA/m |
| Energía producto Bhmax | 42 | MGOe |
| Temperatura trabajo | 80 | °C |

### Eléctricos
| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| Inductancia bobina | 5 | mH |
| Resistencia | 5 | Ω |
| Corriente nominal | 2.5 | A |
| PWM frecuencia | 1000 | Hz |

### Mecánicos
| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| Radio rotor | 50 | mm |
| Anchura rotor | 20 | mm |
| Inercia momento | 0.0001 | kg·m² |
| Fricción rodamiento | 0.001 | Nm |

---

## Métricas de Éxito

### Técnicas
- **RPM mínimo**: >500 rpm con 20W panel
- **Torque neto**: >0.01 Nm continuo
- **Eficiencia conmutación**: >90%
- **Auto-sostenimiento**: Si gen > cons

### Medibles
| Parámetro | Objetivo | Medida |
|-----------|----------|--------|
| RPM rotor | >1000 | Laser rpm |
| Corriente bobina | 2-3A | Multímetro |
| Tensión generada | >5V | Osciloscopio |
| Eficiencia energía | >70% | Power meter |

---

## Risk Analysis - Limitaciones Físicas

### Imposibles (Física Básica)
- ✗ Motor perpetuo sin input energía
- ✗ Energía magnética infinita
- ✗ Conmutación sin pérdidas eléctricas

### Posibles (Ingeniería Real)
- ✓ Rotor con campos desequilibrados
- ✓ Conmutación inteligente Arduino
- ✓ Auto-sostenimiento si eficiencia >70%
- ✓ Generación con muy bajo input solar