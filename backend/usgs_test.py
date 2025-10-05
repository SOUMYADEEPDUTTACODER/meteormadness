from pathlib import Path
import rasterio

# Correct path to USGS tiles folder
USGS_DIR = Path(__file__).resolve().parent / "data" / "usgs"

print("USGS Tiles and their bounding coordinates:")

for tif in USGS_DIR.glob("*.tif"):
    try:
        with rasterio.open(tif) as src:
            bounds = src.bounds
            # bounds: left, bottom, right, top (lon/lat)
            print(
                f"{tif.name}: "
                f"Top Left (lat, lon): ({bounds.top:.4f}, {bounds.left:.4f}), "
                f"Bottom Right (lat, lon): ({bounds.bottom:.4f}, {bounds.right:.4f})"
            )
    except Exception as e:
        print(f"Could not read {tif.name}: {e}")