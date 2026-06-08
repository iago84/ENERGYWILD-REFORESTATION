# NEXUS RISING — DeepStudy & Machine Learning Research Context

> ML/AI research documentation for the BSLC Magnetic Generator system.
> Focus: deep study of NEXUS RISING node network, reinforcement learning for false positive prevention, and optimization objectives.

---

## 1. Objetivo Principal

Desarrollar un sistema de aprendizaje automático para:

1. **Optimización de patrones de imantado** — Selección automática de geometrías Halbach asimétricas óptimas.
2. **Predicción de campos magnéticos** — Regresión de B_total(t) y torque a partir de configuraciones de entrada.
3. **Control de conmutación inteligente** — Aprendizaje por refuerzo (RL) para secuencias óptimas de activación de bobinas.
4. **Detección de falsos positivos** — Clasificación de resultados simulados vs. mediciones reales.

---

## 2. Dataset y Contexto de Entrenamiento

### 2.1 Fuentes de Datos

| Fuente | Tipo | Descripción |
|--------|------|-------------|
| Simulaciones conceptuales | Sintético | Patrones Halbach generados algorítmicamente |
| Mediciones experimentales | Real | Datos de prototipo (futuro) |
| Catálogo de materiales | Estático | NdFeB N52, parámetros magnéticos |
| Configuraciones históricas | Histórico | Patrones probados anteriormente |

### 2.2 Esquema de Features

```python
FEATURES = [
    # Geometría del rotor
    "num_sectores",           # int: 2-6
    "radio_rotor_mm",         # float: 40-80
    "ancho_rotor_mm",         # float: 10-40
    "factores_radio",         # list: [0.6-1.0] por sector
    "polaridades",            # categorical: N/S sequence
    
    # Material imán
    "material_iman",          # categorical: N52, N42, etc.
    "campo_residual_t",       # float: 1.2-1.5
    "rem_br_max_t",           # float from datasheet
    
    # Estator
    "num_bobinas",            # int: 3-12
    "vueltas_bobina",         # int: 200-1000
    "seccion_cable_mm2",      # float: 0.5-2.0
    "corriente_max_a",        # float: 1-5
    
    # Contexto energético
    "voltaje_entrada_v",      # float: 12
    "potencia_panel_w",       # float: 10-100
    "temperatura_ambiente_c", # float: 20-50
]
```

### 2.3 Esquema de Labels (Targets)

```python
TARGETS = {
    "desbalance_magnetico_am2": float,   # Momento dipolar neto
    "torque_teorico_nm": float,           # Torque máximo estimado
    "torque_arranque_nm": float,          # Torque a 0 RPM
    "eficiencia_material": float,         # desbalance / masa kg
    "coste_imanes_eur": float,            # Coste estimado
    "velocidad_critica_rpm": float,       # RPM mínima de generación
    "consumo_estimado_w": float,          # Potencia conmutación
    "viabilidad": categorical,            # ALTA / MEDIA / BAJA / IMPOSIBLE
}
```

---

## 3. Deep Study: Áreas de Investigación

### 3.1 Geometría Sagrada y Fractales

| Concepto | Hipótesis | Aplicación BSLC |
|----------|-----------|-----------------|
| Flor de la Vida | 64 círculos = 64 puntos de resonancia | Distribución de puntos de polaridad en rotor |
| Proporción Áurea (φ=1.618) | Optimiza secuencias de conmutación | Timing entre activaciones de bobinas |
| Triángulo Sierpinski | Resistencia decreciente fractal | Redes resistivas internas del estator |
| Espiral Fibonacci | Campo magnético auto-organizado | Distribución helical de imanes |

### 3.2 Frecuencias Resonantes

```
Frecuencias objetivo del sistema:
- 432 Hz: Resonancia armónica base (afirmado en documentación sagrada)
- 528 Hz: Frecuencia de reparación/estabilidad
- 7.83 Hz: Frecuencia Schumann (tierra) → posible grounding
- 50-200 Hz: Rango PWM conmutación (hardware Arduino)
```

**Hipótesis ML**: Sintonizar la frecuencia de conmutación a múltiplos de 432 Hz puede maximizar la eficiencia de transferencia energética.

### 3.3 Análisis Semántico de Campos

Modelado de campos magnéticos mediante embeddings semánticos:

```python
# Vectorización de configuraciones magnéticas
semantic_embeddings = {
    "atraccion_norte_sur": [0.9, -0.1, 0.3, ...],   # 64 dimensional
    "repulsion_sur_norte": [-0.2, 0.8, -0.4, ...],
    "neutral_equilibrado": [0.0, 0.0, 0.0, ...],
}

# Búsqueda de patrones óptimos por similitud
from sklearn.metrics.pairwise import cosine_similarity
patron_objetivo = embed("max_torque_min_coste_arranque_facil")
candidatos = buscar_patrones_similares(patron_objetivo, top_k=10)
```

---

## 4. Aprendizaje por Refuerzo (RL) para Conmutación

### 4.1 Arquitectura del Agente

```python
# Estado (State): posición rotor + velocidad + temperatura + SOC batería
state_space = {
    "posicion_deg": (0, 360),           # Sensor Hall
    "velocidad_rpm": (0, 2000),         # Calculado
    "temperatura_bobinas_c": (20, 120), # NTC
    "soc_bateria_pct": (0, 100),        # Divisor voltaje
    "corriente_entrada_a": (0, 10),     # Sensor shunt
}

# Acciones (Actions): qué bobinas activar y con qué duty cycle
action_space = {
    "bobina_activa": [0, 1, 2, ...11],  # 12 bobinas
    "duty_cycle_pct": (0, 100),          # PWM 0-100%
    "duracion_pulso_ms": (1, 50),        # Duración activación
}

# Recompensa (Reward): función de optimización multi-objetivo
def reward_function(estado, accion, resultado):
    torque_score = resultado["torque_nm"] * 10
    eficiencia_score = (1 - resultado["consumo_w"] / max(1, resultado["generacion_w"])) * 20
    temperatura_penalty = max(0, estado["temperatura_bobinas_c"] - 80) * -0.5
    desgaste_penalty = accion["duty_cycle_pct"] * -0.01
    
    return torque_score + eficiencia_score + temperatura_penalty + desgaste_penalty
```

### 4.2 Prevención de Falsos Positivos

El agente RL debe aprender a distinguir entre:

1. **Resultados reales** — Mediciones de torque, RPM, voltaje del prototipo físico.
2. **Resultados simulados** — Salida del modelo conceptual Python.
3. **Resultados teóricos** — Cálculos analíticos sin validación.

**Estrategia anti-falso positivo:**

```python
class ValidadorCruzado:
    """
    Sistema de validación triple para detectar inconsistencias.
    Solo un resultado se considera 'verdadero' cuando al menos 2
    de 3 fuentes coinciden dentro de tolerancia.
    """
    
    def validar(self, torque_simulado, torque_teorico, torque_medido=None):
        resultados = []
        
        # Check 1: Simulación vs Teoría
        if abs(torque_simulado - torque_teorico) < 0.01:  # 1% tolerancia
            resultados.append("sim_teo_ok")
        else:
            resultados.append("inconsistencia_sim_teo")
        
        # Check 2: Teoría vs Medida (si existe)
        if torque_medido is not None:
            if abs(torque_teorico - torque_medido) < 0.05:
                resultados.append("teo_med_ok")
            else:
                resultados.append("inconsistencia_teo_med")
        
        # Check 3: Simulación vs Medida
        if torque_medido is not None:
            if abs(torque_simulado - torque_medido) < 0.05:
                resultados.append("sim_med_ok")
            else:
                resultados.append("inconsistencia_sim_med")
        
        # Evaluación final
        positivos = sum(1 for r in resultados if "_ok" in r)
        confianza = positivos / len(resultados)
        
        return {
            "confianza": confianza,
            "checks": resultados,
            "veredicto": "VALIDADO" if confianza >= 0.67 else "RECHAZADO",
        }
```

---

## 5. Dataset JSON Schema

```json
{
  "experimento_id": "BSLC-2026-001",
  "timestamp": "2026-06-08T10:00:00Z",
  "configuracion": {
    "rotor": {
      "radio_mm": 50.0,
      "ancho_mm": 20.0,
      "num_sectores": 3,
      "sectores": [
        {
          "angulo_inicio_deg": 0.0,
          "angulo_fin_deg": 120.0,
          "imanes": [
            {
              "radio_mm": 40.0,
              "polaridad_ns": "N-S",
              "material": "N52"
            }
          ]
        }
      ]
    },
    "estator": {
      "num_bobinas": 12,
      "vueltas": 500,
      "seccion_mm2": 1.0
    }
  },
  "mediciones": {
    "torque_nm": 0.0,
    "velocidad_rpm": 0.0,
    "voltaje_v": 0.0,
    "corriente_a": 0.0,
    "temperatura_c": 25.0,
    "timestamp_medicion": "2026-06-08T10:00:05Z"
  },
  "validacion": {
    "fuente": "simulacion_conceptual",
    "confianza": 0.0,
    "checks": ["inconsistencia_sim_teo"]
  }
}
```

---

## 6. PIPELINE ML Propuesto

```
Datos Crudos → Limpieza → Feature Engineering → Split Train/Val/Test
                                                          |
    ┌─────────────────────────────────────────────────────┘
    ▼
Modelo A: Regresión (XGBoost / LightGBM)
  → Predice: torque, eficiencia, coste
  → Métricas: MAE, R²
    
    ┌─────────────────────────────────────────────────────┐
    ▼                                              
Modelo B: Clasificación (Random Forest / SVM)
  → Predice: viabilidad (ALTA/MEDIA/BAJA/IMPOSIBLE)
  → Métricas: F1-score, Precision, Recall
    │
    ▼
Validación Cruzada (3 fuentes: sim, teo, med)
  → Sistema anti-falso positivo
  → Confianza 0-100%
```

---

## 7. Notebooks de Experimentación

| Notebook | Propósito |
|----------|-----------|
| `01_exploracion_datos.ipynb` | EDA de configuraciones, correlaciones |
| `02_modelado_torque.ipynb` | Regresión de torque vs geometría |
| `03_clasificacion_viabilidad.ipynb` | Clasificador ALTA/MEDIA/BAJA |
| `04_rl_conmutacion.ipynb` | Entrenamiento agente RL (OpenAI Gym custom env) |
| `05_validacion_cruzada.ipynb` | Sistema anti-falso positivo |
| `06_visualizacion_3d.ipynb` | Visualización campos y geometrías |

---

## 8. Stack Tecnológico Recomendado

| Componente | Herramienta | Justificación |
|------------|-------------|----------------|
| Numeros/Básico | NumPy + SciPy | Cálculo vectorial, álgebra lineal |
| Machine Learning | scikit-learn + XGBoost | Modelos tabulares robustos |
| Deep Learning | PyTorch / TensorFlow | Redes neuronales para secuencias |
| RL | Stable-Baselines3 | PPO, A2C para conmutación |
| Visualización | Matplotlib + Plotly | Gráficos interactivos |
| Experimentación | Jupyter Notebook | Iteración rápida |
| Tracking | MLflow / Weights & Biases | Registro de experimentos |

---

## 9. Roadmap ML

| Fase | Duración | Entregable |
|------|----------|------------|
| Fase 1: Datos | 2-4 semanas | Dataset sintético inicial (1000+ muestras) |
| Fase 2: Baseline | 2-3 semanas | Modelos regresión/cls baseline |
| Fase 3: RL | 4-6 semanas | Agente conmutación entrenado |
| Fase 4: Validación | 2-4 semanas | Sistema anti-falso positivo integrado |
| Fase 5: Despliegue | 2-3 semanas | Pipeline productivo en nodo |

---

## 10. Notas Críticas

- **NINGÚN modelo ML reemplaza la validación experimental** del especialista en electromagnetismo.
- Los datasets sintéticos son UTILES para probar pipelines, NO para justificar viabilidad física.
- El sistema anti-falso positivo es OBLIGATORIO antes de cualquier afirmación de rendimiento.
- El RL debe entrenarse en simulación → validarse en prototipo físico antes de despliegue.

---

## Referencias

- `01-energia/generador-bslc/` — Estructura del proyecto
- `01-energia/ficha-tecnica-bslc.md` — Especificaciones base
- `01-energia/prompt-revision-especialista.md` — Handoff a especialista
- `01-energia/generador_patrones_imantado.py` — Generador de patrones (conceptual)
