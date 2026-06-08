# CHECKLISTS GENERADOR BSLC - EXPERIMENTO LABORATORIO

## Checklist Generador BSLC - Hardware

### Componentes Base
- [ ] Imán neodimio N52 (40mm × 10mm, 4 uds) - 15 €
- [ ] Arduino Nano + cable USB - 3 €
- [ ] MOSFET IRF540N (4 uds) + heatsink - 4 €
- [ ] Resistencias 5Ω/10W (8 uds) - 20 €
- [ ] Sensor Hall A3144 (3 uds) - 6 €
- [ ] Panel solar 20W 12V - 15 €
- [ ] Condensadores 1000µF (4 uds) - 5 €
- [ ] Diodos 1N5819 (8 uds) - 3 €
- [ ] Placa protoboard + cables - 10 €
- [ ] **TOTAL HARDWARE**: ~76 €

### Conexiones Eléctricas
- [ ] Diagrama esquemático armado
- [ ] MOSFET conectados a Arduino (gate-source)
- [ ] Flyback diodes instalados
- [ ] Fuente 12V conectada con fuse
- [ ] Sensores Hall alineados con rotor
- [ ] Test continuidad sin cortocircuitos
- [ ] Verificar polaridad panel solar

---

## Checklist Generador BSLC - Software

### Código Arduino
- [ ] Programa PWM control 12 resistencias
- [ ] Lectura sensores Hall 3 canales
- [ ] Cálculo posición rotor en tiempo real
- [ ] Secuencia conmutación programada
- [ ] Serial monitor debug activo
- [ ] EEPROM guardar última configuración
- [ ] Test compilar sin errores

### ML Preparación
- [ ] Dataset estructura definida (8 features)
- [ ] Script Python recolectar datos
- [ ] Modelo TensorFlow/Keras creado
- [ ] Red neuronal entrenada con simulación
- [ ] API REST endpoint para timing
- [ ] Dashboard web visualización
- [ ] Conexión MQTT Mosquitto

---

## Checklist Generador BSLC - Laboratorio

### Setup Mesas
- [ ] Mesa antiestática disponible
- [ ] Osciloscopio USB conectado
- [ ] Fuente DC 12V 10A preparada
- [ ] Multímetro TrueRMS listo
- [ ] Tachómetro láser para RPM
- [ ] Cámara fotografía setup
- [ ] Registro datos PC/notebook

### Protocolo Test
- [ ] Test 1: RPM sin resistencias (base)
- [ ] Test 2: RPM con R1 sola (2.2Ω)
- [ ] Test 3: RPM con patrón lineal 3 resistencias
- [ ] Test 4: RPM con Flower of Life (7 resistencias)
- [ ] Test 5: RPM con Árbol de la Vida (10 resistencias)
- [ ] Test 6: RPM con patrón Fibonacci
- [ ] Test 7: Medir generación eléctrica
- [ ] Test 8: Calcular eficiencia energía

### Medición Específica
- [ ] Voltaje panel sin carga (Voc)
- [ ] Corriente resistencias calor (A)
- [ ] Campo magnético con gaussímetro
- [ ] Temperatura resistencias (°C)
- [ ] RPM rotor inicial y estable
- [ ] Voltaje generación AC (V)
- [ ] Corriente generación (A)
- [ ] Potencia útil (W)
- [ ] Consumo total sistema (W)

---

## Checklist Generador BSLC - Optimización ML

### Analítica Primera
- [ ] 50 datos recolectados sin geometría
- [ ] 50 datos con Flower of Life
- [ ] 50 datos con Árbol de la Vida
- [ ] 50 datos con Fibonacci
- [ ] 50 datos con patrón aleatorio
- [ ] Dataset total: 250 ejemplos

### Entrenamiento Modelo
- [ ] Feature scaling aplicado
- [ ] Train/test split 80/20
- [ ] Modelo neuronal compilado
- [ ] Early stopping configurado
- [ ] Entrenamiento 500 epochs
- [ ] Validación accuracy > 85%
- [ ] Exportar modelo TensorFlow Lite

### Deploy ML
- [ ] Convertir a modelo Arduino
- [ ] Timing óptimo generado
- [ ] Test en hardware real
- [ ] Comparar predicho vs medido
- [ ] Ajustar hiperparámetros
- [ ] Guardar mejor modelo en EEPROM

---

## Checklist Generador BSLC - Validación Campo

### Auto-sostenimiento
- [ ] Generación medida: > 15W
- [ ] Consumo medido: < 12W
- [ ] Eficiencia: > 70%
- [ ] RPM estable 1 hora: ✓
- [ ] Temperatura estable: < 60°C
- [ ] Panel 20W suficiente: ✓

### Seguridad
- [ ] Fusible 10A instalado
- [ ] Protección térmica termistor
- [ ] Ventilación forzada disponible
- [ ] Apagado emergencia botón
- [ ] Voltaje seguro < 24V DC
- [ ] Aislamiento tierra verificado

---

## Checklist Generador BSLC - Escalado

### Kit Comunidad
- [ ] Lista materiales kit completo
- [ ] Precio kit objetivo: < 100 €
- [ ] Instrucciones paso a paso
- [ ] Video tutorial ensamblaje
- [ ] App móvil medir RPM
- [ ] QR código manual en PDF

### Implementación Regional
- [ ] 10 comunidades Mali contactadas
- [ ] 50 voluntarios capacitados
- [ ] 100 kits fabricados
- [ ] Datos recopilados 30 días
- [ ] Modelo ML entrenado datos reales
- [ ] Patrón óptimo comunidad encontrado
- [ ] Auto-sostenimiento validado campo

---

## Checklist Generador BSLC - Paper Científico

### Datos Experimentales
- [ ] 1000 mediciones registradas
- [ ] Eficiencia promedio: X%
- [ ] RPM máximo alcanzado: Y rpm
- [ ] Geometría óptima identificada
- [ ] Comparación con teoría

### Resultados
- [ ] Auto-sostenimiento confirmado: ✓/✗
- [ ] Métricas KPIs completadas
- [ ] Gráficos generados
- [ ] Estadísticas ANOVA realizadas
- [ ] Conclusiones técnicas redactadas

### Envío
- [ ] Paper Nature Sustainability formateado
- [ ] Video YouTube experimento
- [ ] Repo GitHub código abierto
- [ ] Patent provisional geometría
- [ ] Presentación congreso solar