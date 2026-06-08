# Sistema Energético - ESTRATEGIA BSLC

## Visión General
Microredes autónomas para territorios aislados del Sahel, Mali.

## Componentes Energéticos

### 1. Generación Híbrida
- **Solar fotovoltaica distribuida**: Paneles modulares de bajo mantenimiento
- **Energía térmica solar**: Cocinas comunitarias, hornos de concentración
- **Microeólica de baja velocidad**: Turbinas verticales (VAWT)

### 2. Almacenamiento
- **Baterías LFP comunitarias**
- **Sistemas gravitacionales** (agua elevada)
- **Supercondensadores** en nodos críticos

### 3. Distribución
- **Red en malla (mesh grid)**
- **LED ultra eficientes** (1-5W por nodo)
- **Sensores de presencia**

## Arquitectura Óptima por Nodo

```
☀️ Solar (3-10 kW)
    ↓
🔌 MPPT + regulación
    ↓
🔋 Baterías LFP (10-30 kWh)
    ↓
🧠 Inversor bidireccional
    ↓
⚡ BUS AC trifásico local (400V)
    ↓
- bombas de agua
- maquinaria agrícola  
- microindustria de mallas
- iluminación LED
```

## Configuración Técnica Recomendada
- Paneles: 200-500W por nodo
- Batería: 1-3 kWh por nodo (escala)
- Red: sistema mesh con nodos autónomos
- Iluminación: LED 1-5W con sensores

## Especificaciones
- **Autonomía parcial**: 80-95%
- **Eficiencia general**: 90-97% (con BLDC optimizado)
- **Mantenimiento**: bajo
- **Escalabilidad**: alta

---

## Generador BSLC Magnético (AI Design)

### Concepto Único
Panel solar MINIMO (20W) → Arduino → Conmutación imanes inducidos → Rotor imán permanente → Generación eléctrica AUTO-SOSTENIDA

### Geometría Magnetica
- **Rotor**: 3 sectores asimétricos (N-S-N / S-N-S / N-S)
- **Estator**: 12 bobinas con campos variables
- **Imán**: Neodimio N52, 1.4 Tesla

### Prompts AI Disponibles
- `generador-bslc-magnetico.md` - Diseño completo
- `prompt-generador-bslc.md` - Prompts para IA
- `prompts-ai-generador.md` - Subprompts técnicos
- `simulacion-generador.md` - Cálculos + simulación

### Resultado Esperado
- RPM > 500 con solo 20W panel solar
- Generación 10-30W si eficiencia >70%
- Auto-sostenimiento si generación > consumo conmutación

⚠️ **Nota física**: No es perpetuo. El panel alimenta SOLO conmutación. El rotor "quiere" girar por desequilibrio magnético.