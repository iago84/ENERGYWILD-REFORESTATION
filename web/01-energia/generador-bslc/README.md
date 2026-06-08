# BSLC Magnetic Generator

> Sub-repo del proyecto ENERGYWILD enfocado en el diseño, documentación y prototipado del generador eléctrico por conmutación magnética con IA.

## Estructura

- `src/` — Código fuente del modelo conceptual del motor/generador.
- `notebooks/` — Cuadernos de análisis y diagramas.
- `tests/` — Pruebas unitarias (si aplican).
- `data/` — Datos de entrada/salida del modelo.
- `modelo_bslc_blender.py` — Modelo paramétrico Blender 3+.

## Estado

Borrador conceptual sin validar experimentalmente.
Consulte `prompt-revision-especialista.md` para handoff a especialista en electromagnetismo.

## Ejecutar modelo Blender

```bash
blender --background --python modelo_bslc_blender.py
```

## Archivos principales

- `diagramas-concepto-bslc.md`
- `ficha-tecnica-bslc.md`
- `prompt-revision-especialista.md`
- `generador-bslc-magnetico.md`
- `motor_imantado.py`
- `generador_patrones_imantado.py`
- `modelo_bslc_blender.py`
