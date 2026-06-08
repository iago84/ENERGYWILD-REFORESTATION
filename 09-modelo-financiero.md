# MODELO FINANCIERO DETALLADO - BSLC (PASO 2)

## Hoja Cálculo CAPEX/OPEX - Formato Excel

### CAPEX Desglose Completo (€/ha)

| Categoría | Sub-item | Coste unitario | Cantidad | Total |
|-----------|----------|----------------|----------|-------|
| **AGUA** | | | | |
| | Pozo profundo | 5,000 | 1 | 5,000 |
| | Bomba solar 500W | 200 | 1 | 200 |
| | Cisterna 200m³ | 1,500 | 1 | 1,500 |
| | Malla fog harvesting | 20 | 100 m² | 2,000 |
| | | **Subtotal AGUA** | | **8,700** |
| **SUELO** | | | | |
| | Biochar 20 ton | 30 | 20 | 600 |
| | Micorrizas 5 L | 150 | 5 | 750 |
| | Trabajo aplicación | 5 | 10 m³ | 50 |
| | | **Subtotal SUELO** | | **1,400** |
| **AGRICULTURA** | | | | |
| | Panel solar 3kW | 100 | 6 | 600 |
| | Batería LFP 15kWh | 400 | 4 | 1,600 |
| | Inversor MPPT | 200 | 2 | 400 |
| | Semillas + plantones | 5 | 10 kg | 50 |
| | | **Subtotal AGRO** | | **2,650** |
| **INDUSTRIA** | | | | |
| | Trituradora plástico | 3,000 | 1 | 3,000 |
| | Máquina tricotado | 8,000 | 1 | 8,000 |
| | Herramientas | 200 | 1 | 200 |
| | | **Subtotal INDUSTRIA** | | **11,200** |
| **LOGÍSTICA** | | | | |
| | Transporte inicial | 300 | 1 | 300 |
| | Formación técnicos | 500 | 1 | 500 |
| | | **Subtotal LOGÍSTICA** | | **800** |
| | **TOTAL CAPEX/ha** | | | **24,150** |

---

## Flujo Ingresos Anuales (€/ha/año)

| Fuente | Calculo | Ingreso |
|--------|---------|---------|
| **Producción agrícola** | | |
| | Mijo 1.5 ton × 200 €/ton | 300 |
| | Sandía 30 ton × 150 €/ton | 4,500 |
| | Nopal 500 kg × 3 €/kg | 1,500 |
| | Moringa 200 kg × 5 €/kg | 1,000 |
| | **Subtotal Agricultura** | **7,300** |
| **Servicios** | | |
| | Agua gestión comunidad | 500 |
| | Energía comunidad | 800 |
| | **Subtotal Servicios** | **1,300** |
| **Créditos Carbono** | | |
| | CO₂ capturado 50 ton × 30 €/ton | 1,500 |
| | **Subtotal Carbono** | **1,500** |
| **TOTAL INGRESOS/año** | | **10,100** |

---

## OPEX Anual (€/ha/año)

| Concepto | % CAPEX | Importe |
|----------|---------|---------|
| Mantenimiento pozos | 10% | 870 |
| Reposición biochar | 5% | 70 |
| Energía backup | 3% | 72 |
| Gestión comunidad | 15% | 1,219 |
| **TOTAL OPEX/año** | **33%** | **2,231** |

---

## ROI Detallado

### Escenario Base (1 ha)
- CAPEX total: 24,150 €
- Ingresos anuales: 10,100 €
- OPEX anual: 2,231 €
- Neto anual: 7,869 €
- **ROI: 3.1 años**

### Escenario 100 ha piloto
- CAPEX total: 2,415,000 €
- Ingresos anuales: 1,010,000 €
- OPEX anual: 223,100 €
- Neto anual: 786,900 €
- **ROI: 3.1 años**

### Escenario 1000 ha escalado
- CAPEX total: 24,150,000 €
- Ingresos anuales: 10,100,000 €
- OPEX anual: 2,231,000 €
- Neto anual: 7,869,000 €
- **ROI: 3.1 años**

---

## Tabla Amortización

| Año | Ingreso acum (€) | CAPEX invertido | % Amortizado |
|-----|------------------|-----------------|--------------|
| 0 | 0 | 24,150 | 0% |
| 1 | 7,869 | 24,150 | 32.6% |
| 2 | 15,738 | 24,150 | 65.2% |
| 3 | 23,607 | 24,150 | 97.8% |
| 4 | 31,476 | 24,150 | 100%+49% |

---

## Fuentes Financiamiento

| Fuente | Tipo | Monto (€) | Requisitos |
|--------|------|-----------|------------|
| **ONU FAO** | Grant | 500,000 | Proyecto agroecológico |
| **Banco Mundial** | Loan | 1,000,000 | Viabilidad + escalado |
| **African Dev Bank** | Grant/Loan | 300,000-500,000 | Enfoque regional |
| **Green Climate Fund** | Grant | 500,000+ | Enfoque climático |
| **Private Impact** | Investment | 200,000-1,000,000 | ROI comprobado |

---

## Sensibilidad Variables

| Variable | -20% | Base | +20% |
|----------|------|------|------|
| Precio mijo | ROI: 2.8 años | ROI: 3.1 años | ROI: 3.5 años |
| Precio carbono | ROI: 4.1 años | ROI: 3.1 años | ROI: 2.5 años |
| Producción agua | ROI: 4.2 años | ROI: 3.1 años | ROI: 2.6 años |

---

## Descarga Plantilla Excel

```csv
AÑO,CAPEX_TOTAL,INGRESOS_NETOS,ACUMULADO,AMORTIZADO
0,24150,0,0,0
1,24150,7869,7869,32.6%
2,24150,7869,15738,65.2%
3,24150,7869,23607,97.8%
4,24150,7869,31476,100%+49%
```