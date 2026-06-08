# BSLC — Prototipado Experimental

> Plan de construcción y validación del generador BSLC.  
> Objetivo: determinar si el concepto es físicamente viable y bajo qué condiciones reales.

---

## 1. Niveles de prototipado

| Nivel | Nombre | Objetivo | Coste estimado |
|---|---|---|---|
| 0 | Mesa de laboratorio | Validar principio básico de conmutación | 50-100 € |
| 1 | Rotor abierto | Medir torque y RPM con carga variable | 200-400 € |
| 2 | Generador acoplado | Medir eficiencia de conversión real | 500-800 € |

---

## 2. Prototipo Nivel 0 — Mesa de laboratorio

### 2.1 Embase mecánico
- Rodamiento rígido 618zz en soporte de aluminio
- Eje de acero inoxidable 6 mm
- Base MDF 200×200 mm con regleta milimetrada

### 2.2 Rotor magnético (versión mínima)
- 1 imán NdFeB N52, 20 mm diámetro × 10 mm
- Fijación mecánica en el eje (pegamento epoxi resistente)
- Marca de referencia angular para sensor Hall

### 2.3 Estator (versión reducida)
- 1 bobina de 500 vueltas, cable 0.5 mm²
- Núcleo de hierro dulce 20×20×10 mm (opcional)
- Posición ajustable en radial/axial para medición

### 2.4 Electrónica
- Arduino Nano
- Sensor Hall A3144
- MOSFET IRLZ44N + resistencia 220 Ω gate
- Fuente alimentación 12V 2A (laboratorio)
- Cables y protoboard

---

## 3. Prototipo Nivel 1 — Rotor abierto

### 3.1 Rotor completo
- 3 imanes N52 de 40 mm × 10 mm
- Disco de fibra de carbono / poliamida como base
- Centrado dinámico (runout < 0.1 mm)

### 3.2 Estator 3-fase
- 3 bobinas de 500 vueltas cada una
- Distribución cada 120°
- Driver MOSFET triple

### 3.3 Instrumentación
- Tacómetro láser o encoder óptico
- Dinamómetro de freno (correa + peso)
- Osciloscopio USB (para voltaje inducido)
- Datalogger temperatura (NTC 10k)

---

## 4. Protocolo de medición

Ver documento `PROTOCOLO_MEDICION_BSLC.md`.

---

## 5. Criterios de decisión

| Resultado | Decisión |
|---|--|
| RPM > 100 con conmutación activa | Avanzar a Nivel 1 |
| Torque medido < 0.001 N·m sin carga | Rediseño: revisar geometría |
| Consumo > generación real | Rediseño: concepto no viable |
| Temperatura bobinas > 80°C | Fallo por diseño: reducir corriente |
| RPM sostenidas > 500 sin consumo solar | Avanzar a Nivel 2 |

---

## 6. Seguridad

- Imanes de neodimio: mantener distancia > 20 cm con dispositivos electrónicos/pacemakers
- Superficies de imán: riesgo de pinzamiento
- Corrientes > 3 A: verificar calibre de cables y disipación
- Ventilación: bobinas pueden calentar a corriente continua

---


