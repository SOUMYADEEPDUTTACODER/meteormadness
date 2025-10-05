import rasterio
from pathlib import Path

# -------------------------------
# Paths to DEM folders
# -------------------------------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"

USGS_DIR = DATA_DIR / "usgs"   # contains multiple .tif tiles
SRTM_DEM = DATA_DIR / "srtm" / "srtm_sample.tif"
GEBCO_DEM = DATA_DIR / "gebco" / "gebco_sample.tif"


def _read_raster(filepath: Path, lat: float, lon: float) -> float:
    """Helper: read raster value at lat/lon from a single GeoTIFF"""
    with rasterio.open(filepath) as src:
        try:
            row, col = src.index(lon, lat)
            val = src.read(1)[row, col]
            if val == src.nodata:
                raise ValueError(f"No data at {lat},{lon} in {filepath.name}")
            return float(val)
        except IndexError:
            # Point is outside raster extent
            raise ValueError(f"Point outside raster {filepath.name}")


def _search_usgs(lat: float, lon: float) -> float:
    """Try all USGS tiles until one contains the point"""
    if not USGS_DIR.exists():
        raise FileNotFoundError("USGS DEM directory not found.")

    for tif in USGS_DIR.glob("*.tif"):
        try:
            return _read_raster(tif, lat, lon)
        except Exception:
            continue
    raise FileNotFoundError(f"No USGS DEM covers location {lat}, {lon}")


def get_elevation(lat: float, lon: float, source: str = "auto") -> float:
    """
    Return elevation (m) at a given lat/lon.

    source:
        "auto" -> USGS if U.S., else SRTM/GEBCO fallback
        "USGS" -> USGS DEM
        "SRTM" -> NASA SRTM DEM
        "GEBCO" -> GEBCO bathymetry
    """
    source = source.lower()

    # Auto mode
    if source == "auto":
        # Try USGS if in continental U.S.
        if 24 <= lat <= 50 and -125 <= lon <= -66:
            try:
                return _search_usgs(lat, lon)
            except Exception:
                pass

        # Try SRTM for land
        if SRTM_DEM.exists():
            try:
                return _read_raster(SRTM_DEM, lat, lon)
            except Exception:
                pass

        # Fallback to GEBCO
        if GEBCO_DEM.exists():
            try:
                return _read_raster(GEBCO_DEM, lat, lon)
            except Exception:
                pass

        raise FileNotFoundError(f"No DEM available for {lat}, {lon}")

    # Forced sources
    elif source == "usgs":
        return _search_usgs(lat, lon)
    elif source == "srtm":
        return _read_raster(SRTM_DEM, lat, lon)
    elif source == "gebco":
        return _read_raster(GEBCO_DEM, lat, lon)
    else:
        raise ValueError(f"Unknown DEM source: {source}")
