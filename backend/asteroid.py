import requests
import os
from backend.config import NASA_API_KEY, BASE_URL

print("API KEY:", NASA_API_KEY)


def get_sample_asteroids(limit=10):
    url = f"{BASE_URL}?api_key={NASA_API_KEY}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    neos = data.get("near_earth_objects", [])
    print(f"Found {len(neos)} asteroids (showing first {limit}):\n")

    for i, asteroid in enumerate(neos[:limit]):
        print(f"{i+1}. ID: {asteroid['id']} | Name: {asteroid['name']}")

if __name__ == "__main__":
    get_sample_asteroids()