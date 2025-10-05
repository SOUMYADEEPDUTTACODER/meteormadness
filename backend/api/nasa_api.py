# backend/api/nasa_api.py
import requests
import os
from backend.config import NASA_API_KEY, BASE_URL

def fetch_neo_by_id(asteroid_id: str):
    """
    Lookup a specific asteroid by its NASA SPK-ID.
    Returns JSON response with orbital and physical data.
    """
    url = f"{BASE_URL}/{asteroid_id}?api_key={NASA_API_KEY}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def extract_key_fields(neo_json):
    """
    Extract the important fields needed for simulation.
    """
    return {
        "name": neo_json.get("name"),
        "id": neo_json.get("id"),
        "diameter_km": neo_json["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
        "orbital_data": neo_json["orbital_data"],
        "close_approach": [
            {
                "velocity_kps": float(entry["relative_velocity"]["kilometers_per_second"]),
                "miss_distance_km": float(entry["miss_distance"]["kilometers"]),
                "date": entry["close_approach_date"]
            }
            for entry in neo_json.get("close_approach_data", [])
        ]
    }
