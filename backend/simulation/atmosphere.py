def estimate_atmospheric_changes(kinetic_energy: float, impact_lat: float, impact_lon: float) -> dict:
    """
    Estimate simple atmospheric changes after an impact.
    Returns a dict with temperature rise, pressure wave, and wind speed.
    """
    # These are illustrative formulas, not real science!
    temp_rise = min(kinetic_energy / 1e18, 10)  # Max 10°C rise
    pressure_wave = min(kinetic_energy / 1e17, 500)  # Max 500 hPa
    wind_speed = min(kinetic_energy / 1e16, 300)  # Max 300 km/h

    return {
        "temperature_rise_C": round(temp_rise, 2),
        "pressure_wave_hPa": round(pressure_wave, 2),
        "wind_speed_kmh": round(wind_speed, 2),
        "location": (impact_lat, impact_lon)
    }