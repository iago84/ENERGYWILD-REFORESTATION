"""
Simulación hídrica del sistema de regeneración PIRS-1

Modelo simplificado del balance hídrico de un nodo territorial:
    ΔW = P + C + G - E - T - U

Donde:
    ΔW = cambio en agua almacenada (L)
    P  = precipitación (L)
    C  = condensación atmosférica (L)
    G  = aporte subterráneo (L)
    E  = evaporación (L)
    T  = transpiración vegetal (L)
    U  = uso humano/agricola (L)
"""

import math
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ParametrosClimaticos:
    """Parámetros climáticos para la simulación."""
    
    precipitacion_media_anual_mm: float = 300.0       # mm/año (Sahel)
    estacion_lluvias_meses: Tuple[int, int] = (6, 9)  # Jun-Sep
    temperatura_media_c: float = 30.0                  # °C
    humedad_relativa_media_pct: float = 35.0           # %
    radiacion_solar_kwh_m2_dia: float = 6.0            # kWh/m²/día
    viento_velocidad_media_ms: float = 5.0             # m/s (Harmattan)
    
    # Coeficientes de evaporación
    evapotranspiracion_referencia_mm_dia: float = 7.0  # ETo diaria (mm)
    coeficiente_cultivo_ke: float = 0.8                 # Cultivos adaptados
    factor_reduccion_sombra: float = 0.7               # Reducción por sombreado 40%


@dataclass
class ParametrosSuelo:
    """Propiedades del suelo en el nodo."""
    
    capacidad_campo_pct: float = 25.0          # % humedad capacidad de campo
    punto_marchitez_pct: float = 8.0            # % punto de marchitez
    conductividad_hidraulica_mm_h: float = 5.0  # mm/h
    profundidad_efectiva_cm: float = 80.0       # cm capa activa
    cobertura_mulch_pct: float = 30.0           # % reducción evaporación por mulch


@dataclass
class ParametrosCaptacion:
    """Eficiencia de sistemas de captación de agua."""
    
    rendimiento_fog_l_m2_dia: float = 5.0       # L/m²/día niebla
    area_fog_m2: float = 25.0                    # m² mallas instaladas
    rendimiento_condensacion_l_m2_dia: float = 0.5  # L/m²/día radiación nocturna
    area_condensacion_m2: float = 10.0            # m² paneles condensación
    rendimiento_deshumidificador_l_dia: float = 2.0  # L/día solar activo


@dataclass
class ParametrosVegetacion:
    """Características de la vegetación del nodo."""
    
    area_cultivo_ha: float = 0.6
    area_bosque_ha: float = 0.25
    densidad_arboles_ha: int = 200                 # árboles por hectárea
    transpiración_arbol_l_dia: float = 15.0        # L/día árbol maduro (acacia)
    coeficiente_transpiracion_cultivos: float = 0.6 # Factor cultivos adaptados


class SimuladorHidricoPIRS1:
    """
    Simulador del balance hídrico anual para un nodo PIRS-1.
    
    Modela la evolución mes a mes de:
    - Agua captada (atmósfera + subterránea + precipitación)
    - Agua consumida (evaporación + transpiración + uso humano)
    - Almacenamiento en cisterna y suelo
    
    Variables de estado:
        almacenamiento_suelo_mm: humedad del suelo
        almacenamiento_cisterna_l: agua en cisterna
    """
    
    def __init__(
        self,
        clima: ParametrosClimaticos,
        suelo: ParametrosSuelo,
        captacion: ParametrosCaptacion,
        vegetacion: ParametrosVegetacion,
        capacidad_cisterna_l: float = 50000.0,
        uso_humano_l_dia: float = 100.0,  # 50-200 personas × 2L
    ):
        self.clima = clima
        self.suelo = suelo
        self.captacion = captacion
        self.vegetacion = vegetacion
        self.capacidad_cisterna_l = capacidad_cisterna_l
        self.uso_humano_l_dia = uso_humano_l_dia
        
        # Estado inicial
        self.almacenamiento_suelo_mm = self.suelo.punto_marchitez_pct  # Mínimo inicial
        self.almacenamiento_cisterna_l = 0.0
        self.historial: List[Dict] = []
    
    def paso_mensual(self, mes: int, año: int = 1) -> Dict:
        """
        Simula un mes completo del ciclo hídrico.
        
        Parámetros:
            mes: 1-12 (enero=1, diciembre=12)
            año: año de simulación (afecta desarrollo vegetación)
        
        Retorna:
            Diccionario con resultados del mes
        """
        
        # 1. Determinar si es temporada de lluvias
        en_estacion_lluvias = self.clima.estacion_lluvias_meses[0] <= mes <= self.clima.estacion_lluvias_meses[1]
        
        # 2. Calcular precipitación del mes
        if en_estacion_lluvias:
            meses_lluvia = self.clima.estacion_lluvias_meses[1] - self.clima.estacion_lluvias_meses[0] + 1
            precipitacion_mm_mes = self.clima.precipitacion_media_anual_mm / meses_lluvia
        else:
            precipitacion_mm_mes = 0.0
        
        # Convertir mm a litros (1 mm = 10 L/m²)
        area_nodo_m2 = 10000  # 1 ha = 10,000 m²
        precipitacion_l = precipitacion_mm_mes * area_nodo_m2 / 10.0
        
        # 3. Captación atmosférica (fog + condensación)
        # Ajustar por estación: Harmattan (nov-mar) tiene mayor niebla
        es_harmattan = mes in [11, 12, 1, 2, 3]
        factor_harmattan = 1.5 if es_harmattan else 0.6
        
        dias_mes = 30
        captacion_fog_l = (
            self.captacion.rendimiento_fog_l_m2_dia
            * self.captacion.area_fog_m2
            * dias_mes
            * factor_harmattan
        )
        captacion_condensacion_l = (
            self.captacion.rendimiento_condensacion_l_m2_dia
            * self.captacion.area_condensacion_m2
            * dias_mes
        )
        captacion_atm_l = captacion_fog_l + captacion_condensacion_l
        
        # 4. Deshumidificador solar (solo en estación seca)
        captacion_solar_l = 0.0
        if not en_estacion_lluvias:
            captacion_solar_l = self.captacion.rendimiento_deshumidificador_l_dia * dias_mes
        
        captacion_total_l = precipitacion_l + captacion_atm_l + captacion_solar_l
        
        # 5. Evaporación del suelo (E)
        # ETo mensual ajustada por cultivo y cobertura
        eto_mensual_mm = self.clima.evapotranspiracion_referencia_mm_dia * dias_mes / 30.0
        ke_ajustado = self.clima.coeficiente_cultivo_ke * self.clima.factor_reduccion_sombra
        evapotranspiracion_mm = eto_mensual_mm * ke_ajustado
        evaporacion_l_m2 = evapotranspiracion_mm * area_nodo_m2 / 10.0 * (1 - self.suelo.cobertura_mulch_pct / 100)
        evaporizacion_suelo_l = evaporacion_l_m2 * area_nodo_m2 / 10000  # Convertir a litros totales
        
        # 6. Transpiración vegetal (T)
        # Nudos por hectárea (200 árboles/ha en zona bosque + desarrollo árboles en cultivo)
        area_bosque_m2 = self.vegetacion.area_bosque_ha * 10000
        arboles_bosque = self.vegetacion.densidad_arboles_ha * self.vegetacion.area_bosque_ha
        
        # Desarrollo vegetal aumenta con los años
        factor_desarrollo = min(1.0, año * 0.25)  # Año 1: 25%, Año 4: 100%
        
        transp_arboles_l = (
            arboles_bosque
            * self.vegetacion.transpiración_arbol_l_dia
            * dias_mes
            * factor_desarrollo
        )
        transp_cultivos_l = (
            self.vegetacion.area_cultivo_ha
            * 10000
            * evapotranspiracion_mm
            * self.vegetacion.coeficiente_transpiracion_cultivos
            / 10.0
        )
        transpiración_total_l = transp_arboles_l + transp_cultivos_l
        
        # 7. Uso humano/agrícola (U)
        uso_total_l = self.uso_humano_l_dia * dias_mes
        
        # 8. Balance hídrico del suelo
        infiltracion_l = precipitacion_l * 0.7  # 70% infiltración efectiva en suelo arenoso
        escorrentia_l = precipitacion_l * 0.15   # 15% escorrentía recuperable
        recarga_l = infiltracion_l + escorrentia_l
        
        # Actualizar almacenamiento suelo (simplificado)
        capacidad_suelo_l = (
            self.suelo.capacidad_campo_pct
            * self.suelo.profundidad_efectiva_cm
            * area_nodo_m2
            / 100.0
        )
        variacion_suelo_mm = (recarga_l - evaporizacion_suelo_l - transpiración_total_l) / area_nodo_m2 * 10
        self.almacenamiento_suelo_mm = max(
            self.suelo.punto_marchitez_pct,
            min(self.suelo.capacidad_campo_pct, self.almacenamiento_suelo_mm + variacion_suelo_mm)
        )
        
        # 9. Almacenamiento cisterna
        excedente_l = max(0, captacion_total_l - evaporizacion_suelo_l - transpiración_total_l - uso_total_l)
        self.almacenamiento_cisterna_l = min(
            self.capacidad_cisterna_l,
            self.almacenamiento_cisterna_l + excedente_l
        )
        
        # Resultados del mes
        resultado = {
            "mes": mes,
            "año": año,
            "estacion_lluvias": en_estacion_lluvias,
            "precipitacion_mm": round(precipitacion_mm_mes, 1),
            "captacion_atm_l": round(captacion_atm_l, 0),
            "captacion_solar_l": round(captacion_solar_l, 0),
            "captacion_total_l": round(captacion_total_l, 0),
            "evaporizacion_suelo_l": round(evaporizacion_suelo_l, 0),
            "transpiracion_l": round(transpiración_total_l, 0),
            "uso_humano_l": round(uso_total_l, 0),
            "excedente_l": round(excedente_l, 0),
            "almacenamiento_suelo_mm": round(self.almacenamiento_suelo_mm, 1),
            "almacenamiento_cisterna_l": round(self.almacenamiento_cisterna_l, 0),
            "factor_desarrollo_vegetal": round(factor_desarrollo, 2),
        }
        
        self.historial.append(resultado)
        return resultado
    
    def simular_año(self, año: int = 1) -> List[Dict]:
        """Simula un año completo (12 meses) y retorna resultados mensuales."""
        return [self.paso_mensual(mes=m, año=año) for m in range(1, 13)]
    
    def simular_multianual(self, años: int = 5) -> List[Dict]:
        """Simula múltiples años consecutivos."""
        resultados = []
        for año in range(1, años + 1):
            resultados.extend(self.simular_año(año=año))
        return resultados
    
    def resumen_anual(self, año: int = 1) -> Dict:
        """Genera resumen agregado de un año completo."""
        datos_año = [r for r in self.historial if r["año"] == año]
        
        if not datos_año:
            return {}
        
        captacion_total = sum(r["captacion_total_l"] for r in datos_año)
        evaporizacion_total = sum(r["evaporizacion_suelo_l"] for r in datos_año)
        transpiración_total = sum(r["transpiracion_l"] for r in datos_año)
        uso_total = sum(r["uso_humano_l"] for r in datos_año)
        
        humedad_promedio = sum(r["almacenamiento_suelo_mm"] for r in datos_año) / len(datos_año)
        cisterna_final = datos_año[-1]["almacenamiento_cisterna_l"]
        
        return {
            "año": año,
            "captacion_total_l": round(captacion_total, 0),
            "evaporizacion_total_l": round(evaporizacion_total, 0),
            "transpiracion_total_l": round(transpiración_total, 0),
            "uso_total_l": round(uso_total, 0),
            "excedente_total_l": round(captacion_total - evaporizacion_total - transpiración_total - uso_total, 0),
            "humedad_suelo_promedio_mm": round(humedad_promedio, 1),
            "cisterna_final_l": round(cisterna_final, 0),
            "estado_hidrico": self._evaluar_estado_hidrico(captacion_total, uso_total),
        }
    
    def _evaluar_estado_hidrico(self, entrada_l: float, salida_l: float) -> str:
        """Evalúa viabilidad hídrica del nodo."""
        ratio = entrada_l / salida_l if salida_l > 0 else 0
        
        if ratio >= 1.2:
            return "EXCEDENTE_HIDRICO"
        elif ratio >= 0.9:
            return "BALANCE_ESTABLE"
        elif ratio >= 0.7:
            return "DEFICIT_LEVE"
        else:
            return "DEFICIT_CRITICO"
    
    def obtener_kpis(self) -> Dict:
        """KPIs principales del sistema hídrico."""
        if not self.historial:
            return {}
        
        ultimo = self.historial[-1]
        
        # Cálculo de captación anual
        datos_ultimo_año = [r for r in self.historial if r["año"] == ultimo["año"]]
        captacion_anual = sum(r["captacion_total_l"] for r in datos_ultimo_año)
        
        # Eficiencia de captación
        area_captacion_total = self.captacion.area_fog_m2 + self.captacion.area_condensacion_m2
        eficiencia_captacion = captacion_anual / area_captacion_total if area_captacion_total > 0 else 0
        
        return {
            "almacenamiento_suelo_actual_mm": round(self.almacenamiento_suelo_mm, 1),
            "capacidad_campo_mm": self.suelo.capacidad_campo_pct,
            "porcentaje_capacidad": round(self.almacenamiento_suelo_mm / self.suelo.capacidad_campo_pct * 100, 0),
            "cisterna_litros_actuales": round(self.almacenamiento_cisterna_l, 0),
            "capacidad_cisterna_l": self.capacidad_cisterna_l,
            "captacion_anual_l": round(captacion_anual, 0),
            "eficiencia_captacion_l_m2_año": round(eficiencia_captacion, 0),
            "humedad_porcentaje": round(self.almacenamiento_suelo_mm, 1),
            "estado": self._evaluar_estado_hidrico(
                captacion_anual,
                sum(r["uso_humano_l"] for r in datos_ultimo_año)
                + sum(r["transpiracion_l"] for r in datos_ultimo_año)
            ),
        }
