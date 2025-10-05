#!/usr/bin/env python3
"""
Integrated asteroid impact simulation runner (Steps 1-5).
"""

import json
from pathlib import Path
from datetime import datetime

# NASA / orbital
from backend.api.nasa_api import fetch_neo_by_id, extract_key_fields
from backend.simulation.orbital import (
    orbit_from_elements,
    propagate_orbit,
    get_heliocentric_coordinates,
)

# Energy + risk
from backend.simulation.impact_energy import compute_kinetic_energy, classify_risk

# Consequences + DEM
from backend.simulation.consequences import (
    estimate_crater_size,
    estimate_seismic_magnitude,
    estimate_tsunami_height,
)
from backend.data.dem_loader import get_local_elevation
from backend.simulation.atmosphere import estimate_atmospheric_changes

# Output path
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = DATA_DIR / "simulation_result.json"


def pretty_print_vec(name, vec):
    try:
        x, y, z = vec
        print(f"{name}: X={x:.6f} AU, Y={y:.6f} AU, Z={z:.6f} AU")
    except Exception:
        print(f"{name}: {vec}")


def get_elevation_from_usgs_tiles(lat, lon):
    """Wrapper around get_local_elevation (returns 0.0 if fails)."""
    try:
        elev = get_local_elevation(lat, lon)
        print(f"✅ Elevation at ({lat}, {lon}): {elev:.2f} m")
        return elev
    except Exception as e:
        print(f"⚠️ DEM lookup failed at ({lat},{lon}): {e}")
        return 0.0


def run_simulation(
    asteroid_id: str = "3542519",
    impact_lat: float = 24.5,
    impact_lon: float = -80.5,
    dem_source: str = "auto",
    propagate_days: int = 30,
):
    print("=== ASTEROID SIMULATION ===")
    print(f"Time (UTC): {datetime.utcnow().isoformat()}")

    # ----------------------------
    # Step 1: Fetch asteroid data
    # ----------------------------
    print("\n[1] Fetching asteroid data from NASA...")
    raw = fetch_neo_by_id(asteroid_id)
    key = extract_key_fields(raw)

    name = key.get("name", "UNKNOWN")
    diameter_km = float(key.get("diameter_km", 0.0))
    if key.get("close_approach"):
        vel_kps = float(key["close_approach"][0].get("velocity_kps", 0.0))
        miss_km = float(key["close_approach"][0].get("miss_distance_km", 0.0))
        approach_date = key["close_approach"][0].get("date", "N/A")
    else:
        vel_kps = 0.0
        miss_km = None
        approach_date = "N/A"

    print(f"Asteroid: {name} (ID {asteroid_id})")
    print(f"Diameter: {diameter_km:.3f} km")
    print(f"Velocity (sample): {vel_kps:.3f} km/s")
    print(f"Miss distance (sample): {miss_km} km")
    print(f"Approach date: {approach_date}")

    # ----------------------------
    # Step 2: Orbital mechanics
    # ----------------------------
    print("\n[2] Orbit propagation...")
    orbit = orbit_from_elements(key["orbital_data"])
    future_orbit = propagate_orbit(orbit, days=propagate_days)

    print("\n=== ORBITAL ELEMENTS ===")
    print(f"Semi-major axis [AU]: {orbit.a.to('AU').value:.6f}")
    print(f"Eccentricity: {orbit.ecc.value:.6f}")
    print(f"Inclination [deg]: {orbit.inc.to('deg').value:.6f}")
    print(f"RAAN [deg]: {orbit.raan.to('deg').value:.6f}")
    print(f"ArgPeri [deg]: {orbit.argp.to('deg').value:.6f}")
    print(f"True anomaly [deg]: {orbit.nu.to('deg').value:.6f}")

    current_pos = get_heliocentric_coordinates(orbit)
    future_pos = get_heliocentric_coordinates(future_orbit)

    print("\n=== HELIOCENTRIC COORDS ===")
    pretty_print_vec("Current", current_pos)
    pretty_print_vec(f"After {propagate_days} days", future_pos)

    # ----------------------------
    # Step 3: Energy + risk
    # ----------------------------
    print("\n[3] Computing impact energy & risk...")
    energy_j = compute_kinetic_energy(diameter_km, vel_kps)
    energy_mt = energy_j / 4.184e15
    risk_text = classify_risk(energy_j)
    print(f"Energy: {energy_j:.3e} J ({energy_mt:.3f} MT TNT)")
    print(f"Risk: {risk_text}")

    # ----------------------------
    # Step 4: Consequences
    # ----------------------------
    print(f"\n[4] Consequences at impact site ({impact_lat}, {impact_lon})...")
    elevation_m = get_elevation_from_usgs_tiles(impact_lat, impact_lon)

    crater_km = estimate_crater_size(diameter_km, vel_kps)
    seismic_mw = estimate_seismic_magnitude(energy_j)
    tsunami_m = estimate_tsunami_height(diameter_km, vel_kps, distance_km=200)

    print(f"Crater diameter: {crater_km:.3f} km")
    print(f"Seismic magnitude: {seismic_mw:.2f} Mw")
    print(f"Tsunami at 200 km: {tsunami_m:.3f} m")

    # ----------------------------
    # Step 5: Atmospheric changes
    # ----------------------------
    atmo = estimate_atmospheric_changes(energy_j, impact_lat, impact_lon)
    print(f"Estimated temperature rise: {atmo['temperature_rise_C']} °C")
    print(f"Estimated pressure wave: {atmo['pressure_wave_hPa']} hPa")
    print(f"Estimated wind speed: {atmo['wind_speed_kmh']} km/h")

    # ----------------------------
    # Build unified result dict
    # ----------------------------
    result = {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "asteroid": {
            "id": asteroid_id,
            "name": name,
            "diameter_km": diameter_km,
            "velocity_kps_sample": vel_kps,
            "approach_date": approach_date,
            "miss_distance_km_sample": miss_km,
        },
        "orbit": {
            "epoch_jd": float(orbit.epoch.jd),
            "semi_major_axis_AU": float(orbit.a.to("AU").value),
            "eccentricity": float(orbit.ecc.to("")),
            "inclination_deg": float(orbit.inc.to("deg").value),
            "raan_deg": float(orbit.raan.to("deg").value),
            "argp_deg": float(orbit.argp.to("deg").value),
            "true_anomaly_deg": float(orbit.nu.to("deg").value),
            "heliocentric_current": {
                "x_AU": float(current_pos[0]),
                "y_AU": float(current_pos[1]),
                "z_AU": float(current_pos[2]),
            },
            "heliocentric_future": {
                "x_AU": float(future_pos[0]),
                "y_AU": float(future_pos[1]),
                "z_AU": float(future_pos[2]),
            },
        },
        "energy": {
            "joules": energy_j,
            "megatons_tnt": energy_mt,
            "risk_text": risk_text,
        },
        "consequences": {
            "impact_location": {"lat": impact_lat, "lon": impact_lon, "elevation_m": elevation_m},
            "crater_km": crater_km,
            "seismic_mw": seismic_mw,
            "tsunami_m_at_200km": tsunami_m,
            "atmospheric_changes": atmo,
        },
    }

    # Save to disk
    try:
        with open(OUT_PATH, "w") as fh:
            json.dump(result, fh, indent=2)
        print(f"\n✅ Results saved to {OUT_PATH}")
    except Exception as e:
        print(f"❌ Could not save results: {e}")

    print("\n=== End of simulation ===")
    return result


if __name__ == "__main__":
    run_simulation(
        asteroid_id="3542519",
        impact_lat=28.5,
        impact_lon=-89.5,
        dem_source="auto",
        propagate_days=30,
    )
