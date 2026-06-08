"""
API REST para gestión de nodos PIRS-1

Arquitectura:
    - FastAPI para endpoints
    - SQLite/JSON para persistencia ligera
    - Estructura preparada para MQTT + LoRa en producción
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import json
import os

# Inicializar aplicación FastAPI
app = FastAPI(
    title="PIRS-1 API",
    description="Programa Integrado de Regeneración del Sahel - API de Nodos Territoriales",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# === MODELOS PYDANTIC ===

class Coordenadas(BaseModel):
    lat: float = Field(..., ge=10.0, le=25.0, description="Latitud Mali (10°N - 25°N)")
    lon: float = Field(..., ge=-12.0, le=4.0, description="Longitud Mali (12°W - 4°E)")
    region: str = Field(..., description="Región administrativa de Mali")

class ConfiguracionAgua(BaseModel):
    capacidad_cisterna_m3: float = Field(default=50.0, ge=10.0, le=500.0)
    area_fog_m2: float = Field(default=25.0, ge=5.0, le=200.0)
    area_condensacion_m2: float = Field(default=10.0, ge=1.0, le=50.0)
    rendimiento_fog_l_m2_dia: float = Field(default=5.0, ge=0.5, le=20.0)

class ConfiguracionEnergia(BaseModel):
    panel_solar_w: float = Field(default=300.0, ge=0.0)
    microeolica_w: float = Field(default=0.0, ge=0.0)
    bateria_lfp_kwh: float = Field(default=1.0, ge=0.0)

class NodoCreate(BaseModel):
    id_nodo: str = Field(..., pattern=r"^PIRS-\d{3}$", description="ID formato PIRS-001")
    coordenadas: Coordenadas
    superficie_ha: float = Field(default=1.0, ge=0.25, le=10.0)
    fase: int = Field(default=1, ge=1, le=4)
    agua: Optional[ConfiguracionAgua] = None
    energia: Optional[ConfiguracionEnergia] = None

class NodoUpdate(BaseModel):
    fase: Optional[int] = None
    humedad_suelo_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    estado: Optional[str] = None
    biochar_aplicado_kg_m2: Optional[float] = Field(None, ge=0.0)
    nopal_plantas: Optional[int] = Field(None, ge=0)
    arboles_plantados: Optional[int] = Field(None, ge=0)
    panel_solar_w: Optional[float] = Field(None, ge=0.0)
    bateria_lfp_kwh: Optional[float] = Field(None, ge=0.0)

class MedicionCreate(BaseModel):
    nodo_id: str
    timestamp: Optional[datetime] = None
    humedad_suelo: float = Field(..., ge=0.0, le=100.0)
    temperatura_aire: float = Field(..., ge=-10.0, le=60.0)
    viento_ms: float = Field(..., ge=0.0, le=50.0)
    agua_litros_captada: float = Field(..., ge=0.0)
    energia_kwh_generada: float = Field(..., ge=0.0)
    agua_litros_consumida: float = Field(..., ge=0.0)

class MetricasNodo(BaseModel):
    nodo_id: str
    humedad_suelo_actual_pct: float
    capacidad_campo_pct: float
    porcentaje_capacidad: float
    cisterna_litros_actuales: float
    captacion_anual_l: float
    estado_hidrico: str
    co2_secuestrado_kg: float
    productividad_kg_ha: float

# === BASE DE DATOS SIMPLIFICADA (JSON) ===

DATA_DIR = os.environ.get("PIRS1_DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "data"))
NODOS_FILE = os.path.join(DATA_DIR, "nodos.json")
MEDICIONES_FILE = os.path.join(DATA_DIR, "mediciones.json")


def _asegurar_datos():
    """Crea archivos JSON si no existen."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for f in [NODOS_FILE, MEDICIONES_FILE]:
        if not os.path.exists(f):
            with open(f, "w", encoding="utf-8") as fh:
                json.dump({}, fh)


def _leer_nodos() -> Dict[str, Any]:
    _asegurar_datos()
    with open(NODOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _guardar_nodos(nodos: Dict[str, Any]):
    with open(NODOS_FILE, "w", encoding="utf-8") as f:
        json.dump(nodos, f, indent=2, ensure_ascii=False)


def _leer_mediciones() -> Dict[str, Any]:
    _asegurar_datos()
    with open(MEDICIONES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _guardar_mediciones(mediciones: Dict[str, Any]):
    with open(MEDICIONES_FILE, "w", encoding="utf-8") as f:
        json.dump(mediciones, f, indent=2, ensure_ascii=False)


# === ENDPOINTS ===

@app.get("/", tags=["Sistema"])
def raiz():
    """Endpoint de salud del servicio."""
    return {
        "sistema": "PIRS-1 API",
        "version": "1.0.0",
        "descripcion": "Programa Integrado de Regeneración del Sahel",
        "autor": "Yago Otero - Naira Studio LTD",
        "endpoints": ["/nodos", "/mediciones", "/simulacion"]
    }


@app.post("/nodos", response_model=Dict[str, Any], tags=["Nodos"])
def crear_nodo(nodo: NodoCreate):
    """
    Registra un nuevo nodo de regeneración territorial.
    
    Formato ID: PIRS-001, PIRS-002, etc.
    Coordenadas: lat 10-25°N, lon 12°W-4°E (Mali)
    """
    nodos = _leer_nodos()
    
    if nodo.id_nodo in nodos:
        raise HTTPException(status_code=400, detail=f"Nodo {nodo.id_nodo} ya existe")
    
    datos_nodo = {
        "id_nodo": nodo.id_nodo,
        "coordenadas": {
            "lat": nodo.coordenadas.lat,
            "lon": nodo.coordenadas.lon,
            "region": nodo.coordenadas.region,
        },
        "superficie_ha": nodo.superficie_ha,
        "fase": nodo.fase,
        "estado": "planificado",
        "fecha_creacion": str(date.today()),
        "agua": (nodo.agua.dict() if nodo.agua else {
            "capacidad_cisterna_m3": 50.0,
            "area_fog_m2": 25.0,
            "area_condensacion_m2": 10.0,
            "rendimiento_fog_l_m2_dia": 5.0,
        }),
        "energia": (nodo.energia.dict() if nodo.energia else {
            "panel_solar_w": 300.0,
            "microeolica_w": 0.0,
            "bateria_lfp_kwh": 1.0,
        }),
        "metricas": {
            "humedad_suelo_pct": 5.0,
            "captacion_anual_l": 0,
            "estado_hidrico": "sin_datos",
        }
    }
    
    nodos[nodo.id_nodo] = datos_nodo
    _guardar_nodos(nodos)
    
    return {
        "mensaje": f"Nodo {nodo.id_nodo} creado exitosamente",
        "nodo": datos_nodo,
        "siguiente": f"Agregar mediciones: POST /mediciones con nodo_id={nodo.id_nodo}"
    }


@app.get("/nodos", response_model=Dict[str, Any], tags=["Nodos"])
def listar_nodos(region: Optional[str] = None, fase: Optional[int] = None, estado: Optional[str] = None):
    """Lista todos los nodos con filtros opcionales."""
    nodos = _leer_nodos()
    
    resultado = {}
    for nid, nodo in nodos.items():
        if region and nodo.get("coordenadas", {}).get("region") != region:
            continue
        if fase and nodo.get("fase") != fase:
            continue
        if estado and nodo.get("estado") != estado:
            continue
        resultado[nid] = nodo
    
    return {
        "total": len(resultado),
        "filtros": {"region": region, "fase": fase, "estado": estado},
        "nodos": resultado
    }


@app.get("/nodos/{nodo_id}", tags=["Nodos"])
def obtener_nodo(nodo_id: str):
    """Obtiene detalle completo de un nodo específico."""
    nodos = _leer_nodos()
    
    if nodo_id not in nodos:
        raise HTTPException(status_code=404, detail=f"Nodo {nodo_id} no encontrado")
    
    return nodos[nodo_id]


@app.patch("/nodos/{nodo_id}", tags=["Nodos"])
def actualizar_nodo(nodo_id: str, actualizacion: NodoUpdate):
    """
    Actualiza campos de un nodo existente.
    
    Solo actualiza los campos proporcionados en el body (PATCH parcial).
    """
    nodos = _leer_nodos()
    
    if nodo_id not in nodos:
        raise HTTPException(status_code=404, detail=f"Nodo {nodo_id} no encontrado")
    
    nodo = nodos[nodo_id]
    datos_update = actualizacion.dict(exclude_unset=True)
    
    # Mapeo de campos
    if "fase" in datos_update:
        nodo["fase"] = datos_update["fase"]
    if "estado" in datos_update:
        nodo["estado"] = datos_update["estado"]
    
    # Actualizar métricas si se envían
    metricas = nodo.get("metricas", {})
    if "humedad_suelo_pct" in datos_update:
        metricas["humedad_suelo_pct"] = datos_update["humedad_suelo_pct"]
    if datos_update.get("panel_solar_w"):
        nodo.setdefault("energia", {})["panel_solar_w"] = datos_update["panel_solar_w"]
    if datos_update.get("bateria_lfp_kwh"):
        nodo.setdefault("energia", {})["bateria_lfp_kwh"] = datos_update["bateria_lfp_kwh"]
    if "biochar_aplicado_kg_m2" in datos_update:
        metricas["biochar_aplicado"] = datos_update["biochar_aplicado_kg_m2"]
    if "nopal_plantas" in datos_update:
        nodo.setdefault("cultivos", {})["nopal"] = datos_update["nopal_plantas"]
    if "arboles_plantados" in datos_update:
        nodo.setdefault("cultivos", {})["arboles"] = datos_update["arboles_plantados"]
    
    nodo["metricas"] = metricas
    nodo["fecha_actualizacion"] = str(date.today())
    
    nodos[nodo_id] = nodo
    _guardar_nodos(nodos)
    
    return {
        "mensaje": f"Nodo {nodo_id} actualizado",
        "campos_actualizados": list(datos_update.keys()),
        "nodo": nodo
    }


@app.post("/mediciones", tags=["Telemetría"])
def registrar_medicion(medicion: MedicionCreate):
    """
    Registra una nueva medición de sensores para un nodo.
    
    Campos:
        - nodo_id: ID del nodo (PIRS-XXX)
        - timestamp: Momento de la medición (opcional, default: now)
        - humedad_suelo: % humedad del suelo (0-100)
        - temperatura_aire: °C
        - viento_ms: velocidad del viento en m/s
        - agua_litros_captada: L capturados del aire
        - energia_kwh_generada: kWh generados por solar
        - agua_litros_consumida: L usados
    
    Simula estructura MQTT: topics/pirs1/nodos/{id}/mediciones
    """
    nodos = _leer_nodos()
    
    if medicion.nodo_id not in nodos:
        raise HTTPException(status_code=404, detail=f"Nodo {medicion.nodo_id} no existe")
    
    mediciones = _leer_mediciones()
    
    timestamp = medicion.timestamp or datetime.now()
    
    registro = {
        "nodo_id": medicion.nodo_id,
        "timestamp": timestamp.isoformat(),
        "humedad_suelo": medicion.humedad_suelo,
        "temperatura_aire": medicion.temperatura_aire,
        "viento_ms": medicion.viento_ms,
        "agua_captada_l": medicion.agua_litros_captada,
        "energia_kwh": medicion.energia_kwh_generada,
        "agua_consumida_l": medicion.agua_litros_consumida,
    }
    
    # Estructura: mediciones[nodo_id] = [lista de registros]
    if medicion.nodo_id not in mediciones:
        mediciones[medicion.nodo_id] = []
    mediciones[medicion.nodo_id].append(registro)
    
    # Mantener solo últimos 1000 registros por nodo
    mediciones[medicion.nodo_id] = mediciones[medicion.nodo_id][-1000:]
    
    _guardar_mediciones(mediciones)
    
    # Actualizar métricas del nodo
    nodo = nodos[medicion.nodo_id]
    metricas = nodo.get("metricas", {})
    metricas["humedad_suelo_pct"] = medicion.humedad_suelo
    metricas["ultima_medicion"] = timestamp.isoformat()
    nodo["metricas"] = metricas
    nodos[medicion.nodo_id] = nodo
    _guardar_nodos(nodos)
    
    return {
        "mensaje": "Medición registrada",
        "registro": registro,
        "topic_mqtt": f"pirs1/nodos/{medicion.nodo_id}/mediciones"
    }


@app.get("/mediciones/{nodo_id}", tags=["Telemetría"])
def obtener_mediciones(nodo_id: str, ultimas: int = 100):
    """Obtiene las últimas N mediciones de un nodo."""
    mediciones = _leer_mediciones()
    
    if nodo_id not in mediciones:
        raise HTTPException(status_code=404, detail=f"No hay mediciones para {nodo_id}")
    
    datos = mediciones[nodo_id][-ultimas:]
    
    return {
        "nodo_id": nodo_id,
        "total_registros": len(mediciones[nodo_id]),
        "registros_enviados": len(datos),
        "mediciones": datos
    }


@app.get("/nodos/{nodo_id}/estado", response_model=MetricasNodo, tags=["Telemetría"])
def estado_nodo(nodo_id: str):
    """
    Retorna métricas en tiempo real del estado del nodo.
    
    Equivale al dashboard del operador en campo.
    """
    nodos = _leer_nodos()
    
    if nodo_id not in nodos:
        raise HTTPException(status_code=404, detail=f"Nodo {nodo_id} no encontrado")
    
    nodo = nodos[nodo_id]
    metricas = nodo.get("metricas", {})
    
    return MetricasNodo(
        nodo_id=nodo_id,
        humedad_suelo_actual_pct=metricas.get("humedad_suelo_pct", 0.0),
        capacidad_campo_pct=25.0,
        porcentaje_capacidad=round(metricas.get("humedad_suelo_pct", 0.0) / 25.0 * 100, 0),
        cisterna_litros_actuales=metricas.get("cisterna_litros", 0.0),
        captacion_anual_l=metricas.get("captacion_anual_l", 0),
        estado_hidrico=metricas.get("estado_hidrico", "sin_datos"),
        co2_secuestrado_kg=metricas.get("co2_secuestrado_kg", 0.0),
        productividad_kg_ha=metricas.get("productividad_kg_ha", 0.0),
    )


@app.post("/simulacion/hidrica", tags=["Simulación"])
def simular_hidrico(nodo_id: str, años: int = 5):
    """
    Ejecuta simulación hídrica multi-anual para un nodo existente.
    
    Integra con el motor de simulación para proyectar comportamiento futuro.
    """
    from src.simulacion.simulador_hidrico import (
        ParametrosClimaticos,
        ParametrosSuelo,
        ParametrosCaptacion,
        ParametrosVegetacion,
        SimuladorHidricoPIRS1,
    )
    
    nodos = _leer_nodos()
    if nodo_id not in nodos:
        raise HTTPException(status_code=404, detail=f"Nodo {nodo_id} no encontrado")
    
    nodo = nodos[nodo_id]
    agua_cfg = nodo.get("agua", {})
    
    # Configurar parámetros desde el nodo
    clima = ParametrosClimaticos(
        precipitacion_media_anual_mm=300.0,
        radiacion_solar_kwh_m2_dia=6.0,
        viento_velocidad_media_ms=5.0,
    )
    suelo = ParametrosSuelo()
    captacion = ParametrosCaptacion(
        area_fog_m2=agua_cfg.get("area_fog_m2", 25.0),
        rendimiento_fog_l_m2_dia=agua_cfg.get("rendimiento_fog_l_m2_dia", 5.0),
    )
    vegetacion = ParametrosVegetacion()
    
    simulador = SimuladorHidricoPIRS1(
        clima=clima,
        suelo=suelo,
        captacion=captacion,
        vegetacion=vegetacion,
        capacidad_cisterna_l=agua_cfg.get("capacidad_cisterna_m3", 50.0) * 1000,
    )
    
    resultados = simulador.simular_multianual(años=años)
    
    return {
        "nodo_id": nodo_id,
        "parametros_simulacion": {
            "años_simulados": años,
            "precipitacion_media_mm_año": clima.precipitacion_media_anual_mm,
            "area_fog_m2": captacion.area_fog_m2,
            "capacidad_cisterna_m3": agua_cfg.get("capacidad_cisterna_m3", 50.0),
        },
        "resumen_por_año": [simulador.resumen_anual(año=a) for a in range(1, años + 1)],
        "detalle_mensual_primer_año": resultados[:12],
    }


@app.get("/dashboard/resumen", tags=["Dashboard"])
def dashboard_resumen():
    """
    Dashboard consolidado del estado del proyecto.
    
    Agrega métricas de todos los nodos para visión ejecutiva.
    """
    nodos = _leer_nodos()
    mediciones = _leer_mediciones()
    
    resumen_nodos = []
    for nid, nodo in nodos.items():
        metricas = nodo.get("metricas", {})
        coords = nodo.get("coordenadas", {})
        agua = nodo.get("agua", {})
        energia = nodo.get("energia", {})
        
        resumen_nodos.append({
            "id": nid,
            "region": coords.get("region", "N/A"),
            "lat": coords.get("lat"),
            "lon": coords.get("lon"),
            "fase": nodo.get("fase"),
            "estado": nodo.get("estado"),
            "humedad_suelo_pct": metricas.get("humedad_suelo_pct"),
            "capacidad_cisterna_m3": agua.get("capacidad_cisterna_m3"),
            "energia_solar_w": energia.get("panel_solar_w"),
        })
    
    total_mediciones = sum(len(v) for v in mediciones.values())
    
    return {
        "proyecto": "PIRS-1",
        "descripcion": "Programa Integrado de Regeneración del Sahel",
        "fecha_consulta": str(date.today()),
        "total_nodos": len(nodos),
        "total_mediciones": total_mediciones,
        "nodos_por_fase": {
            1: sum(1 for n in resumen_nodos if n["fase"] == 1),
            2: sum(1 for n in resumen_nodos if n["fase"] == 2),
            3: sum(1 for n in resumen_nodos if n["fase"] == 3),
            4: sum(1 for n in resumen_nodos if n["fase"] == 4),
        },
        "nodos": resumen_nodos,
    }


# === PUNTO DE ENTRADA ===

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("PIRS-1 API - Programa Integrado de Regeneración del Sahel")
    print("=" * 60)
    print("Autor: Yago Otero - Naira Studio LTD")
    print("Docs: http://127.0.0.1:8000/docs")
    print("Redoc: http://127.0.0.1:8000/redoc")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "api_nodos:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
