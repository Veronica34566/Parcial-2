from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from .schemas import VaccinationRecord, VaccinationList, ProvinceRecord
from .service import WorldBankService
from .utils import PROVINCES, deterministic_offset, clamp

app = FastAPI(
    title="API Vacunación Sarampión – Panamá (GET-only)",
    version="1.0.0",
    description=(
        "Consulta histórica del indicador SH.IMM.MEAS (% de niños 12–23 meses con vacuna contra sarampión) en Panamá.\n\n"
        "Fuente: Banco Mundial. Endpoints de solo lectura."
    ),
    openapi_tags=[
        {"name": "vacunas", "description": "Cobertura nacional de vacunación"},
        {"name": "provincias", "description": "Valores simulados por provincia/comarca"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

svc = WorldBankService()

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

@app.get("/vacunas", response_model=VaccinationList, tags=["vacunas"])  # GET /vacunas
def get_all():
    data = svc.all()
    return {"count": len(data), "data": data}

@app.get("/vacunas/{anio}", response_model=VaccinationRecord, tags=["vacunas"])  # GET /vacunas/2001
def get_by_year(anio: int):
    row = svc.by_year(anio)
    if not row:
        raise HTTPException(status_code=404, detail=f"No hay registro para el año {anio}.")
    return row

@app.get("/vacunas/provincia/{nombre}", response_model=ProvinceRecord, tags=["provincias"])  # opcional/simulado
def get_by_province(nombre: str, year: Optional[int] = None):
    # Normalizar nombre para comparación flexible
    nombre_norm = nombre.strip().lower()
    match = None
    for p in PROVINCES:
        if p.lower() == nombre_norm:
            match = p
            break
    if not match:
        raise HTTPException(status_code=404, detail="Provincia o comarca no reconocida.")

    # Elegir año
    target_year = year if year is not None else svc.latest_year()
    if target_year is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles.")

    national = svc.by_year(target_year)
    if not national:
        raise HTTPException(status_code=404, detail=f"No hay dato nacional para el año {target_year}.")

    base_val = national.get("value")
    if base_val is None:
        # Sin valor nacional => devolvemos None también
        return ProvinceRecord(
            province=match,
            year=target_year,
            value=None,
            simulated=True,
            base_country_value=None,
        )

    delta = deterministic_offset(match, target_year, spread=0.07) * 100  # puntos porcentuales
    prov_val = clamp(base_val + delta, 0.0, 100.0)

    return ProvinceRecord(
        province=match,
        year=target_year,
        value=prov_val,
        simulated=True,
        base_country_value=base_val,
    )
