# GLOSARIO TÉCNICO COMPLETO - ESTRATEGIA BSLC

## Acrónimos y Términos Clave

| Término | Definición | Fórmula/Aplicación |
|---------|------------|-------------------|
| **BLDC** | Brushless DC Motor - Motor sin escobillas | Eficiencia >95%, control electrónico |
| **CAPEX** | Capital expenditure - Inversión inicial | Coste infraestructura nueva |
| **Cisterna MAR** | Managed Aquifer Recharge - Recarga acuíferos | Agua subterránea sin evaporación |
| **Fog Harvesting** | Captación niebla - Sistemas malla | 2-20 L/m²/día según humedad |
| **FOC** | Field Oriented Control - Control vectorial | Control preciso motores BLDC |
| **GIS** | Geographic Information System - Sistema info geográfica | Mapas capas: viento, agua, nodos |
| **Halbach Array** | Configuración imanes alternados | Campo magnético unidireccional |
| **KPI** | Key Performance Indicator - Métricas clave | Humedad, producción, ROI |
| **LDN** | Land Degradation Neutrality - Neutralidad tierras | ONU/oDM objetivos sostenibilidad |
| **MPPT** | Maximum Power Point Tracking - Seguimiento punto máximo | Optimización paneles solares |
| **OPEX** | Operational expenditure - Gastos operativos | Mantenimiento, reposición |
| **ROI** | Return on Investment - Retorno inversión | Años para amortizar |
| **SDG** | Sustainable Development Goals - ODS ONU | 2, 6, 7, 15 (agua, energía, suelo) |
| **Swale** | Zanja infiltración - Captación escorrentía | Perfil 30cm profundidad |
| **TDR** | Time Domain Reflectometry - Medición humedad | Tecnología sensor suelo |

## Especies Vegetales

| Nombre Científico | Común | Uso BSLC | Rendimiento |
|-------------------|-------|----------|-------------|
| *Opuntia ficus-indica* | Nopal/Cactus | Infrapista hídrica + alimento | 5-15 kg/m²/año |
| *Moringa oleifera* | Moringa | Nutrimentos + nitrógeno | 2-4 kg/m²/año |
| *Acacia tortilis* | Acacia | Nitrógeno + sombra + estabilidad | 0.5-1 kg/m²/año |
| *Azadirachta indica* | Neem | Control biológico plagas | Árbol ornamental |
| *Citrullus lanatus* | Sandía | Regulación hídrica + alimento | 20-40 ton/ha/año |
| *Cucumis melo* | Melón | Producción rápida | 30-50 ton/ha/año |
| *Pennisetum glaucum* | Mijo | Base calórica | 1-2 ton/ha/año |
| *Sorghum bicolor* | Sorgo | Resistencia sequía | 1-3 ton/ha/año |

## Componentes Hardware

| Componente | Especificación Técnica | Equivalencia Local |
|------------|------------------------|-------------------|
| Bomba sumergible | 48V DC, 500W | Alternativa: bomba de mano solar |
| Panel solar | 200-500W monocristalino | Alternativa: panel policristalino |
| Batería LFP | 48V, 5kWh | Alternativa: baterías de automóvil |
| Malla captación | Polipropileno 1mm | Alternativa: tela de nylon local |
| Biochar | Carbón activado | Alternativa: ceniza de leña tratada |
| Micorrizas | Arbusculares 10⁸ UFC | Alternativo: compost local |
| Inversor | 48V-380V trifásico | Alternativa: inversor monofásico |

## Variables Modelo Matemático

| Símbolo | Significado | Unidad | Rango Esperado |
|---------|-------------|--------|----------------|
| N(t) | Número de nodos | unidades | 10-1000 |
| V(t) | Cobertura vegetal | m² | 1000-50000 |
| W(t) | Agua disponible | L | 1000-100000 |
| S(t) | Estabilidad suelo | índice 0-1 | 0.3-0.9 |
| P | Precipitación | mm/día | 0-5 (árido) |
| C | Condensación | L/día | 5-50 |
| G | Aporte subterráneo | L/día | 0-100 |
| E | Evaporación | L/día | 50-200 |
| T | Transpiración | L/día | 20-80 |
| U | Uso consumo | L/día | 50-200 |

---

## Equivalencias Métricas

| Magnitud | Unidad | Conversión |
|----------|--------|------------|
| 1 hectárea | 10,000 m² | 0.01 km² |
| 1 kWh | 3.6 MJ | 1,000 Wh |
| 1 L agua | 1 kg | 0.001 m³ |
| 1 mm precipitación | 1 L | 1 m² |
| 1 kW solar | 5 kWh/día | 1 panel 200W 5h sol |
| 1 kg biochar | 0.8 L retención | Equivalente hídrico |

---

## Referencias Técnicas

1. **FAO** - Estado de la Tierra y Desertificación
2. **Great Green Wall** - Iniciativa Africaña
3. **Tengger Desert** - Técnicas control China
4. **LDN - Land Degradation Neutrality** - Marco ONU
5. **ODA** - Objetivos Desarrollo Sostenible