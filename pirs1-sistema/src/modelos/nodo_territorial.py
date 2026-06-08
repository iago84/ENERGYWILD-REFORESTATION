"""
PIRS-1: Programa Integrado de Regeneración del Sahel
Nodo Territorial - Modelo de unidad autónoma de regeneración

Autor: Yago Otero (Naira Studio LTD)
Licencia: MIT
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date


@dataclass
class NodoTerritorial:
    """
    Representa un nodo de regeneración territorial de 1 hectárea.
    
    Cada nodo es una unidad autónoma que integra:
    - Agua: captación atmosférica + almacenamiento subterráneo
    - Suelo: biochar + micorrizas + compost
    - Agricultura: cultivos base + vertical + agroforestería
    - Energía: solar + almacenamiento LFP + LED
    - Protección: geotextiles + barreras vegetales + corredores
    """
    
    id_nodo: str                      # ID único: PIRS-001, PIRS-002...
    coordenadas_lat: float            # Latitud decimal
    coordenadas_lon: float            # Longitud decimal
    region: str                       # Región: Ségou, Mopti, Tombouctou...
    fase: int = 1                     # Fase: 1=Diagnóstico, 2=Base, 3=Expansión, 4=Consolidación
    superficie_ha: float = 1.0        # Hectáreas del nodo
    
    # === MÓDULO AGUA ===
    # Captación atmosférica (fog harvesting + condensación radiativa)
    captacion_atmosferica_l_dia: float = 0.0      # Litros/día captados del aire
    capacidad_cisterna_m3: float = 50.0           # m³ almacenamiento subterráneo
    nivel_freatico_actual_m3: float = 0.0         # m³ disponibles actualmente
    
    # Subterránea
    profundidad_pozo_m: float = 0.0               # Metros de profundidad
    caudal_pozo_l_h: float = 0.0                  # Litros/hora del pozo
    bomba_solar_w: float = 0.0                    # Potencia bomba solar (W)
    
    # === MÓDULO SUELO ===
    humedad_suelo_pct: float = 5.0                # % humedad del suelo
    biochar_aplicado_kg_m2: float = 0.0           # kg/m² biochar aplicado
    micorrizas_aplicadas: bool = False
    capa_mulch_cm: float = 0.0                    # cm de mulch orgánico
    ph_suelo: float = 7.5                         # pH inicial
    
    # === MÓDULO AGRICULTURA ===
    area_cultivo_ha: float = 0.6                  # Hectáreas de cultivo activo
    area_vertical_m2: float = 0.0                  # m² agricultura vertical
    area_bosque_ha: float = 0.25                  # Hectáreas de bosque climático
    nopal_plantas: int = 0                        # Número de plantas Opuntia
    arboles_plantados: int = 0                    # Acacia + moringa + neem
    cultivos_activos: List[str] = field(default_factory=lambda: [])
    
    # === MÓDULO ENERGÍA ===
    panel_solar_w: float = 0.0                    # Potencia paneles solares (W)
    bateria_lfp_kwh: float = 0.0                  # Capacidad batería (kWh)
    inversion_potencia_kw: float = 0.0            # Inversor (kW)
    iluminacion_led_w: float = 0.0                # Iluminación puntual (W)
    microeolica_w: float = 0.0                    # Microturbina eólica (W)
    
    # === ESTADO Y MÉTRICAS ===
    estado: str = "planificado"                   # planificado/activo/consolidado/madurado
    fecha_inicio: Optional[date] = None
    fecha_ultimo_mantenimiento: Optional[date] = None
    
    # Métricas calculadas
    agua_captada_acumulada_l: float = 0.0
    co2_secuestrado_kg: float = 0.0
    supervivencia_cultivos_pct: float = 0.0
    productividad_kg_ha: float = 0.0
    erosion_reducida_pct: float = 0.0
    
    def __post_init__(self):
        """Validar coordenadas Mali y coherencia de parámetros."""
        # Validar bounds de Mali
        if not (10.0 <= self.coordenadas_lat <= 25.0):
            raise ValueError(f"Latitud fuera de rango Mali: {self.coordenadas_lat}")
        if not (-12.0 <= self.coordenadas_lon <= 4.0):
            raise ValueError(f"Longitud fuera de rango Mali: {self.coordenadas_lon}")
        
        # Validar superficie total
        area_total = self.area_cultivo_ha + self.area_vertical_m2 / 10000 + self.area_bosque_ha
        if area_total > self.superficie_ha:
            raise ValueError(
                f"Áreas asignadas ({area_total:.2f} ha) exceden superficie ({self.superficie_ha} ha)"
            )
    
    def descripcion_breve(self) -> str:
        """Resumen descriptivo del nodo para reportes."""
        return (
            f"PIRS-{self.id_nodo}: {self.region} "
            f"({self.coordenadas_lat:.2f}N, {self.coordenadas_lon:.2f}E) "
            f"| Fase {self.fase} | {self.superficie_ha}ha "
            f"| Agua: {self.capacidad_cisterna_m3}m³ "
            f"| Energía: {self.panel_solar_w}W"
        )
