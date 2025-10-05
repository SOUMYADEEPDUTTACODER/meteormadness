import math
from .usgs_data import get_elevation

def estimate_crater_size(diameter_km: float, velocity_kms: float, density=3000):
    """Estimate transient crater diameter in km"""
    D = diameter_km * 1000  # m
    v = velocity_kms * 1000  # m/s
    rho = density

    mass = (4/3) * math.pi * (D/2)**3 * rho
    energy = 0.5 * mass * v**2

    # Simplified scaling law for transient crater diameter
    crater_diameter_m = 1.8 * (energy**0.22)
    return crater_diameter_m / 1000  # km

def estimate_seismic_magnitude(energy_j: float) -> float:
    """Estimate seismic magnitude from impact energy (rough)"""
    logE = math.log10(energy_j)
    Mw = (logE - 4.8) / 1.5
    return Mw

def estimate_tsunami_height(diameter_km: float, velocity_kms: float, distance_km: float = 100):
    """Very rough initial tsunami height in meters"""
    D = diameter_km * 1000
    v = velocity_kms * 1000
    mass = (4/3) * math.pi * (D/2)**3 * 3000
    energy = 0.5 * mass * v**2

    h0 = (energy**0.25) / 1e5
    h_at_distance = h0 / math.sqrt(distance_km)
    return h_at_distance

def get_local_elevation(lat: float, lon: float, source="auto") -> float:
    """Wrapper to fetch elevation from USGS/SRTM/GEBCO"""
    return get_elevation(lat, lon, source)
