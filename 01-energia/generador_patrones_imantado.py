"""
Generador de geometrías Halbach asimétricas - BSLC Generator

Crea configuraciones óptimas de imantado para el rotor,
generando patrones de polaridad y tamaños variables
que maximicen el torque desequilibrado.

Estrategias:
- Halbach puro (ideal teórico)
- Halbach asimétrico (óptimo práctico)
- Multipolar asimétrico (más pares polares)
- Personalizado (array numpy definido por usuario)
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Callable
import json

from motor_imantado import (
    ConfiguracionRotor,
    SectorRotor,
    ConfiguracionImán,
    MotorImantado,
    TipoImantado,
)


@dataclass
class PatronImantado:
    """Patrón de imantado completo para un rotor."""
    
    nombre: str
    tipo: TipoImantado
    radio_mm: float = 50.0
    ancho_mm: float = 20.0
    grosor_mm: float = 10.0
    numero_sectores: int = 3
    pares_polos: int = 2  # Número de pares polo N-S
    polaridades: Optional[List[str]] = None
    factores_radio: Optional[List[float]] = None  # Variación de radio por sector (0-1)
    angulos_personalizados: Optional[List[float]] = None
    
    def generar_configuracion(self) -> ConfiguracionRotor:
        """Genera la ConfiguracionRotor lista para usar."""
        
        if self.tipo == TipoImantado.HALBACH_ASIMETRICO:
            return self._generar_halbach_asimetrico()
        elif self.tipo == TipoImantado.MULTIPOLAR:
            return self._generar_multipolar()
        elif self.tipo == TipoImantado.RADIAL:
            return self._generar_radial()
        elif self.tipo == TipoImantado.AXIAL:
            return self._generar_axial()
        elif self.tipo == TipoImantado.PERSONALIZADO:
            return self._generar_personalizado()
        else:
            raise ValueError(f"Tipo no soportado: {self.tipo}")
    
    def _generar_halbach_asimetrico(self) -> ConfiguracionRotor:
        """
        Halbach asimétrico: mejora del estándar con desbalance deliberado.
        
        Patrón óptimo documentado para BSLC:
        - 3 sectores con polaridades: N-S-N (crea torque neto)
        - Radios decrecientes: 100%, 90%, 80%
        - Resultado: campo rotante auto-inducido
        """
        sectores = []
        angulo_paso = 360.0 / self.numero_sectores
        
        # Secuencia de polaridades para Halbach asimétrico
        # Patrón: N→S→N (cambia en cada sector)
        polaridades = self.polaridades or ["N", "S", "N"]
        
        # Factores de radio para desbalance magnético
        factores = self.factores_radio or [1.0, 0.85, 0.7]
        
        for i in range(self.numero_sectores):
            ang_inicio = i * angulo_paso
            ang_fin = (i + 1) * angulo_paso
            radio_sector = self.radio_mm * factores[i % len(factores)]
            pol_inicio = polaridades[i % len(polaridades)]
            pol_fin = polaridades[(i + 1) % len(polaridades)]
            
            iman = ConfiguracionImán(
                radio_mm=radio_sector,
                ancho_mm=self.ancho_mm,
                grosor_mm=self.grosor_mm,
                polaridad_inicio=pol_inicio,
                polaridad_fin=pol_fin,
                angulo_inicio_deg=ang_inicio,
                angulo_fin_deg=ang_fin,
            )
            
            sector = SectorRotor(
                angulo_inicio_deg=ang_inicio,
                angulo_fin_deg=ang_fin,
                imanes=[iman],
                nombre=f"Sector_{i+1}_N{int(factores[i%len(factores)]*100)}",
            )
            sectores.append(sector)
        
        return ConfiguracionRotor(
            radio_mm=self.radio_mm,
            ancho_mm=self.ancho_mm,
            sectores=sectores,
        )
    
    def _generar_multipolar(self) -> ConfiguracionRotor:
        """Multipolar: más pares de polos para RPM bajas, alto torque."""
        sectores = []
        total_sectores = self.numero_sectores * self.pares_polos * 2
        angulo_paso = 360.0 / total_sectores
        
        # Alternar N-S-N-S... para multipolar
        polaridades_seq = []
        for _ in range(self.pares_polos):
            polaridades_seq.extend(["N", "S"] * self.numero_sectores)
        
        for i in range(total_sectores):
            ang_inicio = i * angulo_paso
            ang_fin = (i + 1) * angulo_paso
            
            # Radio decreciente para multipolar
            radio_sector = self.radio_mm * (1.0 - 0.05 * (i % self.numero_sectores))
            
            iman = ConfiguracionImán(
                radio_mm=radio_sector,
                ancho_mm=self.ancho_mm,
                grosor_mm=self.grosor_mm,
                polaridad_inicio=polaridades_seq[i],
                polaridad_fin=polaridades_seq[(i + 1) % len(polaridades_seq)],
                angulo_inicio_deg=ang_inicio,
                angulo_fin_deg=ang_fin,
            )
            
            sector = SectorRotor(
                angulo_inicio_deg=ang_inicio,
                angulo_fin_deg=ang_fin,
                imanes=[iman],
                nombre=f"Multi_{i+1}",
            )
            sectores.append(sector)
        
        return ConfiguracionRotor(
            radio_mm=self.radio_mm,
            ancho_mm=self.ancho_mm,
            sectores=sectores,
        )
    
    def _generar_radial(self) -> ConfiguracionRotor:
        """Radial: imanes apuntando hacia fuera (radialmente)."""
        sectores = []
        angulo_paso = 360.0 / self.numero_sectores
        
        for i in range(self.numero_sectores):
            ang_inicio = i * angulo_paso
            ang_fin = (i + 1) * angulo_paso
            
            iman = ConfiguracionImán(
                radio_mm=self.radio_mm,
                ancho_mm=angulo_paso * np.pi * self.radio_mm / 180,
                grosor_mm=self.grosor_mm,
                polaridad_inicio="N" if i % 2 == 0 else "S",
                polaridad_fin="S" if i % 2 == 0 else "N",
                angulo_inicio_deg=ang_inicio,
                angulo_fin_deg=ang_fin,
            )
            
            sector = SectorRotor(
                angulo_inicio_deg=ang_inicio,
                angulo_fin_deg=ang_fin,
                imanes=[iman],
                nombre=f"Radial_{i+1}",
            )
            sectores.append(sector)
        
        return ConfiguracionRotor(
            radio_mm=self.radio_mm,
            ancho_mm=self.ancho_mm,
            sectores=sectores,
        )
    
    def _generar_axial(self) -> ConfiguracionRotor:
        """Axial: imanes paralelos al eje (flujo axial)."""
        # Simplificación: equivalente a radial pero con geometría diferente
        return self._generar_radial()
    
    def _generar_personalizado(self) -> ConfiguracionRotor:
        """Genera desde ángulos personalizados."""
        if not self.angulos_personalizados:
            raise ValueError("Requiere angulos_personalizados para tipo PERSONALIZADO")
        
        sectores = []
        angulos = self.angulos_personalizados
        
        for i in range(len(angulos) - 1):
            ang_inicio = angulos[i]
            ang_fin = angulos[i + 1]
            
            iman = ConfiguracionImán(
                radio_mm=self.radio_mm,
                ancho_mm=self.ancho_mm,
                grosor_mm=self.grosor_mm,
                polaridad_inicio="N" if i % 2 == 0 else "S",
                polaridad_fin="S" if i % 2 == 0 else "N",
                angulo_inicio_deg=ang_inicio,
                angulo_fin_deg=ang_fin,
            )
            
            sector = SectorRotor(
                angulo_inicio_deg=ang_inicio,
                angulo_fin_deg=ang_fin,
                imanes=[iman],
                nombre=f"Custom_{i+1}",
            )
            sectores.append(sector)
        
        return ConfiguracionRotor(
            radio_mm=self.radio_mm,
            ancho_mm=self.ancho_mm,
            sectores=sectores,
        )
    
    def exportar_json(self, ruta_archivo: str):
        """Exporta el patrón a JSON para documentación."""
        config = self.generar_configuracion()
        
        datos = {
            "patron": {
                "nombre": self.nombre,
                "tipo": self.tipo.value,
                "radio_mm": self.radio_mm,
                "ancho_mm": self.ancho_mm,
                "grosor_mm": self.grosor_mm,
                "numero_sectores": self.numero_sectores,
                "pares_polos": self.pares_polos,
            },
            "sectores": [],
        }
        
        for sector in config.sectores:
            datos["sectores"].append({
                "nombre": sector.nombre,
                "angulo_inicio_deg": sector.angulo_inicio_deg,
                "angulo_fin_deg": sector.angulo_fin_deg,
                "imanes": [
                    {
                        "radio_mm": iman.radio_mm,
                        "ancho_mm": iman.ancho_mm,
                        "grosor_mm": iman.grosor_mm,
                        "material": iman.material,
                        "campo_residual_t": iman.campo_residual_t,
                        "polaridad": f"{iman.polaridad_inicio}-{iman.polaridad_fin}",
                        "angulo_deg": f"{iman.angulo_inicio_deg:.1f}-{iman.angulo_fin_deg:.1f}",
                    }
                    for iman in sector.iman
                ],
            })
        
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)


class OptimizadorHalbach:
    """
    Optimizador de geometrías Halbach mediante búsqueda paramétrica.
    
    Variables a optimizar:
    - Número de sectores (n)
    - Secuencia de polaridades
    - Factores de radio por sector
    - Ángulos de transición
    
    Objetivos (multi-objetivo):
    1. Maximizar desbalance magnético (torque)
    2. Minimizar consumo de material (coste)
    3. Maximizar rango RPM auto-sostenido
    """
    
    def __init__(self, motor: MotorImantado):
        self.motor = motor
        self.historial_optimizacion: List[dict] = []
    
    def evaluar_configuracion(self, patron: PatronImantado) -> dict:
        """Evalúa una configuración de imantado."""
        rotor = patron.generar_configuracion()
        
        # Calcular métricas
        desbalance = rotor.desbalance_magnetico()
        torque_teorico = rotor.torque_teorico_nm()
        
        # Coste estimado (neodimio ≈ 80€/kg, densidad 7.4 g/cm³)
        volumen_total_m3 = sum(
            sum(iman.volumen_m3 for iman in s.imanes)
            for s in rotor.sectores
        )
        masa_kg = volumen_total_m3 * 7400  # kg/m³
        coste_imanes = masa_kg * 80  # €
        
        # Número de imanes necesarios
        num_imanes = rotor.numero_imanes()
        
        # Eficiencia de material (desbalance / masa)
        if masa_kg > 0:
            eficiencia_material = desbalance / masa_kg
        else:
            eficiencia_material = 0.0
        
        return {
            "patron": patron.nombre,
            "tipo": patron.tipo.value,
            "desbalance_magnetico_am2": round(desbalance, 6),
            "torque_teorico_nm": round(torque_teorico, 6),
            "masa_imanes_kg": round(masa_kg, 4),
            "coste_imanes_eur": round(coste_imanes, 2),
            "numero_imanes": num_imanes,
            "eficiencia_material": round(eficiencia_material, 6),
            "evaluacion_torque": self._clasificar_torque(torque_teorico),
            "evaluacion_coste": self._clasificar_coste(coste_imanes),
        }
    
    def _clasificar_torque(self, torque_nm: float) -> str:
        if torque_nm > 0.1:
            return "ALTO"
        elif torque_nm > 0.01:
            return "MEDIO"
        else:
            return "BAJO"
    
    def _clasificar_coste(self, coste_eur: float) -> str:
        if coste_eur < 20:
            return "ECONÓMICO"
        elif coste_eur < 50:
            return "MODERADO"
        else:
            return "ALTO"
    
    def comparar_patrones(
        self,
        patrones: List[PatronImantado],
    ) -> List[dict]:
        """Compara múltiples patrones y retorna ranking."""
        resultados = []
        
        for patron in patrones:
            eval_result = self.evaluar_configuracion(patron)
            resultados.append(eval_result)
            self.historial_optimizacion.append(eval_result)
        
        # Ordenar por desbalance magnético (mayor torque potencial)
        resultados.sort(key=lambda x: x["desbalance_magnetico_am2"], reverse=True)
        
        # Añadir ranking
        for i, res in enumerate(resultados):
            res["ranking"] = i + 1
        
        return resultados
    
    def optimizar_secuencia_polaridad(
        self,
        numero_sectores: int = 3,
        objetivo: str = "torque",
    ) -> List[str]:
        """
        Busca la secuencia de polaridades óptima para N sectores.
        
        Objetivos:
        - "torque": maximizar desbalance -> secuencias asimétricas
        - "suave": minimizar vibraciones -> equilibrio cercano a simetría
        - "efficiencia": maximizar eficiencia material -> mínimo imanes necesarios
        """
        mejor_score = -1
        mejor_secuencia = []
        
        # Generar todas las permutaciones posibles de N/S
        from itertools import product
        combinaciones = list(product(["N", "S"], repeat=numero_sectores))
        
        for seq in combinaciones:
            patron = PatronImantado(
                nombre=f"Optimized_{'-'.join(seq)}",
                tipo=TipoImantado.HALBACH_ASIMETRICO,
                numero_sectores=numero_sectores,
                polaridades=list(seq),
            )
            
            eval_res = self.evaluar_configuracion(patron)
            score = eval_res["desbalance_magnetico_am2"]
            
            if objetivo == "suave":
                score = -abs(eval_res["torque_teorico_nm"] - 0.05)
            
            if score > mejor_score:
                mejor_score = score
                mejor_secuencia = list(seq)
        
        return mejor_secuencia
    
    def generar_recomendacion(self, presupuesto_eur: float = 50.0) -> dict:
        """Genera una recomendación óptima para un presupuesto dado."""
        # Buscar en historial o generar configuraciones
        recomendaciones = []
        
        for n_sectores in [2, 3, 4, 5, 6]:
            for factores in [
                [1.0, 0.8, 0.6],
                [1.0, 0.9, 0.7],
                [1.0, 0.85, 0.65],
            ]:
                patron = PatronImantado(
                    nombre=f"Eval_{n_sectores}s",
                    tipo=TipoImantado.HALBACH_ASIMETRICO,
                    numero_sectores=n_sectores,
                    factores_radio=factores,
                )
                eval_res = self.evaluar_configuracion(patron)
                recomendaciones.append(eval_res)
        
        # Filtrar por presupuesto
        viables = [r for r in recomendaciones if r["coste_imanes_eur"] <= presupuesto_eur]
        
        if not viables:
            return {
                "advertencia": f"Presupuesto {presupuesto_eur}€ muy bajo para configuraciones viables",
                "minimo_requerido": min(r["coste_imanes_eur"] for r in recomendaciones),
            }
        
    # Seleccionar mejor opción (ranking por desbalance/coste)
    if viables:
        viables.sort(key=lambda x: x["desbalance_magnetico_am2"] / max(1, x["coste_imanes_eur"]), reverse=True)
        mejor = viables[0]
        
        return {
            "recomendacion": mejor,
            "alternativas_top3": viables[:3],
            "presupuesto_utilizado_eur": mejor["coste_imanes_eur"],
            "presupuesto_restante_eur": presupuesto_eur - mejor["coste_imanes_eur"],
        }
    else:
        return {
            "advertencia": f"Presupuesto {presupuesto_eur}€ muy bajo para configuraciones viables",
            "minimo_requerido": min(r["coste_imanes_eur"] for r in recomendaciones),
        }


def crear_patron_bslc_optimo() -> PatronImantado:
    """
    Crea el patrón óptimo para BSLC basado en análisis previo.
    
    Especificaciones del generador BSLC documentado:
    - 3 sectores asimétricos
    - Radios: 40mm, 30mm, 20mm (N52)
    - Polaridades: N-S-N, S-N-S, N-S
    """
    return PatronImantado(
        nombre="BSLC_v1_Optimo",
        tipo=TipoImantado.HALBACH_ASIMETRICO,
        radio_mm=50.0,
        ancho_mm=20.0,
        grosor_mm=10.0,
        numero_sectores=3,
        polaridades=["N", "S", "N"],
        factores_radio=[0.8, 0.6, 0.4],  # 40mm, 30mm, 20mm sobre 50mm
    )


if __name__ == "__main__":
    # Demo: comparar patrones
    from motor_imantado import MotorImantado
    
    motor = MotorImantado()
    
    optimizador = OptimizadorHalbach(motor)
    
    # Comparar configuraciones alternativas
    patrones = [
        PatronImantado("BSLC_Optimo_3s", TipoImantado.HALBACH_ASIMETRICO, numero_sectores=3,
                       polaridades=["N", "S", "N"], factores_radio=[1.0, 0.85, 0.7]),
        PatronImantado("BSLC_Alt_4s", TipoImantado.HALBACH_ASIMETRICO, numero_sectores=4,
                       polaridades=["N", "S", "N", "S"], factores_radio=[1.0, 0.9, 0.8, 0.7]),
        PatronImantado("Multipolar_6p", TipoImantado.MULTIPOLAR, numero_sectores=3, pares_polos=2,
                       polaridades=["N", "S"], factores_radio=[1.0, 0.95]),
        PatronImantado("Minimalista_2s", TipoImantado.HALBACH_ASIMETRICO, numero_sectores=2,
                       polaridades=["N", "S"], factores_radio=[1.0, 0.9]),
    ]
    
    resultados = optimizador.comparar_patrones(patrones)
    
    print("=" * 70)
    print("ANÁLISIS COMPARATIVO PATRONES DE IMANTADO - BSLC")
    print("=" * 70)
    
    for res in resultados:
        print(f"\nRanking #{res['ranking']}: {res['patron']}")
        print(f"  Tipo: {res['tipo']}")
        print(f"  Desbalance magnético: {res['desbalance_magnetico_am2']:.6f} A·m²")
        print(f"  Torque teórico:       {res['torque_teorico_nm']:.6f} N·m")
        print(f"  Masa imanes:          {res['masa_imanes_kg']:.4f} kg ({res['coste_imanes_eur']:.2f}€)")
        print(f"  Nº imanes:            {res['numero_imanes']}")
        print(f"  Evaluación torque:    {res['evaluacion_torque']}")
        print(f"  Evaluación coste:     {res['evaluacion_coste']}")
    
    print("\n" + "=" * 70)
    
    # Recomendación para presupuesto 50€
    rec = optimizador.generar_recomendacion(presupuesto_eur=50.0)
    print("\nRECOMENDACIÓN PARA PRESUPUESTO 50€:")
    print(f"  Configuración: {rec['recomendacion']['patron']}")
    print(f"  Coste imanes:  {rec['recomendacion']['coste_imanes_eur']:.2f}€")
    print(f"  Torque:        {rec['recomendacion']['torque_teorico_nm']:.4f} N·m")
    print(f"  Presupuesto restante: {rec['presupuesto_restante_eur']:.2f}€")
