# PROMPTS AI - GENERADOR BSLC (ESPECÍFICOS)

## Prompt 1: Geometría Imán Asimétrico Rotor

```
DISEÑA EL DISEÑO GEOMÉTRICO EXACTAMENTO DE 3 IMÁNES PERMANENTES EN UN ROTOR CILÍNDRICO:

- ROTOR: cilindro 50mm radio × 20mm anchura
- IMÁN 1: sector 0-120°, polaridad N-S-N (3 imánes 20mm × 5mm)
- IMÁN 2: sector 120-240°, polaridad S-N-S (3 imánes 20mm × 5mm)  
- IMÁN 3: sector 240-360°, polaridad N-S (2 imánes 20mm × 5mm)

OBJETIVO:
Crear un campo magnético NO uniforme que genere un torque variable constante

CALCULOS REQUERIDOS:
- Campo magnético B(θ) para cada ángulo θ
- Torque medio B_avg = ∫B(θ)dθ/360
- Cogging torque mecánico estimado
- Momento inercia rotora J_rotor
- Energy barrier mínima para arranque

ENTRGAR:
1. Diagrama polaridad con dibujo ASCII
2. Fórmula torque medio (Nm)
3. Estrategia conmutación estator
```

---

## Prompt 2: Estator Bobinas Optimizado

```
DISEÑA 12 BOBINAS ESTATORAS PARA INTERACTUAR CON ROTOR ASIMÉTRICO:

GEOMETRÍA:
- 12 bobinas distribuidas cada 30°
- 500 vueltas cada una, alambre cobre 1mm²
- Radio media bobina 45mm
- Anchura 15mm

CONEXIONES:
- Fase A: bobinas 0°, 120°, 240°
- Fase B: bobinas 30°, 150°, 270°
- Fase C: bobinas 60°, 180°, 300°

PARAMETROS ELÉCTRICOS:
- L = 5mH inductancia
- R = 5Ω resistencia
- I_rms = 2A corriente operativa

CALCULA:
- Campo H(θ) cuando bobina encendida
- Fuerza de interacción rotor-bobina
- Timing offset óptimo (grados)
- Corriente necesaria 2-3A

SALIDA:
Tabla timing offset (bobina vs ángulo rotor)
```

---

## Prompt 3: Control Arduino con PWM Inteligente

```
DISEÑA CÓDIGO ARDUINO NANO PARA CONTROLAR 12 MOSFET CON PWM:

ENTRADAS:
- Sensor Hall A3144 (detecta imán rotor)
- Variable velocidad actual (calculada)
- Potenciometro ajuste timing (0-100%)

SALIDAS:
- PWM pins ~3,~4,~5,~6 (4 pares MOSFET)
- Serial monitor debug
- LED indicador estado

ALGORITMO:
1. Leer posición rotor (0-360°)
2. Calcular fase activa según tabla
3. Encender MOSFET correspondiente PWM
4. Delay 5-20ms (ajustable)
5. Apagar y siguiente fase
6. Registrar RPM y corriente

OPTIMIZACIONES:
- Dead time 1μs entre conmutaciones
- Duty cycle variable 30-80%
- Histeresis velocidad controlada
- Modo arranque vs sostenido

CONSTRUCCIONES:
- Protección sobrecalentamiento
- Watchdog timer 5 segundos
- EEPROM guardar ajustes
```

---

## Prompt 4: Análisis Energético Realista

```
ANALIZA SI EL SISTEMA PUEDE SER AUTO-SOSTENIDO:

DATOS CONOCIDOS:
- Panel solar: 20W 12V (máximo 1.6A)
- Consumo Arduino: 50mA continuo
- Consumo MOSFET: 5mA gate cada uno (12 = 60mA)
- Corriente bobinas: 2.5A × 3 bobinas = 7.5A (solamente 1 encendida)

CALCULOS:
1. Corriente requerida conmutación (7.5A)
2. Voltaje necesario MOSFET drive (12V)
3. Potencia consumida: 12V × 7.5A = 90W
4. ¿20W panel puede alimentar 90W consumo?

PROBLEMA IDENTIFICADO:
Consumo > producción disponible

SOLUCIÓN REQUERIDA:
- Reducción corriente bobina
- Conmutación ultra breve (<1ms)
- Batería buffer 7Ah
- Panel mayor 50W

¿QUÉ CAMBIO HACER PARA AUTO-SOSTENIMIENTO?
```

---

## Prompt 5: Esquema Conexión Electrónica Completo

```
DISEÑA ESQUEMA CONEXIÓN COMPLETO ARDUINO + MOSFET + BOBINAS:

PUERTOS ARDUINO NANO:
- D2,D3,D4: Control PWM fase A (3 bobinas)
- D5,D6,D9: Control PWM fase B (3 bobinas)  
- D10,D11,A0: Control PWM fase C (3 bobinas)
- A1,A2,A3: Sensores Hall
- D13: LED status

MOSFET IRF540N CONEXIÓN:
- Drain → bobina positiva
- Source → ground común
- Gate → Arduino (con 100Ω resistencia)
- Flyback diode 1N5819 antiparalelo bobina

ALIMENTACIÓN:
- Vin Arduino ← panel solar 12V
- Capacitor 4700μF 25V en Vin
- Fusible 10A en alimentación

PROTECCIONES:
- Termistor 10k en MOSFET (temperatura)
- Resistencia pull-up 10k sensores Hall
- Diodo 1N4007 en Vin protección polaridad

DIAGRAMA ASCII:
ArDUINO → MOSFET → BOBINA → LED INDICADOR
```

---

## Prompt 6: Optimización Parameter Tuning

```
CREA TABLA DE AJUSTES ÓPTIMOS PARA GENERADOR BSLC:

VARIABLES CONTROLABLES:
1. PWM frequency: 100-10000 Hz
2. Duty cycle: 10-90%
3. Delay conmutación: 1-50 ms
4. Corriente bobina: 1-5A
5. Número bobinas activas: 1-3

TABLA AJUSTES:

| RPM objetivo | PWM Freq | Duty | Delay | Corriente (A) | Resultado esperado |
|--------------|----------|------|-------|---------------|-------------------|
| Arrancar (500)| 1000 | 80% | 50 | 3.5 | Aceleración rápida |
| Sostener (1000)| 5000 | 50% | 10 | 2.5 | Operación estable |
| Generar (2000)| 10000 | 30% | 5 | 2.0 | Máx eficiencia |

ALGORITMO TUNING:
1. Medir RPM actual
2. Si RPM < objetivo: aumentar duty
3. Si corriente > 3A: reducir delay
4. Si temperatura > 60°C: reducir corriente
5. Guardar optimo en EEPROM
```

---

## Prompt 7: Mediciones Laboratorio Controladas

```
DISEÑA PROTOCOLO LABORATORIO PARA VALIDAR GENERADOR BSLC:

EQUIPO NECESARIO:
- Osciloscopio 100MHz (Tektronix)
- Fuente DC 12V 10A
- Multímetro TrueRMS
- Tachómetro láser
- Power analyzer 200W
- Magnetic field meter

MEDICIONES:

1. POSICIÓN ROTOR
   - Sensor Hall → ángulo (0-360°)
   - RPM inicial sin carga
   - Time constant conmutación

2. CAMPO MAGNÉTICO
   - Gauss en eje rotor (sensor Hall)
   - Variación B vs ángulo
   - Mapa campo 3D (opcional)

3. ENERGÍA ELÉCTRICA
   - Voltaje generado (open circuit)
   - Corriente cortocircuit
   - Potencia disponible
   - Eficiencia conmutación

4. EFICIENCIA SISTEMA
   - Input solar panel (W)
   - Output generación (W)
   - Pérdidas mecánicas (W)
   - Auto-sostenimiento = output - input > 0

RESULTADO ESPERADO:
Motor genera 10-20W si eficiencia > 70%
```