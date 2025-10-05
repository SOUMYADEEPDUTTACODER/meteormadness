# backend/app.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from pathlib import Path
import traceback

# Import your existing logic
from backend.api.nasa_api import fetch_neo_by_id
from backend.api.nasa_api import fetch_neo_by_id, extract_key_fields
from backend.data.dem_loader import get_local_elevation
from backend.main import run_simulation

app = FastAPI(title="Meteor Defender Simulation API", version="0.2")

# Allow local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Models
# -------------------------
class OrbitalElements(BaseModel):
    epoch_jd: float
    semi_major_axis_AU: float
    eccentricity: float
    inclination_deg: float
    raan_deg: float
    argp_deg: float
    true_anomaly_deg: float
    heliocentric_current: dict
    heliocentric_future: dict

class EnergyInfo(BaseModel):
    joules: float
    megatons_tnt: float
    risk_text: str

class AtmosphericChanges(BaseModel):
    temperature_rise_C: float
    pressure_wave_hPa: float
    wind_speed_kmh: float

class Consequences(BaseModel):
    impact_location: dict
    crater_km: float
    seismic_mw: float
    tsunami_m_at_200km: float
    atmospheric_changes: AtmosphericChanges

class AsteroidInfo(BaseModel):
    id: str
    name: str
    diameter_km: float
    velocity_kps_sample: float
    approach_date: str
    miss_distance_km_sample: Optional[float]

class SimulateRequest(BaseModel):
    asteroid_id: str = Field(..., description="NASA NEO SPK-ID or asteroid id")
    impact_lat: float = Field(..., description="Impact latitude in degrees")
    impact_lon: float = Field(..., description="Impact longitude in degrees")
    dem_source: Optional[str] = Field("auto", description="DEM source: auto/usgs/srtm/gebco")
    propagate_days: Optional[int] = Field(30, ge=0, description="Days to propagate the orbit forward")

class SimulateResponse(BaseModel):
    result_path: Optional[str]
    timestamp_utc: str
    asteroid: AsteroidInfo
    orbit: OrbitalElements
    energy: EnergyInfo
    consequences: Consequences

# -------------------------
# Health
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok", "app": "Meteor Defender Backend"}

# -------------------------
# NEO endpoints
# -------------------------
@app.get("/api/neo/{asteroid_id}")
def neo_lookup(asteroid_id: str):
    try:
        return fetch_neo_by_id(asteroid_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NEO lookup failed: {e}")

@app.get("/api/neo/browse")
def neo_browse(page: int = Query(0, ge=0), page_size: int = Query(20, ge=1, le=50)):
    try:
        if 'nasa_browse_neos' in globals() and callable(nasa_browse_neos):
            return nasa_browse_neos(page=page, page_size=page_size)
        else:
            raise RuntimeError("browse_neos helper not implemented in backend.api.nasa_api")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NEO browse failed: {e}")

# -------------------------
# DEM / Elevation endpoint
# -------------------------
@app.get("/api/elevation")
def elevation(lat: float = Query(...), lon: float = Query(...), source: Optional[str] = Query("auto")):
    try:
        elev = get_local_elevation(lat, lon)
        return {"lat": lat, "lon": lon, "elevation_m": elev}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No DEM found for {lat},{lon}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elevation lookup failed: {e}")

# -------------------------
# Simulation endpoint
# -------------------------
@app.post("/api/simulate", response_model=SimulateResponse)
def simulate(req: SimulateRequest):
    try:
        out = run_simulation(
            asteroid_id=req.asteroid_id,
            impact_lat=req.impact_lat,
            impact_lon=req.impact_lon,
            dem_source=req.dem_source,
            propagate_days=req.propagate_days,
        )

        out_file = Path(__file__).resolve().parents[1] / "data" / "simulation_result.json"
        out_path = str(out_file) if out_file.exists() else None

        return {"result_path": out_path, **out}
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail={"error": str(e), "trace": tb})

# -------------------------
# Static helper: list available USGS tiles
# -------------------------
@app.get("/api/usgs/tiles")
def list_usgs_tiles():
    try:
        tiles = []
        p = Path(__file__).resolve().parents[1] / "data" / "usgs"
        if p.exists():
            tiles = [t.name for t in p.glob("*.tif")]
        return {"count": len(tiles), "tiles": tiles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not list tiles: {e}")
