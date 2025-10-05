import math

# Approximate density of typical stony asteroid
ASTEROID_DENSITY = 3000  # kg/m³

# TNT conversion
JOULES_TO_KT = 4.184e12       # 1 kt TNT
JOULES_TO_MT = 4.184e15       # 1 MT TNT

def compute_kinetic_energy(diameter_km: float, velocity_kms: float, density=ASTEROID_DENSITY):
    """
    Compute kinetic energy in Joules of an asteroid.
    """
    D = diameter_km * 1000  # km → m
    v = velocity_kms * 1000  # km/s → m/s

    mass = (4/3) * math.pi * (D/2)**3 * density
    energy_joules = 0.5 * mass * v**2
    return energy_joules


def classify_risk(energy_joules: float) -> str:
    """
    Simple risk classification comparing impact energy to known events:
    - Hiroshima bomb ~15 kt
    - Tunguska ~15 Mt
    - Chicxulub ~100 million MT
    """
    energy_kt = energy_joules / JOULES_TO_KT
    energy_mt = energy_joules / JOULES_TO_MT

    if energy_kt < 50:
        return f"Low risk (~{energy_kt:.1f} kt TNT)"
    elif energy_mt < 1:
        return f"Moderate risk (~{energy_mt*1000:.1f} kt / {energy_mt:.3f} MT TNT)"
    elif energy_mt < 100:
        return f"High risk (~{energy_mt:.2f} MT TNT) — comparable to Tunguska"
    else:
        return f"Catastrophic (~{energy_mt:.1f} MT TNT) — comparable to Chicxulub"


# Example usage
if __name__ == "__main__":
    diameter_km = 0.3
    velocity_kms = 20
    E = compute_kinetic_energy(diameter_km, velocity_kms)
    risk = classify_risk(E)
    print(f"Kinetic energy: {E:.2e} J")
    print("Risk level:", risk)
