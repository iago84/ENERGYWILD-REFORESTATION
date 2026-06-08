# IA APLICADA A DISEÑO ENERGÉTICO DE NODOS BSLC
## Optimización automática de generación, almacenamiento y demanda

---

## 1. OBJETIVO
- Usar modelos de IA para dimensionar la infraestructura energética de cada nodo según su perfil climático, demanda agrícola y presupuesto.
- Reducir overdesign / underdesign en paneles, baterías y controladores.
- Generar configuraciones óptimas en minutos a partir de datos locales.

---

## 2. DATOS DE ENTRADA (features)

| Variable | Tipo | Unidad | Fuente |
|----------|------|--------|--------|
| Radiación solar diaria | num | kWh/m²/día | NASA POWER / estación local |
| Consumo estimado nodo | num | kWh/día | Cálculo cargas (riego, LED, bombeo) |
| Presupuesto máximo | num | € | Definición proyecto |
| Temperatura media | num | °C | Estación meteorológica |
| Topografía / sombras | cat | flat / slope / shaded | GIS / campo |
| Tipo de demanda | cat | riego + iluminación / básico | Proyecto |

---

## 3. ARQUITECTURA DEL MODELO

### 3.1 Modelo A: Regresión (XGBoost / LightGBM)
Predice:
- kWh panel necesarios.
- Capacidad batería (kWh).
- Potencia pico inversor (W).

### 3.2 Modelo B: Optimización (programación lineal + RL)
Asigna:
- Secuencia de carga (horario).
- Margin batería.
- Reducción demanda en horas pico.

### 3.3 Pipeline
```
Datos entrada → preprocesado → modelo A (dimensión) → escenarios → modelo B (operación) → JSON salida
```

---

## 4. SALIDA APLICABLE A NODOS

```json
{
  "nodo_id": "MALI-001",
  "solar_kwp": 520,
  "bateria_kwh": 1.2,
  "inversor_w": 800,
  "iluminacion_w": 10,
  "bombeo_w": 150,
  "horario_riego": ["06:00", "18:00"],
  "alertas": ["Reducir riego si SOC < 40%"]
}
```

---

## 5. BENEFICIOS ESPERADOS
- Disminución 20-40 % coste energético por nodo.
- Mejora fiabilidad (evitar fallos por subdimensionamiento).
- Adaptación rápida a nuevos perfiles climáticos.

---

## 6. INTEGRACIÓN EN PROYECTO
- Entrena con datos de `plantillas-datos-campo.md`.
- Aplica a cada nuevo nodo antes de construcción.
- Feedback loop con sensores nodo para reentrenar.
