import math

def estimate_mass(diameter_km: float, density: float = 3000.0) -> float:
    """
    Estimate mass of asteroid assuming spherical body.
    
    Parameters:
        diameter_km: Diameter in kilometers
        density: Average density in kg/m³ (default ~3000, typical for stony asteroid)
    
    Returns:
        Mass in kilograms
    """
    diameter_m = diameter_km * 1000  # convert km → m
    radius_m = diameter_m / 2
    volume = (4/3) * math.pi * (radius_m ** 3)  # m³
    return volume * density  # kg


def impact_energy(mass: float, velocity_kps: float) -> float:
    """
    Calculate kinetic energy of impact.
    
    Parameters:
        mass: Mass in kilograms
        velocity_kps: Velocity in km/s
    
    Returns:
        Energy in Joules
    """
    velocity_ms = velocity_kps * 1000  # km/s → m/s
    return 0.5 * mass * (velocity_ms ** 2)


def energy_megatons(energy_joules: float) -> float:
    """
    Convert Joules → Megatons of TNT equivalent.
    1 megaton TNT ≈ 4.184e15 Joules
    """
    return energy_joules / 4.184e15

def classify_risk(energy_mt: float) -> str:
    """
    Classify impact energy into historical/comparative risk scales.
    
    References:
    - Hiroshima bomb ~ 0.015 MT
    - Tunguska event ~ 15 MT
    - Chelyabinsk (2013) ~ 0.0005 MT
    - Chicxulub (dinosaur extinction) ~ 1e8 MT
    """
    if energy_mt < 0.001:  # <1 kt
        return "Negligible (smaller than most nuclear tests)"
    elif energy_mt < 0.015:
        return "Comparable to small nuclear bomb (< Hiroshima)"
    elif energy_mt < 1:
        return "Comparable to Hiroshima bomb (15 kt TNT)"
    elif energy_mt < 20:
        return "Comparable to Tunguska event (~15 MT)"
    elif energy_mt < 1e6:
        return "Regional catastrophe (could devastate a country)"
    elif energy_mt < 1e8:
        return "Global consequences (climate disruption)"
    else:
        return "Mass extinction scale (Chicxulub-level event)"
