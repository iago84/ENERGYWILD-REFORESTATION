# BSLC — Optimización de Rotación y Generación Híbrida

> Concepto sin validar: usar el giro del rotor BSLC para accionar
> ventiladores/ turbina eólica miniatura, añadiendo una vía de generación
> aerodinámica complementaria a la magnética.

---

## Hipótesis base
El rotor BSLC ya gira por empuje magnético.
Si esa rotación se usa además para mover aire, se puede generar
electricidad adicional por inducción eólica sin consumir energía extra.

---

## Arquitectura híbrida propuesta

```
Panel solar 20W ──► Arduino + conmutación magnética ──► Rotor BSLC
                                                             │
                        ┌────────────────────────────────────┘
                        ▼
              Ventilador/turbina mini acoplada al eje
                        │
                        ▼
              Generador eólico pequeño (12-24V)
                        │
                        ▼
              Salida eléctrica adicional a batería
```

---

## Opción A — Ventilador axial integrado en cubo de rotor

- Ubicación: delante/detrás del rotor magnético (mismo eje).
- Tipo: hélice plástica 40-60 mm, paso optimizado para 500-1500 RPM.
- Generador acoplado: motor DC sin escobillas recuperado (DVD, 30-80 W).
- Voltaje objetivo: 12-24 V en banda de RPM útil.
- Ventaja: no altera la geometría magnética del rotor.

---

## Opción B — Turbina Savonius lateral

- Ubicación: perpendicular al eje, accionada por correa o engranaje.
- Tipo: rotor Savonius 2-3 palas, diámetro 80-120 mm.
- Ventaja: arranque a bajas RPM, buena para rotor BSLC de baja inercia.
- Generador: alternador pequeño de imanes permanentes (alternativa lavadora).

---

## Opción C — Turbina axial inline (ducted fan)

- Envolvente tipo duct en el propio estator.
- El campo magnético variable induce giro.
- El flujo axial pasa por la turbina generando electricidad adicional.
- Ventaja: compacto, aprovecha el mismo flujo sin elementos externos.

---

## Criterios de acoplamiento

| Criterio | Valor objetivo |
|---|---|
| RPM rotor utilizable | 300-1500 RPM |
| Torque mínimo eje | > 1 mN·m |
| Pérdida por fricción ventilador | < 5% del torque generado |
| Eficiencia aerodinámica | 0.25-0.35 (mini turbina) |
| Potencia eólica adicional | 5-20 W estimada |
| Coste adicional | < 10-15 € (recuperado) |

---

## Integración inteligente

- Arduino regula conmutación para mantener RPM en zona óptima conjunta:
  magnético + aerodinámico.
- Si la turbina produce suficiente, reduce corriente en bobinas.
- Modo mixto:
  - Baja potencia solar: solo magnético.
  - Media-alta: magnético + aerodinámico.
  - Viento natural extra: priorizar aerodinámico.

---

## Otras opciones inteligentes de generación complementaria

### 1. Piezoeléctrico en cojinetes
Vibración del eje → pastilla piezoeléctrica → 0.5-2 W continuos.
Útil para sensores y bajo consumo.

### 2. Termoeléctrico (Seebeck) en bobinas
Caloramiento bobinas (pérdidas) → módulos Seebeck → 1-3 W recuperados.
No interfiere con operación.

### 3. Inducción por rozamiento (tribo-generación)
Material triboeléctrico en zona de rozamiento eje-cojinete → carga estática
controlada → pequeña corriente continua.

### 4. Recuperación en conmutación
En cada apagado de bobina, el colapso de campo induce un pico de tensión
(back-EMF). Capturar con diodos rápidos + capacitor → 2-5 W adicionales.

### 5. Híbrido solar-termo
Colector solar térmico pequeño calienta agua del nodo.
El gradiente térmico acciona un motor Stirling mini → generación complementaria.

---

## Matriz de decisión

| Tecnología | Potencia | Coste | Complejidad | Integración |
|---|---|---|---|---|
| Ventilador axial | 5-15 W | Bajo | Media | Alta |
| Savonius lateral | 3-10 W | Bajo | Baja | Media |
| Ducted fan inline | 8-20 W | Medio | Alta | Alta |
| Piezoeléctrico | 0.5-2 W | Bajo | Baja | Alta |
| Termoeléctrico | 1-3 W | Medio | Baja | Alta |
| Back-EMF | 2-5 W | Muy bajo | Media | Media |
| Stirling mini | 10-30 W | Alto | Alta | Baja |

---

## Riesgos
- Sobregirar el rotor reduce eficiencia magnética.
- La turbina debe tener balance dinámico para no inducir vibración.
- El controlador necesita lógica de modo mixto.

---

## Próximo paso recomendado
Seleccionar una opción de generación complementaria y definir:
- posición exacta en el eje,
- transmisión (directa / correa / engranaje),
- generador recuperado o nuevo,
- controlador de modo compartido.
