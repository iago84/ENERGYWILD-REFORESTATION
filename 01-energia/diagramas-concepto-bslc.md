# BSLC Magnetic Generator — Diagramas Conceptuales

> Borrador de diseño sin validar experimentalmente.  
> Documento de apoyo para revisión por especialista en electromagnetismo.

---

## 1. Diagrama de Bloques del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    BSLC Magnetic Generator                   │
├────────────┬────────────┬────────────┬──────────────────────┤
│  Panel     │  Arduino   │ Conmutador │  Rotor + Generador   │
│  Solar     │  Control   │ de Campo   │  (Inducción Secund.)  │
│  10-20 W   │  + PWM     │  3 fases   │  Salida eléctrica     │
└────────────┴────────────┴────────────┴──────────────────────┘
       │              │            │              │
       ▼              ▼            ▼              ▼
    [1] 12VDC      [2] Lógica   [3] Crea       [4] Genera
       Baja          Conmutación Campo         Potencia AC/DC
       Potencia      + Sensor   Magnético       para carga
                     Hall       Variable
```

**Flujo de energía (conceptual):**
- Entrada: 10-20 W solares → Arduino + conmutación
- Intermedio: Campos magnéticos variables (bobinas) empujan rotor de neodimio
- Salida: Rotación → inducción secundaria → potencia eléctrica útil

---

## 2. Diagrama de Flujo — Principio de Conmutación

```
Posición Rotor (sensor Hall)
         │
         ▼
   ┌─────────────┐
   │ ¿0°-45°?    │──Sí──► Bobina A ON │ Bobina B OFF │ Atracción
   ├─────────────┤
   │ ¿45°-90°?   │──Sí──► Bobina A OFF│ Bobina B ON │ Repulsión
   ├─────────────┤
   │ ¿90°-135°?  │──Sí──► Bobina A ON│ Bobina C ON │ Giro suave
   └─────────────┘
         │
         ▼ Secuencia cíclica 360°
```

**Objetivo:** Rotor "quiera" girar en todo momento, sin puntos muertos.

---

## 3. Diagrama de Geometría — Rotor Halbach Asimétrico

```
                    Vista frontal (diámetro 50mm)
                    
         ▲ Z (eje rotor)
         │
    ┌────┴────┐
    │  N      S │  ← Sector 1 (40mm, polaridad N→S)
    │         │
    │    S    N │  ← Sector 2 (30mm, polaridad S→N) 
    │         │
    │      N  S │  ← Sector 3 (20mm, polaridad N→S)
    └──────────┘
    
    Secuencia polaridades: N-S-N | S-N-S | N-S
    Radios decrecientes:    100%  85%    70% (desbalance deliberado)
```

**Efecto pretendido:** Campo no uniforme = torque neto sin necesidad de conmutación perfecta.

---

## 4. Diagrama de Principio Físico (Conceptual)

```
B_total(t) = B_permanente + B_inducido(t)

B_permanente: 1.4 T (neodimio N52, fijo en rotor)
B_inducido:   μ₀ · N · I(t) (variable desde bobinas estator)

Torque 𝜏 ≈ r · (B_total × I · L)

Objetivo diseño:
  - B_inducido modula B_total en fase con posición rotor
  - Resultado: torque siempre en dirección de giro
```

---

## 5. Diagrama de Secuencia de Conmutación (3 fases)

```
Tiempo →─────────────────────────────────►

Fase 1: Atracción
  [A=ON] ──► aproxima polo opuesto → rotor gira hacia bobina

Fase 2: Repulsión  
  [B=ON] ──► repele polo igual → rotor continúa giro

Fase 3: Asistencia (Híbrido)
  [A+C=ON] ──► campo guía → mantiene momentum

Ciclo cada 60° mecánicos ≈ 6 pulsos/rev (para 3 pares polos)
```

---

## 6. Diagrama de Resultado Pretendido

```
Velocidad vs Tiempo
(RPM)

 1200 │                          ╭──╮
      │                      ╭──╯  ╰──╮
  600 │       ╭──╮       ╭──╯        ╰──╮
      │   ╭──╯  ╰──╮   ╭╯              ╰──╮
    0 │───╯        ╰───╯                   ╰──►
      0    1s   2s   3s     arranque    auto-sostenido
      
Potencia vs RPM (curva característica teórica)
  
   P (W)
   50 │                    ╱￣￣￣￣￣
      │               ╭──╯
   25 │            ╭──╯
      │         ╭──╯
    0 │───────╭╯
      0      300    600    900   RPM
      
Nota: curva conceptual, no verificada experimentalmente.
```

---

## 7. Esquema de Conexiones — Controlador Arduino

```
Arduino Nano / Uno
         │
   5V ───┤──► Sensor Hall (A3144)
   GND ──┤──► Común
   D3 ───┤──► Driver MOSFET → Bobina A
   D4 ───┤──► Driver MOSFET → Bobina B  
   D5 ───┤──► Driver MOSFET → Bobina C
   A0 ───┤──► Lectura AC generador secundario
   A1 ───┤──► Lectura tensión salida
```

**Componentes clave (lista conceptual):**
- Sensor efecto Hall: detección posición rotor
- MOSFETs IRLZ44N: conmutación bobinas
- Diodos flyback: protección bobinas
- Capacitor 1000µF: filtrado entrada 12V

---

## 8. Diagrama de Flujo de Energía (Balance Energético Conceptual)

```
                ENTRADA                        PROCESO               SALIDA
                
    Panel 20W ──► [Arduino + MOSFETs] ──► Campos variables ──► Rotor gira ──► Generador 50-100W
         │              │                         │                      │
         ▼              ▼                         ▼                      ▼
    Batería        Control PWM          Conmutación magnética     Carga DC 12V
    12V 10Ah      + Sensor Hall             + Inducción            (objetivo)
                                                             
Supuesto conceptual: 20W entrada → 50-100W salida (factor de multiplicación por inercia rotórica)
**Requiere validación experimental — balance energético real sin confirmar**
```

---

## Referencias
- Diseño conceptual BSLC Magnetic Generator: `generador-bslc-magnetico.md`
- Arquitectura de patrones de imantado: `generador_patrones_imantado.py`
- Motor base (modelo conceptual): `motor_imantado.py`
