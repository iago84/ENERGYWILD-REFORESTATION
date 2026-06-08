#!/usr/bin/env python3
"""
NEXUS RISING — Dataset Preparation for ML Training
====================================================

Utilities for generating, validating, and exporting ML-ready datasets
for the BSLC Magnetic Generator optimization system.

Status: CONCEPTUAL ONLY — synthetic data for pipeline testing.
"""

import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from pathlib import Path
import random

# ============================================================
# DATA SCHEMAS
# ============================================================

@dataclass
class MagnetConfig:
    """Configuration of a single permanent magnet."""
    radio_mm: float = 40.0
    altura_mm: float = 10.0
    material: str = "N52"
    campo_residual_t: float = 1.4
    polaridad_ns: str = "N-S"
    angulo_ini_deg: float = 0.0
    angulo_fin_deg: float = 120.0


@dataclass
class SectorRotor:
    """Rotational sector with one or more magnets."""
    angulo_inicio_deg: float
    angulo_fin_deg: float
    imanes: List[MagnetConfig] = field(default_factory=list)
    nombre: str = ""


@dataclass
class ConfigRotor:
    """Complete rotor configuration."""
    radio_mm: float = 50.0
    ancho_mm: float = 20.0
    sectores: List[SectorRotor] = field(default_factory=list)


@dataclass
class ConfigBobina:
    """Stator coil configuration."""
    vueltas: int = 500
    seccion_mm2: float = 1.0
    resistencia_ohm: float = 5.0
    corriente_max_a: float = 3.0
    posicion_deg: float = 0.0


@dataclass
class ConfigEstator:
    """Complete stator configuration."""
    radio_mm: float = 60.0
    num_bobinas: int = 12
    bobinas: List[ConfigBobina] = field(default_factory=list)


@dataclass
class SampleBSLC:
    """Single ML sample: config + targets + metadata."""
    sample_id: str
    configuracion: Dict
    targets: Dict
    metadata: Dict = field(default_factory=dict)
    validacion: Dict = field(default_factory=dict)


# ============================================================
# SYNTHETIC DATA GENERATOR (PIPELINE TESTING ONLY)
# ============================================================

class SyntheticDataGenerator:
    """
    Generate synthetic BSLC samples for ML pipeline testing.
    
    WARNING: Labels are PLACEHOLDER synthetic values, NOT physical predictions.
    Use ONLY for testing data pipelines, preprocessing, and model skeletons.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)

    def generar_configuracion_aleatoria(self) -> Dict:
        """Generate a random valid BSLC configuration."""
        num_sectores = random.choice([2, 3, 4, 5, 6])
        angulo_paso = 360.0 / num_sectores
        
        sectores = []
        for i in range(num_sectores):
            num_imanes = random.randint(1, 3)
            imanes = []
            for j in range(num_imanes):
                iman = MagnetConfig(
                    radio_mm=random.uniform(20, 50),
                    altura_mm=random.uniform(5, 15),
                    material=random.choice(["N52", "N42", "N35"]),
                    campo_residual_t=random.uniform(1.2, 1.5),
                    polaridad_ns=random.choice(["N-S", "S-N"]),
                    angulo_ini_deg=i * angulo_paso,
                    angulo_fin_deg=(i + 1) * angulo_paso,
                )
                imanes.append(iman)
            
            sector = SectorRotor(
                angulo_inicio_deg=i * angulo_paso,
                angulo_fin_deg=(i + 1) * angulo_paso,
                imanes=imanes,
                nombre=f"Sector_{i+1}",
            )
            sectores.append(sector)
        
        rotor = ConfigRotor(
            radio_mm=random.uniform(40, 80),
            ancho_mm=random.uniform(10, 40),
            sectores=sectores,
        )
        
        num_bobinas = random.choice([3, 6, 9, 12])
        bobinas = []
        for i in range(num_bobinas):
            bobina = ConfigBobina(
                vueltas=random.randint(200, 1000),
                seccion_mm2=random.uniform(0.5, 2.0),
                resistencia_ohm=random.uniform(2, 10),
                corriente_max_a=random.uniform(1, 5),
                posicion_deg=i * (360 / num_bobinas),
            )
            bobinas.append(bobina)
        
        estator = ConfigEstator(
            radio_mm=random.uniform(50, 80),
            num_bobinas=num_bobinas,
            bobinas=bobinas,
        )
        
        return {
            "rotor": asdict(rotor),
            "estator": asdict(estator),
        }

    def generar_targets_sinteticos(self, config: Dict) -> Dict:
        """
        Generate PLACEHOLDER targets from configuration.
        
        WARNING: These are NOT physical predictions.
        They are synthetic values for ML pipeline testing only.
        """
        num_sectores = len(config["rotor"]["sectores"])
        radio_rotor = config["rotor"]["radio_mm"]
        num_bobinas = config["estator"]["num_bobinas"]
        
        # Synthetic (NOT physical) relationships
        desbalance = random.uniform(0.001, 0.1) * (num_sectores / 3)
        torque = random.uniform(0.001, 0.05) * (num_bobinas / 12)
        coste = random.uniform(50, 300)
        eficiencia = random.uniform(0.1, 0.9)
        viabilidad = random.choice(["ALTA", "MEDIA", "BAJA", "IMPOSIBLE"])
        
        return {
            "desbalance_magnetico_am2": round(desbalance, 6),
            "torque_teorico_nm": round(torque, 6),
            "torque_arranque_nm": round(torque * 0.3, 6),
            "eficiencia_material": round(eficiencia, 4),
            "coste_imanes_eur": round(coste, 2),
            "velocidad_critica_rpm": round(random.uniform(100, 500), 1),
            "consumo_estimado_w": round(random.uniform(5, 50), 1),
            "viabilidad": viabilidad,
        }

    def generar_sample(self, sample_id: str) -> SampleBSLC:
        """Generate one complete ML sample."""
        config = self.generar_configuracion_aleatoria()
        targets = self.generar_targets_sinteticos(config)
        
        return SampleBSLC(
            sample_id=sample_id,
            configuracion=config,
            targets=targets,
            metadata={"fuente": "sintetico_pipeline", "version": "0.1"},
            validacion={"confianza": 0.0, "checks": ["sintetico"]},
        )

    def generar_dataset(self, n_samples: int = 100) -> List[SampleBSLC]:
        """Generate a complete dataset of n_samples."""
        samples = []
        for i in range(n_samples):
            sample_id = f"BSLC-SYN-{i+1:04d}"
            sample = self.generar_sample(sample_id)
            samples.append(sample)
        return samples


# ============================================================
# DATASET EXPORTERS
# ============================================================

class DatasetExporter:
    """Export datasets to various ML formats."""

    @staticmethod
    def to_jsonl(samples: List[SampleBSLC], ruta: str):
        """Export to JSONL format (one JSON per line)."""
        path = Path(ruta)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            for sample in samples:
                f.write(json.dumps(asdict(sample), ensure_ascii=False) + "\n")
        
        print(f"Dataset exportado a JSONL: {path} ({len(samples)} samples)")

    @staticmethod
    def to_json(samples: List[SampleBSLC], ruta: str):
        """Export to single JSON file."""
        path = Path(ruta)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "dataset_id": hashlib.md5(str(len(samples)).encode()).hexdigest()[:8],
            "num_samples": len(samples),
            "samples": [asdict(s) for s in samples],
        }
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Dataset exportado a JSON: {path} ({len(samples)} samples)")

    @staticmethod
    def to_csv_features_targets(samples: List[SampleBSLC], ruta_features: str, ruta_targets: str):
        """Export flattened features and targets to CSV."""
        import csv
        
        # Flatten features
        rows_f = []
        rows_t = []
        
        for s in samples:
            # Features (configuracion)
            row_f = {
                "sample_id": s.sample_id,
                "num_sectores": len(s.configuracion["rotor"]["sectores"]),
                "radio_rotor_mm": s.configuracion["rotor"]["radio_mm"],
                "ancho_rotor_mm": s.configuracion["rotor"]["ancho_mm"],
                "num_bobinas": s.configuracion["estator"]["num_bobinas"],
            }
            rows_f.append(row_f)
            
            # Targets
            row_t = {"sample_id": s.sample_id}
            row_t.update(s.targets)
            rows_t.append(row_t)
        
        # Write CSV
        for rows, path in [(rows_f, ruta_features), (rows_t, ruta_targets)]:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            print(f"CSV exportado: {p}")


# ============================================================
# VALIDATION UTILITIES
# ============================================================

class DatasetValidator:
    """Validate dataset integrity for ML training."""

    @staticmethod
    def validar_schema(sample: SampleBSLC) -> Dict:
        """Validate a single sample against expected schema."""
        errores = []
        
        # Check required fields
        if not sample.sample_id:
            errores.append("sample_id vacío")
        
        if "rotor" not in sample.configuracion:
            errores.append("falta configuracion.rotor")
        
        if "estator" not in sample.configuracion:
            errores.append("falta configuracion.estator")
        
        if not sample.targets:
            errores.append("targets vacíos")
        
        # Check targets
        required_targets = [
            "desbalance_magnetico_am2",
            "torque_teorico_nm",
            "eficiencia_material",
            "viabilidad",
        ]
        for t in required_targets:
            if t not in sample.targets:
                errores.append(f"falta target: {t}")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
        }

    @staticmethod
    def validar_dataset(samples: List[SampleBSLC]) -> Dict:
        """Validate entire dataset."""
        resultados = [DatasetValidator.validar_schema(s) for s in samples]
        
        invalidos = [i for i, r in enumerate(resultados) if not r["valido"]]
        
        return {
            "total_samples": len(samples),
            "validos": len(samples) - len(invalidos),
            "invalidos": len(invalidos),
            "indices_invalidos": invalidos[:10],  # Primeros 10
            "porcentaje_validez": (len(samples) - len(invalidos)) / max(1, len(samples)) * 100,
        }


# ============================================================
# CLI / MAIN
# ============================================================

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("NEXUS RISING — Dataset Preparation")
    print("=" * 60)
    
    # Generar dataset sintético
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    print(f"\nGenerando {n} muestras sintéticas...")
    
    gen = SyntheticDataGenerator(seed=42)
    samples = gen.generar_dataset(n_samples=n)
    
    # Validar
    print("\nValidando dataset...")
    val = DatasetValidator.validar_dataset(samples)
    print(f"  Válidos: {val['validos']}/{val['total_samples']} ({val['porcentaje_validez']:.1f}%)")
    
    if val["invalidos"] > 0:
        print(f"  ⚠️  Muestras inválidas: {val['indices_invalidos']}")
    
    # Exportar
    base = "01-energia/generador-bslc/data"
    DatasetExporter.to_json(samples, f"{base}/dataset_sintetico.json")
    DatasetExporter.to_jsonl(samples, f"{base}/dataset_sintetico.jsonl")
    DatasetExporter.to_csv_features_targets(
        samples,
        f"{base}/features.csv",
        f"{base}/targets.csv",
    )
    
    print("\n✅ Dataset listo para ML pipeline.")
