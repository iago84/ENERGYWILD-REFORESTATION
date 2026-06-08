# FOG HARVESTING - SISTEMA DE CAPTACIÓN NIEBLA
## Adaptación Sahel/Mali: datos reales, diseño y mantenimiento

---

## 1. PRINCIPIO DE FUNCIONAMIENTO
- Captura mediante mallas verticales expuestas al viento cargado de humedad.
- Las microgotas se depositan en la red y caen por gravedad a canaletas.
- No requiere energía externa; el viento es el motor.

---

## 2. EFICIENCIA REAL DOCUMENTADA

### 2.1 Rango global verificado
| Zona | Rendimiento medio | Máximo | Fuente |
|-------|-------------------|--------|--------|
| Atacama (Chile) | 6 L/m²/día | 14 L/m²/día | Calderón et al. |
| Tenerife (España) | 10 L/m²/día | 7-10 L/m²/día | Marzol et al. |
| Sidi Ifni (Marruecos) | 1.6-6 L/m²/día | 21 L/m²/día (abril) | Schunk et al., 2024 |
| Alto Patache (Chile) | 6 L/m²/día (14 años) | 8 L/m²/día | Klemm et al. |
| Omán | 0-30 L/m²/día | 30 L/m²/día | Abdul-Wahab et al. |
| Perú (Cajamarca) | 1.09-1.28 L/m²/día | 108 L/día en 24 m² | Revista Ciencia Norandina |
| Colombia (Páramo) | 0.02-1.77 L/m²/día | 4.4 L/m²/día | Cortés-Pérez et al. |
| Bolivia (CloudFisher) | 7-11 L/m²/día | 350 L/m²/mes | Zabalketa/ICO |

### 2.2 Factores críticos
- **Material de malla**: Raschel (eficaz); 3D CloudFisher (mejor).
- **Velocidad del viento**: óptima 4-10 m/s (14-36 km/h).
- **Dirección**: debe ser perpendicular a vientos húmedos dominantes.
- **Altura**: 1-3 m sobre suelo (mejor captación en gradiente de humedad).

---

## 3. ADAPTACIÓN A MALI / SAHEL

### 3.1 Potencial estimado
- Zona atlántica (Mauritania, Senegal): > 5 L/m²/día en época niebla.
- Crestas elevadas interiores: 2-8 L/m²/día.
- No aplicable en interior puramente desértico (sin fuente humedad).

### 3.2 Diseño recomendado nodo BSLC
```
Malla: Raschel 3D o PET reciclado UV-estabilizado
Dimensiones: 3-5 m² por unidad
Cantidad: 2-3 unidades por nodo
Altura: 1.5-2 m
Orientación: NE-SO (perpendicular Harmattan húmedo)
Canaleta: PVC 4" con desagüe a cisterna
Mantenimiento: limpieza mensual, reparación anual
```

---

## 4. CÁLCULO DE COBERTURA
- Consumo per cápita recomendado: 16-38 L/día (OMS básico: 16 L).
- Nodo 50 personas × 16 L = 800 L/día.
- Necesario: 800 / 5 L/m² = 160 m² de malla.
- Distribución: 10 nodos × 16 m² = 160 m² total.
- Complementar con condensación nocturna y pozo para periodos sin niebla.

---

## 5. CALIDAD DE AGUA
- Agua de niebla: generalmente potable después de filtrado simple.
- Contaminantes potenciales: polvo atmosférico, insectos.
- Tratamiento: filtro sedimentos + cloración UV ligera.
- Usos: consumo humano, riego, stock de emergencia.

---

## 6. MANTENIMIENTO COMUNITARIO
- Limpieza malla: cada 2-4 semanas (polvo/insectos).
- Reparación tensores: después de tormentas de arena.
- Reemplazo malla: cada 3-5 años (según material).
- Registro caudal: semanal (hoja simple o app móvil).

---

## 7. REFERENCIAS EN PROYECTO
- `agua/README.md` → Sistema captación atmosférica.
- `nodo-tipo.md` → Diseño módulo agua nodo.
- `checklists-detallados.md` → Fog harvesting.
- Artículos científicos: Schunk et al. (2024), Klemm et al. (2012), Zabalketa/ICO Bolivia.
