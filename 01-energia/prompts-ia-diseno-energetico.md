# PROMPTS IA - DISEÑO ENERGÉTICO BSLC
## Biblioteca de prompts para generación, optimización y auditoría energética

---

## 1. PROMPT: DIMENSIONAMIENTO DE NODO ENERGÉTICO

```
Eres un ingeniero de energías renovables especializado en micro-redes rurales en zonas áridas (Sahel, Mali). Dimensiona un nodo BSLC para 50 personas con las siguientes restricciones:

- Radiación solar: 5,5 kWh/m²/día (NASA POWER estación Ségou).
- Consumo objetivo: 12 kWh/día (riego 3 kWh, iluminación 0,5 kWh, otros 8,5 kWh).
- Presupuesto máximo: 1.200 € para energía.
- Autonomía mínima: 2 días sin sol.

Entrega:
1) configuración paneles (Wp, cantidad, orientación);
2) banco baterías LFP (kWh);
3) inversor y protecciones;
4) estimación OPEX anual;
5) advertencias climáticas locales relevantes.
```

---

## 2. PROMPT: OPTIMIZADOR DE SISTEMA HÍBRIDO

```
Actúa como consultor en sistemas híbridos off-grid para zonas remotas. Optimiza el siguiente sistema para minimizar OPEX y maximizar fiabilidad:

- Solar 500 Wp
- Batería LFP 1 kWh
- Carga base 10 kWh/día
- Riego opcional +3 kWh/día

Evalúa:
1) Añadir microeólica vertical (VAWT) 300 W: ¿mejora autosuficiencia?
2) Reducir consumo LED a 1 W/nodo: impacto económico.
3) Almacenamiento gravitacional (agua elevada): caso de uso óptimo.
4) Estrategia de arbitraje energético (desplazar cargas según pronóstico).

Entrega recomendación final + curva de carga diaria.
```

---

## 3. PROMPT: AUDITORÍA DE PROYECTO ENERGÉTICO

```
Revisa este diseño energético para un nodo Sahel y detecta riesgos de fallo:

- Panel 500 W, batería 1 kWh, inversor 800 W.
- Climatología: temperaturas 30-45°C, polvo en suspensión.
- Mano de obra local sin formación eléctrica avanzada.

Devuelve:
1) Lista de fallos comunes en entornos áridos;
2) Soluciones de mitigación por coste ascendente;
3) Protocolo mantenimiento trimestral;
4) Inventario mínimo repuestos nodo.
```

---

## 4. PROMPT: PREDICCIÓN DE DEMANDA

```
Predice la demanda energética semanal de un nodo agrícola en Mali con:

- Cultivos: nopal, mijo, melón.
- Riego automático 6:00 y 18:00.
- Iluminación LED 5 W de 19:00 a 23:00.
- Bombeo agua: 100 W × 4 h/día.

Incluye:
1) Perfil de carga horaria verano/invierno;
2) Puntos de riesgo sobreconsumo;
3) Estrategias de reducción sin perder servicio.
```

---

## 5. PROMPT: MATERIALES BAJO COSTE

```
Propón materiales alternativos de bajo coste y mantenibilidad local para:

- Estructura soporte paneles solares.
- Carcasa protección electrónica nodo.
- Cableado y protecciones DC.

Considera:
- Disponibilidad en Mali;
- Resistencia térmica y polvo;
- Coste máximo total 300 €;
- Capacidad reparación por personal local.
```

---

## 6. PROMPT: CONTROL IoT Y TELEMETRÍA

```
Diseña un sistema IoT barato y robusto para nodos Sahel que permita:

- Monitorear voltaje, corriente, SOC batería.
- Medir caudal agua y humedad suelo.
- Transmitir datos a dashboard central.
- Actuar sobre riego según reglas simple.

Propón:
1) Stack hardware por nodo (< 150 €);
2) Protocolo comunicación (LoRa / mobile / ambos);
3) Dashboard mínimo viable;
4) Estrategia offline-first si conectividad falla.
```
