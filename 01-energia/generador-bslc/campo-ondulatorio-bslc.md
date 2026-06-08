 # BSLC — Geometría de Campo Ondulatorio y Torque Oscilante

> Concepto sin validar: modela el campo del estator como una onda viajera que
> “empuja” el rotor de forma continua, en lugar de pulsos discretos.

---

## Hipótesis central
Si el campo magnético en el entrehierro se propaga como una onda viajera
con vector sincronizado a la posición del rotor, se puede producir torque
sostenido incluso a baja velocidad.

---

## Forma de onda propuesta

Campo tangencial en el entrehierro:
```
B_theta(theta, t) = B0 * sin(k * theta - omega * t + phi0)
```
- `k` = número de ondas espaciales = pares de polos efectivos
- `omega` = frecuencia angular del rotor
- `phi0` = fase de control

---

## Implementación con bobinas distribuidas

Cada bobina aporta un “armónico” en su posición angular.
Secuenciándolas en desfase progresivo, la suma produce una onda viajera.

Desfase entre bobinas:
```
delta_phi = 360 / N_bobinas
```
Ejemplo 12 bobinas → desfase 30°.

---

## Dibujo ASCII del campo ondulatorio

```
Btheta(t)
   |
 B0 |    /\         /\
    |   /  \       /  \
    |  /    \     /    \
    | /      \   /      \
    |/        \ /        \
  0 +----------+----------+------> theta (360°)
    0        90       180     270
    Bobina A   B        C       D
```

---

## Sinergia con rotor Halbach asimétrico
- El rotor ya presenta polaridad variable por sector.
- La onda del estator se adapta a esa variación creando una “huella”
  campo-rotor minimizando puntos muertos.

---

## Parámetros a optimizar
- Amplitud onda `B0` (corriente bobinas)
- Número de armónicos activos (cuántas bobinas se usan a la vez)
- Fase inicial `phi0` según velocidad
- Ancho angular de cada excitación (pulso más ancho = más torque,
  menos eficiencia)

---

## Riesgos / preguntas para especialista
- ¿Puede realmente formarse una onda viajera con bobinas discretas?
- ¿Qué forma de banda ancha/banda estrecha es más eficiente?
- ¿Cómo afecta la resistencia de las bobinas a la atenuación de la onda?
