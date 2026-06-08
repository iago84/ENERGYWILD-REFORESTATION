# NEXUS RISING — Optimization Objectives for MATERIALS & PATTERNS

> Technical specification of optimization goals across all system layers.
> Status: Conceptual design, NOT experimentally validated.

---

## 1. Optimization Framework

### 1.1 Multi-Objective Function

```
F_total(x) = w1·f_torque(x) + w2·f_eficiencia(x) + w3·f_coste(x) - w4·f_riesgo(x)
```

Where:
- `x` = vector de parámetros de diseño
- `w1-w4` = pesos del decisor (default: [0.4, 0.3, 0.2, 0.1])

### 1.2 Constraints

```
g1(x): torque_arranque ≥ 0.01 N·m      (mínimo para vencer inercia)
g2(x): coste_imanes ≤ presupuesto       (límite económico)
g3(x): temperatura_bobinas ≤ 80°C       (seguridad térmica)
g4(x): masa_total ≤ 500 g               (portabilidad)
g5(x): consumo_control ≤ 10 W           (sostenibilidad energética)
```

---

## 2. MATERIAL OPTIMIZATION

### 2.1 Magnet Materials Comparison

| Material | Br (T) | Hc (kA/m) | (BH)max (MGOe) | Cost/kg (€) | Peso estimado (g) |
|----------|--------|-----------|----------------|-------------|-------------------|
| N52 | 1.45 | 876 | 42 | 80 | 45 |
| N42 | 1.32 | 836 | 36 | 60 | 52 |
| N35 | 1.20 | 796 | 30 | 45 | 60 |
| Ferrita | 0.38 | 250 | 3.5 | 2 | 180 |
| SmCo | 1.05 | 800 | 25 | 200 | 40 |

**Objective**: Find material/size/geometry combination that maximizes torque/cost ratio while keeping mass under 500g.

### 2.2 Coating/Resistive Layer Optimization

**Hypothesis**: Internal resistive meshes can alter magnetic field distribution, reducing eddy current losses or creating field gradients.

| Layer | Proposed Material | Purpose | Status |
|-------|-------------------|---------|--------|
| Surface coating | Ni-Cu-Ni (triple plating) | Corrosion resistance, smooth B-field | Estándar |
| Internal mesh | Al 7075-T6 (patterned) | Custom field shaping | Experimental |
| Resistive network | Cermet thick-film | Frequency-dependent damping | Conceptual |
| Insulation | Polyimide (Kapton) | Inter-turn isolation | Standard |

**Optimization targets**:
- Minimize eddy current losses: `P_eddy ∝ t² · f² · B²`
- Maximize field homogeneity in active zone
- Minimize added mass (< 10% of rotor)

### 2.3 Internal Network Topologies

```
Opciones de malla interna en rotor:

A. Patrón hexagonal
   - Proporción llenado: 60%
   - Efecto: homogeniza campo tangencial
   
B. Patrón radial-spiral
   - Proporción llenado: 40%
   - Efecto: guía flujo hacia estator
   
C. Patrón checkerboard
   - Proporción llenado: 50%
   - Efecto: rompe simetría (induce torque)
```

---

## 3. PATTERN OPTIMIZATION OBJECTIVES

### 3.1 Primary Objectives

| Objective | Metric | Target | Weight |
|-----------|--------|--------|--------|
| Torque de arranque | N·m @ 0 RPM | > 0.01 | 0.35 |
| Torque sostenido | N·m @ 300-1000 RPM | > 0.05 | 0.30 |
| Eficiencia material | N·m / kg | > 0.5 | 0.20 |
| Coste total | € (imanes + bobinas) | < 150 | 0.10 |
| Masa total | g | < 500 | 0.05 |

### 3.2 Secondary Objectives

| Objective | Metric | Target |
|-----------|--------|--------|
| Temperatura operación | °C | < 80 |
| Tiempo arranque | segundos | < 3 |
| Vida útil estimada | horas | > 5000 |
| Facilidad fabricación | score 1-5 | > 3 |

---

## 4. SEQUENCE ACTIVATION OPTIMIZATION

### 4.1 Parameters to Optimize

```
Para cada bobina i:
- phi_i = ángulo de encendido óptimo (grados)
- t_on_i = duración pulso (ms)
- duty_i = ciclo trabajo PWM (%)
- t_delay_i = retardo después de apagado (ms)

N_total = 12 bobinas → espacio de búsqueda enorme
Reducción: simetría cada 30° → 3 fases independientes
```

### 4.2 Objective Function for Sequences

```python
def f_secuencia(secuencia, rotor_config):
    """
    Evalúa una secuencia de activación completa.
    
    Retorna: score_multiproposito
    """
    torques = simular_torque_series(secuencia, rotor_config)
    
    torque_promedio = mean(torques)
    torque_min = min(torques)
    variabilidad = std(torques)
    
    # Objetivos
    obj1 = torque_promedio              # Maximizar torque medio
    obj2 = -variabilidad                # Minimizar ripple
    obj3 = -tiempo_arranque             # Minimizar tiempo a RPM crítico
    obj4 = -energia_consumida           # Minimizar consumo
    
    return 0.4*obj1 + 0.3*obj2 + 0.2*obj3 + 0.1*obj4
```

### 4.3 Search Strategies

| Strategy | Complexity | Coverage | Recommended For |
|----------|-----------|----------|-----------------|
| Grid search | Medio | exhaustiva 3D | Fase inicial |
| Random search | Bajo | muestreo | Exploración rápida |
| Bayesian opt | Alto | inteligente | Optimización final |
| RL (PPO/A2C) | Muy alto | adaptativa | Producción |

---

## 5. RESISTIVE NETWORK DESIGN

### 5.1 Hypothesis

Resistive elements distributed in the stator/rotor interface can:
- Shape magnetic field gradients
- Create frequency-selective responses (RLC networks)
- Dampen unwanted harmonics

### 5.2 Network Topologies

**5.2.1 Lumped RC Snubbers**
```
Por cada bobina:
- R_snub = 10-100 Ω
- C_snub = 100-1000 nF
- Frecuencia corte: f_c = 1/(2πRC) ≈ 1-10 kHz
```

**5.2.2 Distributed Resistive Pattern**
```
Patrón en espiral de resistencias impresas:
- R_total = 1-10 Ω por rama
- Se activan selectivamente vía MOSFET
- Crea gradiente de campo "suave"
```

**5.2.3 Fractal Sierpinski Network**
```
Nivel 1: 3 resistencias en triángulo
Nivel 2: 9 resistencias
Nivel 3: 27 resistencias
Efecto: múltiples frecuencias de resonancia simultáneas
```

---

## 6. WAVY FIELD GEOMETRY

### 6.1 Concept

Instead of discrete coil activation, create a continuous traveling wave in the air gap:

```
B_theta(theta, t) = B0 · sin(k·theta - omega·t + phi0)

k = 6 (6 pares polos viajeros)
omega = velocidad angular rotor
phi0 = fase de control
```

### 6.2 Implementation via Discrete Coils

With N discrete coils, approximate the wave:

```python
B_wavy(theta, t) = sum(
    B_i(t) · sinc(k·(theta - theta_i))
    for i in range(N)
)
```

Where `sinc(x) = sin(pi*x)/(pi*x)` is the interpolation kernel.

### 6.3 Optimization Targets for Wavy Field

| Parameter | Optimal | Effect |
|-----------|---------|--------|
| k (spatial frequency) | 4-8 | More poles = smoother torque |
| B0 (amplitude) | 0.15-0.3 T | Higher = more torque, more loss |
| Phase velocity | Match rotor speed | Minimize slip |
| Coil count | 12-24 | Tradeoff: resolution vs. complexity |

---

## 7. COATINGS & SURFACE TREATMENTS

### 7.1 Magnet Surface Optimization

| Treatment | Effect on Field | Cost | Feasibility |
|-----------|-----------------|------|-------------|
| Ni plating (50 µm) | Smooths B-field boundary | Low | Standard |
| Epoxy coating | Insulates, reduces eddy | Low | Standard |
| Diamond-like carbon (DLC) | Ultra-smooth surface | Medium | Advanced |
| Ion implantation | Modifies surface coercivity | High | R&D |

### 7.2 Internal Layer Concept

```
Sección transversal del rotor optimizado:

[Diseño propuesto con malla interna]

1. Núcleo: Fibra de carbono (estructura)
2. Imanes: NdFeB N52 (campo primario)
3. Malla intermedia: Al 7075 patrón hexagonal (modificación de campo)
4. Recubrimiento: Ni-Cu-Ni (protección + suavizado)
```

**Effect**: Internal mesh creates secondary field patterns that complement the Halbach arrangement.

---

## 8. SYSTEM-LEVEL OPTIMIZATION

### 8.1 Coupled Optimization Variables

```
Variables globales a optimizar conjuntamente:

├── Rotor
│   ├── Material imán (N52/N42/Ferrita)
│   ├── Número sectores (2-6)
│   ├── Secuencia polaridades
│   └── Factores radio por sector
│
├── Estator
│   ├── Número bobinas (3-24)
│   ├── Vueltas por bobina
│   ├── Sección cable
│   └── Topología red resistiva
│
├── Control
│   ├── Secuencia activación (fase + duty + delay)
│   ├── Frecuencia PWM
│   └── Algoritmo RL policy
│
└── Sistema
    ├── Voltaje entrada
    ├── Potencia panel
    └── Configuración híbrida (magnético + eólico)
```

### 8.2 Optimization Strategy

1. **Coarse optimization**: Genetic algorithm on rotor geometry (fast, ~1000 evals)
2. **Fine optimization**: Bayesian optimization on control sequences (~100 evals)
3. **RL adaptation**: Train agent on best-found configuration (~10k episodes)
4. **Hardware-in-loop**: Final validation on physical prototype

---

## 9. RISK MITIGATION IN OPTIMIZATION

| Risk | Mitigation |
|------|------------|
| Overfitting synthetic data | Cross-validation with real measurements |
| Local optima | Multi-start + genetic algorithm diversity |
| Computational cost | Surrogate models (Gaussian Process) |
| Physical invalidity | Veto filter based on energy conservation |
| Thermal runaway | Temperature constraint in optimizer |

---

## 10. DELIVERABLES FROM THIS SPEC

1. `optimizer_genes.py` — Genetic algorithm for geometry + pattern optimization
2. `optimizer_bayes.py` — Bayesian optimization wrapper (scikit-optimize)
3. `rl_environment.py` — Custom Gym environment for BSLC commutation
4. `resistive_networks.py` — Network topology generator and evaluator
5. `coating_models.py` — Surface treatment effect models
