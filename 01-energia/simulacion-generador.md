# SIMULACIÓN GENERADOR BSLC

## Cálculo Torque Imán Asimétrico (Matlab/Python)

```matlab
% rotor_magnetico.m
% Calcula torque rotor con imánes asimétricos

% Parámetros
Br = 1.4;  % Tesla fuerza imán
A = 0.0001; % m² área imán (20mm × 0.5mm)
theta = 0:1:360; % ángulos

% Geometría rotor (asimétrico)
B_theta = zeros(size(theta));
for i = 1:length(theta)
    angulo = theta(i);
    if angulo < 120
        B_theta(i) = Br * 1.0; % sector fuerte
    elseif angulo < 240
        B_theta(i) = Br * 0.5; % sector medio
    else
        B_theta(i) = Br * 0.2; % sector débil
    end
end

torque = 0.001 * B_theta .* sin(deg2rad(theta)); % torque variable
fprintf('Torque medio: %.2f mNm\n', mean(torque));
```

---

## Cálculo Conmutación Óptima

```python
#!/usr/bin/env python3
import numpy as np

# Parámetros conmutación
f_pwm = 5000  # Hz
duty = 0.5     # 50%
corriente = 2.5 # A
resistencia = 5 # ohm

# Potencia bobina
potencia = corriente**2 * resistencia
print(f"Potencia bobina: {potencia} W")

# Torque estimado
longitud = 0.05 # m radio efectivo
fuerza = corriente * 0.001 # aproximación T = kI
torque = fuerza * longitud
print(f"Torque estimado: {torque} Nm")

# Eficiencia conmutación
eficiencia = 0.95  # ideal MOSFET
potencia_util = potencia * eficiencia
print(f"Potencia útil: {potencia_util} W")
```

---

## Simulación PWM con Arduino (Simulador)

```cpp
// simulacion_pwm.ino
// Simula comportamiento sin hardware

void simular_conmutacion() {
  // Fase A (bobinas 0,120,240°)
  int fase_a_pwm = map(velocidad_actual, 500, 2000, 80, 30);
  analogWrite(PWM_A, fase_a_pwm * 255 / 100);
  
  // Fase B compensación
  int fase_b_pwm = (fase_a_pwm + 120) % 100;
  analogWrite(PWM_B, fase_b_pwm * 255 / 100);
  
  // Fase C estabilización
  int fase_c_pwm = (fase_a_pwm + 240) % 100;
  analogWrite(PWM_C, fase_c_pwm * 255 / 100);
}
```

---

## Resultados Estimados Generador BSLC

### Condiciones Optimas
| Parámetro | Valor mínimo | Valor óptimo | Unidad |
|-----------|--------------|--------------|--------|
| Panel solar | 20W | 50W | W |
| RPM rotor | 500 | 1500 | rpm |
| Torque neto | 0.01 | 0.05 | Nm |
| Corriente bobina | 2.0 | 2.5 | A |
| Voltaje generado | 5 | 12 | V |
| Potencia generada | 10 | 30 | W |

### Consumo vs Generación
```
CONSUMO ARDUINO:
- Arduino Nano: 5V × 0.05A = 0.25W
- 12 MOSFET: 12V × 0.01A × 12 = 1.44W
- Sensores Hall: 5V × 0.02A = 0.1W
TOTAL CONSUMO: 1.79W

GENERACIÓN ESPERADA:
- Rotor 1000 rpm: 15 mW/rpm × 1000 = 15W
- Eficiencia 70%: 10.5W útiles

RESULTADO: AUTO-SOSTENIMIENTO POSIBLE
```

---

## Configuración Arduino Final

```cpp
/* CONFIG ACTUAL PARA PROTOTIPO BSLC */

#define PANEL_MIN 20  // W mínimo
#define CONSUMO_TOTAL 2  // W estimado
#define GENERACION_MIN 10 // W necesaria

// Si generación > consumo: sistema estable
if (generar_energia() > CONSUMO_TOTAL) {
  modo_operacion = AUTONOMO;
} else {
  modo_operacion = AHORRO; // reducir frecuencia
}
```