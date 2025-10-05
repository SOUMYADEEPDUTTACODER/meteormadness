import os
import requests
from tqdm import tqdm
from pathlib import Path

RAW_FOLDER = "data/raw/usgs"
OUT_FOLDER = "data/usgs"
os.makedirs(RAW_FOLDER, exist_ok=True)
os.makedirs(OUT_FOLDER, exist_ok=True)

# Full U.S. bounding box (xmin, ymin, xmax, ymax)
US_BBOX = [-85, 24, -75, 32]

DATASET = "National Elevation Dataset (NED) 1 arc-second"
PROD_FORMAT = "GeoTIFF"

def fetch_usgs_tiles(bbox):
    url = (
        "https://tnmaccess.nationalmap.gov/api/v1/products"
        f"?datasets={DATASET}"
        f"&bbox={','.join(map(str, bbox))}"
        f"&prodFormats={PROD_FORMAT}&outputFormat=JSON"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data.get("items", [])

def download_tile(url, output_folder):
    local_filename = os.path.join(output_folder, url.split("/")[-1])
    if os.path.exists(local_filename):
        print(f"Already exists: {local_filename}")
        return local_filename
    try:
        resp = requests.get(url, stream=True, timeout=60)
        if resp.status_code == 404:
            print(f"⚠️ Skipping (404 Not Found): {url}")
            return None
        resp.raise_for_status()
        total_size = int(resp.headers.get('content-length', 0))
        with open(local_filename, 'wb') as f:
            for chunk in tqdm(resp.iter_content(chunk_size=1024*1024),
                              total=total_size//(1024*1024) if total_size else None,
                              unit='MB', desc=os.path.basename(local_filename)):
                f.write(chunk)
        print(f"✅ Downloaded: {local_filename}")
        return local_filename
    except Exception as e:
        print(f"⚠️ Failed to download {url}: {e}")
        return None

def download_usgs_dem(bbox=US_BBOX):
    items = fetch_usgs_tiles(bbox)
    print(f"Found {len(items)} DEM tiles")
    downloaded = []
    for item in items:
        print("Downloading:", item["title"])
        tile = download_tile(item["downloadURL"], OUT_FOLDER)
        if tile:
            downloaded.append(tile)
    print(f"✅ Finished downloading {len(downloaded)} tiles")
    return downloaded

if __name__ == "__main__":
    tiles = download_usgs_dem()
    print("Downloaded tiles:")
    for t in tiles:
        print("-", t)