# ESPECIFICACIONES TÉCNICAS - MOTOR BLDC BSLC

## Motor Brushless de Alta Eficiencia para Nodos Rurales

### Especificaciones Base

| Parámetro | Valor |
|-----------|-------|
| Potencia | 5-15 kW (según aplicación) |
| Voltaje | 48V DC (integrado con sistema solar) |
| Eficiencia | >95% |
| Velocidad | Variable 100-3000 RPM |
| Par máximo | 50-150 Nm |
| Protección | IP54 (polvo/agua) |

### Componentes

#### Rotor (Halbach Array)
- Imanes NpFeB (Neodimio) fuerza 45-52 MGOe
- Geometría tipo Halbach para maximizar campo unidireccional
- Peso reducido, momento de inercia bajo
- Material del recubrimiento: fibra de carbono

#### Estator
- Bobinas de cobre esmaltado (3 fases)
- Tooth/core de acero siliconado
- Optimizado FEM para flujo radial uniforme
- Espesor cable: 0.5-1.0 mm

#### Controlador (Inversor)
- FOC (Field Oriented Control)
- Frecuencia conmutación: 8-20 kHz
- Protecciones: sobrecalentamiento, sobre corriente
- Comunicación: CAN bus / RS485

### Aplicaciones en Sistema BSLC

| Aplicación | Potencia Requerida | Notas |
|------------|-------------------|-------|
| Bomba agua (subida) | 3-8 kW | Tracción directa |
| Tricotado geotextil | 2-5 kW | Alta velocidad |
| Ventilación vertical | 0.5-2 kW | Baja potencia continua |
| Transporte interno | 1-3 kW | Movimiento lineal |
| Generación recuperación | 5-15 kW | Modo generador |

### Recuperación Energética (Modo Generador)

Cuando el rotor es impulsado por fuerza externa:
- Bomba descendente → generación energética
- Vibración estructural → recuperación piezoeléctrica
- Movimiento agrícola → generación de bajo nivel

### Integración con Sistema Solar

```
☀️ Panel Solar (3-10 kW)
    ↓
🔌 MPPT Controller (48V)
    ↓
🔋 Baterías LFP (10-30 kWh)
    ↓
🧠 Inversor BLDC Bidireccional
    ↓
⚙️ Motor/Generador (aplicación)
```

### Ventajas para el Sistema BSLC

1. **Alta eficiencia** (>95%) reduce consumo energético total
2. **Bidireccional** permite recuperación energética
3. **Control preciso** de velocidad y torque para aplicaciones específicas
4. **Bajo mantenimiento** sin escobillas
5. **Operación silenciosa** no molesta fauna

### Limitaciones Técnicas

- Requiere electrónica de control activa
- No funciona sin energía externa (no es perpetuo)
- Coste inicial más alto que motores tradicionales
- Necesita sensores de posición para control óptimo