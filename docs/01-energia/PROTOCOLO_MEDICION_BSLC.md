# BSLC — Protocolo de Medición

> Procedimiento estandarizado para validar el generador BSLC.
> Versión 0.1 — Documento vivo sujeto a revisión tras cada campaña de prueba.

---

## 1. Instrumentos requeridos

| Instrumento | Rango mínimo | Precisión requerida |
|---|---|---|
| Fuente alimentación DC | 0-12 V, 5 A | ±1% |
| Tacómetro | 0-3000 RPM | ±5 RPM |
-| Dinamómetro / célula de carga | 0-1 N·m | ±0.01 N·m |
| Osciloscopio | 0-10 kHz | 8 bits, 1 MS/s |
| Voltímetro DC | 0-30 V | ±0.1 V |
| Amperímetro DC | 0-5 A | ±0.01 A |
| Cámara térmica (opcional) | -20 a 200 °C | ±2 °C |
| Cinta métrica / calibre | 0-150 mm | ±0.5 mm |

---

## 2. Variables a medir

| Variable | Símbolo | Unidad | Método |
|---|---|---|---|
| Velocidad rotor | ω | RPM | Tacómetro láser / encoder |
| Torque eje | τ | N·m | Dinamómetro |
| Corriente entrada | I_in | A | Shunt 0.1 Ω + voltímetro |
| Voltaje entrada | V_in | V | Multímetro DC |
-| Potencia entrada | P_in | W | V_in × I_in |
| Corriente salida | I_out | A | Analizador de carga |
| Voltaje salida | V_out | V | Multímetro / osciloscopio |
| Potencia salida | P_out | W | V_out × I_out |
| Temperatura bobinas | T_bob | °C | NTC 10k o cámara térmica |
| Posición angular | θ | ° | Sensor Hall + registro |

---

## 3. Secuencia de medición

### 3.1 Fase A — Punto muerto (sin conmutación)
1. Montar rotor en cojinetes sin bobinas
2. Impulso manual → medir tiempo de parada
3. Registrar ω_inicial y ω_final vs tiempo
4. Calcular deceleración α = dω/dt

**Propósito:** Determinar decaer mecánico de referencia (rozamiento, resistencia aire).
Sin esta referencia, cualquier aceleración con bobinas activas no tiene baseline.

### 3.2 Fase B — Arranque con 1 bobina
1. Conectar 1 bobina en posición 0°
2. Alimentar con 2 A durante 1 segundo
3. Medir ω(t) desde t=0 hasta ω_max o caída
4. Registrar τ_efectivo = J × α (si se conoce J)

**Propósito:** Validar si el campo magnético produce torque medible.

### 3.3 Fase C — Conmutación básica (3 bobinas)
1. Configurar 3 bobinas cada 120°
2. Programa Arduino: secuencia fija 60° por paso
3. Corriente: 2 A → 3 A → 4 A (3 pruebas separadas)
4. Medir RPM estacionario para cada corriente
5. Medir P_in y P_out simultáneamente

**Propósito:** Determinar relación I_entrada → RPM_salida → P_out.

### 3.4 Fase D — Carga eléctrica
1. Conectar resistencia variable como carga (10-100 Ω)
2. Variar carga y medir P_out para cada punto
3. Buscar punto de máxima eficiencia η = P_out / P_in
4. Identificar condición de autosostenimiento: ¿P_out > P_in en algún punto?

**Propósito:** Determinar si el sistema puede ser auto-sostenido o si requiere aporte externo continuo.

### 3.5 Fase E — Temperatura y estabilidad
1. Operar en condición de máxima potencia durante 10 minutos
2. Medir T_bob cada 60 segundos
3. Verificar si RPM se mantiene o decae por calentamiento
4. Apagar y registrar tiempo de enfriamiento

---

## 4. Formato de registro de datos

```csv
experimento_id,corriente_a,voltaje_v,rpm_rpm,torque_nm,t_bob_c,tiempo_s,p_out_w,p_in_w,observaciones
BSLC-001,2.0,12.0,0,0.000,25,0.0,0,24,arranque_manual
BSLC-001,2.0,12.0,45,0.012,26,0.5,0,24,bobina_1_activada
BSLC-001,2.0,12.0,120,0.008,28,1.0,0,24,decay_inicio
```

---

## 5. Criterios de aprobado / suspenso

| Criterio | Aprobado | Suspenso |
|---|---|---|
| Torque medible a 0 RPM | τ > 0.01 N·m | τ < 0.005 N·m |
| Aceleración neta positiva | ω aumenta > 20 RPM/s | ω no sube o cae |
| Eficiencia en carga | η > 10% | η < 5% |
| Estabilidad térmica | T_max < 80°C tras 10 min | T_max > 100°C |
| Autosostenimiento | P_out > 0.8 × P_in en algún punto | P_out siempre < P_in |

---

## 6. Acciones por resultado

### 6.1 Si APROBADO en Fase C y D
→ Avanzar a Nivel 2 (generador acoplado).  
→ Documentar geometría ganadora.

### 6.2 Si SUSPENSO en Fase B (torque no medible)
→ Rediseño de geometría (aumentar área magnética).  
→ Verificar polaridad real de imanes con brújula.

### 6.3 Si SUSPENSO en Fase D (P_out < P_in)
→ Evaluar si la relación puede mejorar con: a) más pares de polos, b) rotor de mayor inercia, c) menor distancia entrehierro.  
→ Si ninguna mejora funciona: rechazar concepto.

### 6.4 Si SUSPENSO en Fase E (térmico)
→ Reducir ciclo de trabajo (PWM < 70%).  
→ Añadir disipador o refrigeración por aire forzado.

---

## 7. Cadena de custodia de datos

- Cada campaña de pruebas se guarda en `data/experimentos/BSLC-YYYY-MM-DD.json`
- Incluir: configuración geométrica, condiciones ambientales, instrumentos usados, valores en bruto y procesados
- Incluir al menos 3 repeticiones por condición para estimar incertidumbre

---

## 8. Próxima acción recomendada

Construir **Prototipo Nivel 0** con materiales de coste mínimo y ejecutar **Fase A** (punto muerto) para obtener baseline mecánico antes de energizar bobinas.
