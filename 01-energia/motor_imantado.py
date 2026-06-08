"""
Motor de patrones de imantado - BSLC Magnetic Generator

Modela el sistema de generación eléctrica por conmutación magnética:
- Rotor con imanes permanentes en geometría Halbach asimétrica
- Estator con bobinas de inducción
- Campo magnético total: B_total = B_permanente + B_inducido

Autor: Yago Otero (Naira Studio LTD)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from enum import Enum


class TipoImantado(Enum):
    """Estrategias de imantado para el rotor."""
    HALBACH_ASIMETRICO = "halbach_asimetrico"
    MULTIPOLAR = "multipolar"
    RADIAL = "radial"
    AXIAL = "axial"
    PERSONALIZADO = "personalizado"


@dataclass
class ConfiguracionImán:
    """Define un imán permanente del rotor."""
    
    radio_mm: float = 40.0
    ancho_mm: float = 10.0
    grosor_mm: float = 10.0
    material: str = "N52"
    campo_residual_t: float = 1.4  # Tesla (N52 ≈ 1.4T)
    polaridad_inicio: str = "N"    # N o S
    polaridad_fin: str = "S"       # N o S
    angulo_inicio_deg: float = 0.0
    angulo_fin_deg: float = 120.0
    
    @property
    def area_m2(self) -> float:
        return (self.radio_mm / 1000) ** 2 * np.pi
    
    @property
    def volumen_m3(self) -> float:
        return self.area_m2 * (self.grosor_mm / 1000)
    
    @property
    def momento_magnetico_am2(self) -> float:
        """Momento dipolar magnético aproximado."""
        return self.campo_residual_t * self.volumen_m3 / (4 * np.pi * 1e-7)


@dataclass
class SectorRotor:
    """Un sector del rotor con uno o más imanes."""
    
    angulo_inicio_deg: float
    angulo_fin_deg: float
    imanes: List[ConfiguracionImán] = field(default_factory=list)
    nombre: str = ""
    
    def campo_magnetico_en(self, r: float, theta: float) -> Tuple[float, float]:
        """
        Calcula el campo magnético producido por este sector
        en coordenadas polares (r, theta) en metros y radianes.
        
        Retorna (Br, Btheta) en Tesla.
        """
        Br_total = 0.0
        Btheta_total = 0.0
        
        theta_deg = np.degrees(theta) % 360
        
        for iman in self.iman:
            # Contribución del dipolo (simplificación para diseño)
            # Campo decae con el cubo de la distancia
            dist = max(0.05, r)  # Mínimo 5cm para evitar singularidad
            factor = self.iman.momento_magnetico_am2 / (4 * np.pi * dist ** 3)
            
            # Dirección del dipolo (radial vs tangencial según polaridad)
            if iman.polaridad_inicio == iman.polaridad_fin:
                # Dipolo radial
                Br_total += factor * np.cos(2 * theta)
                Btheta_total += factor * np.sin(2 * theta)
            else:
                # Dipolo tangencial (más torque)
                Br_total += factor * np.sin(2 * theta)
                Btheta_total += factor * np.cos(2 * theta)
        
        return Br_total, Btheta_total


@dataclass
class ConfiguracionBovina:
    """Define una bobina del estator."""
    
    numero_vueltas: int = 500
    seccion_mm2: float = 1.0
    resistencia_ohm: float = 5.0
    radio_mm: float = 60.0       # Radio de la bobina
    angulo_deg: float = 0.0      # Posición angular centro
    ancho_deg: float = 30.0      # Ancho angular de la bobina
    inductancia_mh: float = 10.0 # Inductancia aproximada
    
    @property
    def area_bobina_m2(self) -> float:
        return np.pi * (self.radio_mm / 1000) ** 2
    
    def flujo_enlace_wb(self, campo_b_normal: float) -> float:
        """Flujo concatenado: Φ = B × A × N."""
        return campo_b_normal * self.area_bobina_m2 * self.numero_vueltas
    
    def voltaje_inducido_v(self, db_dt: float) -> float:
        """Ley de Faraday: V = -N × dΦ/dt."""
        return -self.numero_vueltas * self.area_bobina_m2 * db_dt


@dataclass
class ConfiguracionRotor:
    """Configuración completa del rotor."""
    
    radio_mm: float = 50.0
    ancho_mm: float = 20.0
    peso_g: float = 250.0
    inercia_kgm2: float = 1e-4  # 0.0001 kg·m²
    sectores: List[SectorRotor] = field(default_factory=list)
    
    def numero_imanes(self) -> int:
        return sum(len(s.imanes) for s in self.sectores)
    
    def desbalance_magnetico(self) -> float:
        """
        Calcula el desbalance magnético del rotor.
        Valor alto = mayor torque neto posible.
        """
        if not self.sectores:
            return 0.0
        
        momentos = []
        for sector in self.sectores:
            for iman in sector.imanes:
                momentos.append(iman.momento_magnetico_am2)
        
        # Suma vectorial de momentos
        suma_x = 0.0
        suma_y = 0.0
        for i, m in enumerate(momentos):
            angulo = np.radians(i * 360 / len(momentos))
            suma_x += m * np.cos(angulo)
            suma_y += m * np.sin(angulo)
        
        # Desbalance = magnitud de la suma (no es cero si es asimétrico)
        return np.sqrt(suma_x**2 + suma_y**2)
    
    def torque_teorico_nm(self, campo_estator_t: float = 0.1) -> float:
        """Torque aproximado: τ = r × F = r × (B × I × L)."""
        r = self.radio_mm / 1000  # metros
        # Fuerza magnética aproximada en el entrehierro
        F = campo_estator_t * self.ancho_mm / 1000 * 1.0  # Corriente implícita 1A
        return r * F


@dataclass
class ConfiguracionEstator:
    """Configuración completa del estator."""
    
    radio_mm: float = 60.0
    numero_bobinas: int = 12
    bobinas: List[ConfiguracionBovina] = field(default_factory=list)
    
    def generar_bobinas_circunferenciales(
        self,
        vueltas: int = 500,
        seccion_mm2: float = 1.0,
        resistencia_ohm: float = 5.0,
        ancho_deg: float = 30.0,
    ):
        """Genera bobinas distribuidas uniformemente alrededor del estator."""
        self.bobinas = []
        angulo_paso = 360.0 / self.numero_bobinas
        
        for i in range(self.numero_bobinas):
            bobina = ConfiguracionBovina(
                numero_vueltas=vueltas,
                seccion_mm2=seccion_mm2,
                resistencia_ohm=resistencia_ohm,
                radio_mm=self.radio_mm,
                angulo_deg=i * angulo_paso,
                ancho_deg=ancho_deg,
            )
            self.bobinas.append(bobina)
    
    def campo_magnetico_inducido_t(self, corriente_a: float) -> float:
        """Campo magnético generado por una bobina con corriente I."""
        if not self.bobinas:
            return 0.0
        
        # Campo aproximado de una bobina circular: B = μ₀ × N × I / (2 × R)
        mu0 = 4 * np.pi * 1e-7
        bobina = self.bobinas[0]
        B_single = mu0 * bobina.numero_vueltas * corriente_a / (2 * bobina.radio_mm / 1000)
        
        # Contribución total (simplificación: suma de campos)
        return B_single * len(self.bobinas)


@dataclass
class EstadoConmutacion:
    """Estado de conmutación en un instante dado."""
    
    tiempo_s: float = 0.0
    posicion_rotor_deg: float = 0.0
    velocidad_rpm: float = 0.0
    corrientes_bobinas: List[float] = field(default_factory=list)
    campos_bobinas_t: List[float] = field(default_factory=list)
    campo_total_t: float = 0.0
    torque_nm: float = 0.0
    voltaje_inducido_v: float = 0.0
    potencia_generada_w: float = 0.0
    
    def eficiencia(self) -> float:
        """Eficiencia instantánea (potencia out / potencia in)."""
        potencia_consumo = sum(
            i**2 * 5.0 for i in self.corrientes_bobinas  # R ≈ 5Ω
        )
        if potencia_consumo <= 0:
            return 0.0
        return min(1.0, self.potencia_generada_w / potencia_consumo)


class MotorImantado:
    """
    Motor/generador de conmutación magnética BSLC.
    
    Integra:
    - Rotor con geometría de imanes definida
    - Estator con bobinas distribuidas
    - Simulación de campo magnético y torque
    - Control de conmutación (Arduino lógico)
    """
    
    def __init__(
        self,
        rotor: Optional[ConfiguracionRotor] = None,
        estator: Optional[ConfiguracionEstator] = None,
    ):
        self.rotor = rotor or ConfiguracionRotor()
        self.estator = estator or ConfiguracionEstator()
        
        if not self.estator.bobinas:
            self.estator.generar_bobinas_circunferenciales()
        
        # Estado dinámico
        self.posicion_deg: float = 0.0
        self.velocidad_rpm: float = 0.0
        self.historial_estados: List[EstadoConmutacion] = []
        self.secuencia_conmutacion: List[List[bool]] = []
    
    def configurar_halbach_asimetrico(
        self,
        sectores: int = 3,
        radio_mm: float = 50.0,
        ancho_mm: float = 20.0,
        grosor_mm: float = 10.0,
    ) -> ConfiguracionRotor:
        """
        Genera un rotor con geometría Halbach asimétrica.
        
        Diseño óptimo para torque variable sin equilibrio:
        - Sectores con polaridades diferentes
        - Imanes de tamaños decrecientes (o variables)
        - Resultado: rotor "quiere" girar siempre
        """
        angulo_paso = 360.0 / sectores
        sectores_config = []
        
        # Secuencia de polaridades para desbalance
        polaridades = ["N", "S", "N"]  # Asimétrico base
        
        for i in range(sectores):
            ang_inicio = i * angulo_paso
            ang_fin = (i + 1) * angulo_paso
            
            # Variar tamaño para asimetría
            radio_variado = radio_mm * (1.0 - 0.1 * i)  # 90%, 80%, 70%
            
            iman = ConfiguracionImán(
                radio_mm=radio_variado,
                ancho_mm=ancho_mm,
                grosor_mm=grosor_mm,
                polaridad_inicio=polaridades[i % len(polaridades)],
                polaridad_fin=polaridades[(i + 1) % len(polaridades)],
                angulo_inicio_deg=ang_inicio,
                angulo_fin_deg=ang_fin,
            )
            
            sector = SectorRotor(
                angulo_inicio_deg=ang_inicio,
                angulo_fin_deg=ang_fin,
                imanes=[iman],
                nombre=f"Sector_{i+1}",
            )
            sectores_config.append(sector)
        
        rotor = ConfiguracionRotor(
            radio_mm=radio_mm,
            ancho_mm=ancho_mm,
            sectores=sectores_config,
        )
        
        self.rotor = rotor
        return rotor
    
    def calcular_campo_magnetico_total(
        self,
        posicion_deg: float,
        distancia_m: float = 0.1,
    ) -> Tuple[float, float, float]:
        """
        Calcula el campo magnético total en el entrehierro.
        
        Parámetros:
            posicion_deg: posición angular del rotor
            distancia_m: distancia al entrehierra (radial)
        
        Retorna:
            (Br, Btheta, B_total) en Tesla
        """
        theta = np.radians(posicion_deg)
        
        # 1. Campo del rotor (permanente)
        Br_rotor = 0.0
        Btheta_rotor = 0.0
        
        for sector in self.rotor.sectores:
            # Simplificación: campo dipolar promedio por sector activo
            sector_activo = (
                sector.angulo_inicio_deg <= posicion_deg < sector.angulo_fin_deg
            )
            if sector_activo and sector.iman:
                iman = sector.iman[0]
                factor = iman.campo_residual_t * iman.area_m2 / (distancia_m ** 2)
                Br_rotor += factor * np.cos(theta)
                Btheta_rotor += factor * np.sin(theta)
        
        # 2. Campo del estator (inducido por corrientes)
        Br_estator = 0.0
        Btheta_estator = 0.0
        
        for bobina in self.estator.bobinas:
            # Determinar si la bobina está "activada"
            angulo_bobina = bobina.angulo_deg
            diferencia_angular = abs((posicion_deg - angulo_bobina + 180) % 360 - 180)
            
            # Campo más fuerte cuando rotor está cerca de la bobina
            factor_cercania = max(0, 1 - diferencia_angular / 60.0)
            
            # Campo de la bobina (simplificación)
            B_bobina = bobina.campo_magnetico_inducido_t(2.0) * factor_cercania
            
            # Contribución tangencial (genera torque)
            Btheta_estator += B_bobina * np.sin(np.radians(diferencia_angular))
            Br_estator += B_bobina * np.cos(np.radians(diferencia_angular))
        
        Br_total = Br_rotor + Br_estator
        Btheta_total = Btheta_rotor + Btheta_estator
        B_magnitud = np.sqrt(Br_total**2 + Btheta_total**2)
        
        return Br_total, Btheta_total, B_magnitud
    
    def calcular_torque(
        self,
        posicion_deg: float,
        corriente_bobinas: Optional[List[float]] = None,
    ) -> float:
        """
        Calcula el torque electromagnético en el rotor.
        
        τ = r × F = r × (B × I × L)
        """
        if corriente_bobinas is None:
            corriente_bobinas = [2.0] * len(self.estator.bobinas)
        
        _, Btheta, B_total = self.calcular_campo_magnetico_total(posicion_deg)
        
        # Parámetros geométricos
        r = self.rotor.radio_mm / 1000  # Radio en metros
        L = self.rotor.ancho_mm / 1000  # Longitud axial
        
        # Torque total (suma de contribuciones)
        torque_total = 0.0
        for i, bobina in enumerate(self.estator.bobinas):
            if i < len(corriente_bobinas):
                I = corriente_bobinas[i]
                # Torque de cada bobina: τ = r × B × I × L
                tau_bobina = r * B_total * I * L
                torque_total += tau_bobina
        
        return torque_total
    
    def paso_temporal(
        self,
        dt_s: float,
        torque_mecanico_nm: float = 0.0,
        corrientes: Optional[List[float]] = None,
    ) -> EstadoConmutacion:
        """
        Simula un paso temporal dt_s del motor.
        
        Parámetros:
            dt_s: paso de tiempo en segundos
            torque_mecanico_nm: torque externo aplicado (carga)
            corrientes: corrientes en cada bobina (A)
        
        Retorna estado del sistema en ese instante.
        """
        if corrientes is None:
            corrientes = [0.0] * len(self.estator.bobinas)
        
        # 1. Calcular campo magnético y torque
        Br, Btheta, B_total = self.calcular_campo_magnetico_total(self.posicion_deg)
        torque_electrico = self.calcular_torque(self.posicion_deg, corrientes)
        
        # 2. Ecuación de movimiento: τ_net = I × α
        torque_neto = torque_electrico - torque_mecanico_nm
        aceleracion = torque_neto / self.rotor.inercia_kgm2
        
        # 3. Integrar (método Euler)
        self.velocidad_rpm += aceleracion * dt_s * 60 / (2 * np.pi)  # rad/s² → RPM
        self.posicion_deg += self.velocidad_rpm * dt_s * 6  # RPM × dt → grados
        self.posicion_deg %= 360  # Mantener en [0, 360)
        
        # 4. Calcular voltaje inducido (Faraday)
        dPhi_dt = B_total * self.rotor.area_m2 * self.velocidad_rpm / 60
        voltaje = sum(
            bobina.voltaje_inducido_v(dPhi_dt) for bobina in self.estator.bobinas[:3]
        )
        
        # 5. Potencia generada
        potencia_gen = voltaje * sum(abs(c) for c in corrientes[:3])
        
        estado = EstadoConmutacion(
            tiempo_s=dt_s,
            posicion_rotor_deg=self.posicion_deg,
            velocidad_rpm=self.velocidad_rpm,
            corrientes_bobinas=corrientes,
            campos_bobinas_t=[b.campo_magnetico_inducido_t(c) for b, c in zip(self.estator.bobinas, corrientes)],
            campo_total_t=B_total,
            torque_nm=torque_electrico,
            voltaje_inducido_v=voltaje,
            potencia_generada_w=potencia_gen,
        )
        
        self.historial_estados.append(estado)
        return estado
    
    def simular_ventana(
        self,
        tiempo_s: float,
        dt_s: float = 0.001,
        carga_nm: float = 0.0,
        estrategia_conmutacion: Optional[str] = "simple",
    ) -> List[EstadoConmutacion]:
        """
        Simula una ventana de tiempo completa.
        
        Estrategias:
            "simple": conmutación básica cada 60°
            "optimizada": conmutación adelantada para torque
            "off": bobinas sin corriente (freewheeling)
        """
        n_pasos = int(tiempo_s / dt_s)
        resultados = []
        
        # Pre-generar secuencia de corrientes
        secuencias = self._generar_secuencias(n_pasos, estrategia_conmutacion)
        
        for paso in range(n_pasos):
            corrientes = secuencias[paso]
            estado = self.paso_temporal(dt_s=dt_s, torque_mecanico_nm=carga_nm, corrientes=corrientes)
            resultados.append(estado)
        
        return resultados
    
    def _generar_secuencias(
        self,
        n_pasos: int,
        estrategia: str,
    ) -> List[List[float]]:
        """Genera secuencias de corrientes según estrategia."""
        secuencias = []
        
        for paso in range(n_pasos):
            pos = self.posicion_deg + self.velocidad_rpm * paso * 0.001 * 6
            pos %= 360
            
            corrientes = [0.0] * len(self.estator.bobinas)
            
            if estrategia == "simple":
                # Conmutación cada 60° (3 fases)
                fase = int(pos / 60) % 3
                corrientes[fase * 4] = 3.0  # Activar bobina de fase
                corrientes[fase * 4 + 1] = 2.0
            
            elif estrategia == "optimizada":
                # Conmutación adelantada 15° para torque máximo
                pos_adelantado = (pos + 15) % 360
                fase = int(pos_adelantado / 60) % 3
                corrientes[fase * 4] = 4.0
                corrientes[fase * 4 + 2] = 1.5
            
            elif estrategia == "off":
                corrientes = [0.0] * len(self.estator.bobinas)
            
            secuencias.append(corrientes)
        
        return secuencias
    
    def analizar_desbalance(self) -> dict:
        """Análisis completo del desbalance magnético."""
        desbalance = self.rotor.desbalance_magnetico()
        torque_teorico = self.rotor.torque_teorico_nm()
        
        return {
            "desbalance_magnetico_am2": round(desbalance, 4),
            "torque_teorico_nm": round(torque_teorico, 4),
            "numero_imanes": self.rotor.numero_imanes(),
            "numero_sectores": len(self.rotor.sectores),
            "radio_rotor_mm": self.rotor.radio_mm,
            "evaluacion": self._evaluar_desbalance(desbalance),
        }
    
    def _evaluar_desbalance(self, desbalance: float) -> str:
        """Clasifica el desbalance."""
        if desbalance > 0.01:
            return "EXCELENTE - Alto torque asimétrico"
        elif desbalance > 0.005:
            return "BUENO - Desbalance moderado"
        elif desbalance > 0.001:
            return "REGULAR - Casi simétrico"
        else:
            return "DEFICIENTE - Prácticamente equilibrado (poco torque)"
