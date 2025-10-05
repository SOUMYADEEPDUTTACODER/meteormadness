from astropy import units as u
from poliastro.bodies import Sun
from poliastro.twobody import Orbit
from astropy.time import Time
import numpy as np

def safe_float(value, default=0.0):
    """Convert string to float safely; fallback to default if empty."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def orbit_from_elements(orbital_data: dict):
    """
    Create an Orbit object from NASA's orbital elements.
    """
    a = safe_float(orbital_data.get("semi_major_axis")) * u.AU
    ecc = safe_float(orbital_data.get("eccentricity"))* u.one
    inc = safe_float(orbital_data.get("inclination")) * u.deg
    raan = safe_float(orbital_data.get("ascending_node_longitude")) * u.deg
    argp = safe_float(orbital_data.get("perihelion_argument")) * u.deg
    M = safe_float(orbital_data.get("mean_anomaly")) * u.deg

    epoch_jd = safe_float(orbital_data.get("epoch_osculation"))
    epoch = Time(epoch_jd, format="jd")

    return Orbit.from_classical(Sun, a, ecc, inc, raan, argp, M, epoch=epoch)

def propagate_orbit(orbit, days=30):
    """
    Propagate orbit forward by N days and return new Orbit object.
    """
    future_orbit = orbit.propagate(days * u.day)
    return future_orbit

def get_heliocentric_coordinates(orbit):
    """
    Return X, Y, Z position in AU for a given Orbit object.
    """
    r = orbit.r.to(u.AU).value  # Convert to AU
    x, y, z = r[0], r[1], r[2]
    return x, y, z
