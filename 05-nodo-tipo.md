# NODO TIPO PIRS-1 - DISEÑO COMPLETO
## Arquitectura unitaria replicable ×10 por cluster zona crítica

---

## 1. DATOS DE PARTIDA
- **Número de cluster**: 1 (fase piloto 0)
- **Número de nodos en cluster**: 10
- **Dimensión nodo**: 1 hectárea cada uno
- **Población objetivo**: 50-200 personas por nodo
- **Zona de estudio**: Sahel Central Maliense (ej. Ségou / Mopti)

---

## 2. ESPECIFICACIONES TÉCNICAS POR MÓDULO

### 2.1 MÓDULO AGUA
| Item | Cantidad | Especificación |
|------|----------|----------------|
| Pozo perforado | 1 cada 10 nodos (cluster) | 30-60 m, acuífero superficial |
| Tanque enterrado | 1 por nodo | 50 m³, geomembrana HDPE |
| Fog harvester | 1 por nodo | 2-3 mallas 5×5 m, PET reciclado UV |
| Clorador UV | 1 por nodo | 0.5-1 W, desinfección agua consumo |
| Tuberías PEAD | Completo | ½" y ¾", distribución parcelas |
| Kit de filtros | 1 por nodo | Grava + arena + carbón activado |

**Cálculo captación fog**  
`Q = 0,5 L/m²/día × mallas 50 m² = 25 L/día por nodo`  
Mínimo viable: 3×3 m (9 m²) con 5 L/día = 45 L/día útiles

---

### 2.2 MÓDULO SUSTRATO Y SUELO
| Capa | Profundidad | Mezcla |
|------|-------------|--------|
| Mulch orgánico | 5 cm | Restos cosecha + hojarasca |
| Capa activa | 50 cm | 40% biochar + 40% compost + 20% arena arcillosa |
| Capa mineral | 25 cm | Suelo nativo + polvo de roca local |
| Microorganismos | Inoculación | Micorrizas + Rhizobium |

**Dosis biochar**: 1,5-2 kg/m² inicial, luego reposición anual 0,5 kg/m²  
**pH objetivo**: 6,0-6,5 tras biochar (ajuste con ceniza si necesario)

---

### 2.3 MÓDULO AGRÍCOLA
**Disposición parcelas 1 ha nodo**:

```
Zona A - Cultivos base (4.000 m²)
- Mijo / Sorgo: 2.000 m²
- Melón / Sandía: 1.000 m²
- Hortalizas locales: 1.000 m²

Zona B - Cactus y fijadores (2.000 m²)
- Opuntia: 1.000 m² (barrera viento + alimento)
- Acacia + Moringa: 1.000 m² (setos + sombra)

Zona C - Agua + energía (1.000 m²)
- Fog harvester + almacenamiento + panel solar

Zona D - Reserva / expansion (3.000 m²)
- Rotación o expansión agroforestería
```

---

### 2.4 MÓDULO ENERGÍA
| Componente | Potencia | Función |
|-------------|----------|---------|
| Panel solar | 500 Wp | Generación primaria |
| Batería LFP | 1 kWh | Almacenamiento nocturno |
| Inversor 48V DC | 800 W | Distribución |
| LED aviso/luz | 5 W | Iluminación puntual |
| Bombeo agua | 100 W | Opcional si pozo comunitario |

**Consumo estimado nodo**: 12-18 kWh/día  
- Riego goteo automático: 3 kWh
- Cloración UV: 0,5 kWh
- Carga herramientas/comunicación: 9-14,5 kWh  
**Excedente teórico (panel 500W × 5h sol = 2,5 kWh)**: no cubre demanda sola → requiere compartir nodos o reducir consumo.

---

### 2.5 MÓDULO EROSIÓN / PROTECCIÓN
| Elemento | Descripción |
|----------|-------------|
| Malla PET reciclada | Patrón checkerboard, fijación estacas cada 2 m |
| Setos vivos | Leucaena / acacias espinosas |
| Zanjas infiltración | Cada 20 m en pendiente, 30×30 cm |
| Brea vegetal | Parcelas muertas de protección |

---

## 3. SECUENCIA DE CONSTRUCCIÓN NODO (30 días aprox.)
| Semana | Actividad |
|--------|-----------|
| 1 | Topografía, delimitación, replanteo zanjas |
| 2 | Colocación mallas + hincado estacas |
| 3 | Excavación zanjas + siembra setos |
| 4 | Instalación pozo + tanque + panel |
| 5 | Relleno sustrato + plantación cactus |
| 6 | Riego inicial + inoculación |
| 7 | Siembra mijo/sorgo + melón |
| 8-9 | Crecimiento inicial + ajustes riego |
| 10 | Evaluación y registro datos |

---

## 4. LISTA DE MATERIALES POR 1 NODO

| Categoría | Item | Cantidad | Coste estimado (€) |
|-----------|------|----------|-------------------|
| Agua | Fog harvester PET | 1 kit | 150 |
| | Tanque HDPE 50 m³ | 1 ud | 300 |
| | Kit filtros / clorador | 1 ud | 120 |
| Energía | Panel 500 W | 1 ud | 120 |
| | Batería LFP 1 kWh | 1 ud | 250 |
| | Inversor / bombeo | 1 ud | 180 |
| Suelo | Biochar inicial | 1.000 kg | 100 |
| | Compost | 500 kg | 50 |
| Siembra | Semillas mijo/sorgo | 10 kg | 20 |
| | Plantones cactus | 500 uds | 150 |
| | Plantones acacia/moringa | 200 uds | 100 |
| Protección | Mallas PET | 30 m | 90 |
| | Estacas / hilo | Lote | 60 |

**Total por nodo**: ~1.690 € (sin mano de obra local)  
**Total por cluster 10 nodos**: ~16.900 €

---

## 5. REQUERIMIENTOS DE MANO DE OBRA
- Jefe de nodo: 1 persona dedicada (formada)
- Ayudantes: 2-3 personas/etapa
- Horas hombre estimadas: 320 h por nodo
- Incluye: perforación/siembra/mantenimiento primer año

---

## 6. VARIABLES DE MEDICIÓN (CHECKLIST OPERATIVO)
| Variable | Frecuencia | Método |
|----------|------------|--------|
| Humedad suelo | Semanal | Sondeo 0-40 cm + sensor capacitivo |
| Captación agua | Diaria | Caudalímetro |
| Crecimiento cultivo | Quincenal | Medición altura / biomasa verde |
| Consumo energía | Semanal | Registro inversor / batería |
| Erosión visual | Mensual | Foto punto fijo + estaca-test |
| Supervivencia plantas | Mensual | % por especie |

---

## 7. ESCALABILIDAD
- **Año 1**: 1 cluster (10 nodos, 10 ha)
- **Año 2-3**: 5 clusters (50 nodos)
- **Año 4-7**: 20 clusters (200 nodos, 200 km²)
- **Año 8-15**: Escalado regional red nodo-corredor verde

---

## 8. REFERENCIAS EN PROYECTO
- `checklists-detallados.md` → Checklist 2 / Diseño del Nodo Tipo
- `agua/README.md` → Captación y almacenamiento
- `agricultura/README.md` → Cultivos y sustrato
- `reforestacion/README.md` → Especies vegetales
- `plantillas-gis.md` → Delimitación geoespacial
