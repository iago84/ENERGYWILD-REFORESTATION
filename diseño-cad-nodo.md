# DISEÑO CAD NODO ESTÁNDAR - BSLC (PASO 1)

## Especificaciones Constructivas

### Dimensiones Base: 100 m² (10m × 10m)

```
VISTA AÉREA (Planta)
┌─────────────────────────────┐
│  ┌─────┐                   │
│  │AGUA │  CULTIVO 40 m²    │ ← Nopal/Mijo
│  │PUYO │  ┌───────┐       │
│  │50m³ │  │SOMBRA │       │
│  └─────┘  │TORRE  │       │
│           │3NIVEL │       │
│ ┌─────────┴─────────┐     │
│ │ENERGÍA + CONTROL  │     │ ← Panel 300W + controlador
│ │                    │     │
│ └────────────────────┘     │
└─────────────────────────────┘

SECCIÓN TRANSVERSAL
ATMÓSFERA
    ↓
──────────────────────────
🌿 Capa vegetal (0-30 cm)
- mulch (10 cm)
- tierra viva (20 cm)
──────────────────────────
🟫 Capa productiva (30-60 cm)
- biochar (20 cm)
- compost (10 cm)
──────────────────────────
🟤 Capa mineral (60-100 cm)
- arena (30 cm)
- arcilla compactada (10 cm)
──────────────────────────
💧 Cisterna (subterránea)
- 50 m³ capacidad
- geomembrana HDPE
```

---

## Planos Constructivos Detallados

### 1. Estructura Cisterna

**Materiales:**
- Geomembrana HDPE 1mm (100 m²)
- Hormigón armado 15cm (estructura)
- Tubo entrada 10cm PVC
- Tubo salida 10cm PVC
- Llanta entrada poliéster

**Montaje:**
1. Excavar 60 cm profundidad
2. Colocar geomembrana
3. Sellado juntas térmico
4. Conexiones entrada/salida
5. Tubo bombeo sumergible

### 2. Estructura Torre Vertical

**Perfil:** Acero galvanizado 50×50 mm → 3m altura
**Niveles:** 3 plataformas (0.8m, 1.8m, 2.8m)
**Sustrato:** Biochar + compost + arena (40%/40%/20%)
**Riego:** Microaspersión + condensación nocturna

### 3. Sistema Solar

**Paneles:** 2 × 300W monocristalino
**Estructura:** Montaje inclinado 15° norte
**Cableado:** 6mm² DC → MPPT → batería
**Protección:** Disyuntor 30A + fusible 20A

### 4. Red de Mallas Anti-Erosión

**Malla 2×2m:** 10 unidades
**Altura:** 30 cm sobre suelo
**Fijación:** Estacas madera cada 2m
**Patrón:** Checkerboard 50% cobertura

---

## Lista Materiales CAD (100m²)

| Categoría | Item | Cantidad | Dimensiones/Peso |
|-----------|------|----------|------------------|
| Estructura | Acero galvanizado | 50 kg | 50×50×3m perfiles |
| Agua | Geomembrana HDPE | 1 rollo | 1mm×100m² |
| Agua | Bomba solar | 1 | 48V DC, 500W |
| Agua | Tubo PVC | 4 m | 10cm diámetro |
| Energía | Panel solar | 2 | 300W cada uno |
| Energía | Batería LFP | 1 | 12V 100Ah |
| Energía | Controlador MPPT | 1 | 48V 60A |
| Cultivo | Biochar | 2 m³ | activado |
| Cultivo | Compost | 2 m³ | orgánico |
| Cultivo | Semillas nopal | 1 kg | Opuntia ficus |
| Cultivo | Semillas mijo | 0.5 kg | variedad local |
| Mallas | Geotextil | 40 m² | 2×2m unidades |
| Mallas | Estacas madera | 20 | 2m tratadas |

---

## Ejes de Ensamblaje

### Secuencia Montaje (4 días)

**Día 1:**
- Excavar cisterna 60cm
- Colocar geomembrana
- Conexiones agua

**Día 2:**
- Montar torre vertical
- Instalar riego

**Día 3:**
- Estructura solar + cableado
- Mallas anti-erosión

**Día 4:**
- Capas suelo (biochar/compost)
- Siembra cultivos
- Prueba sistema completo

---

## Coste Estimado 100m²

| Categoría | Coste (€) |
|-----------|-----------|
| Agua | 200-300 |
| Energía | 150-250 |
| Cultivo | 100-150 |
| Estructura | 150-200 |
| Labor | 50-100 |
| **Total** | **650-1000 €** |