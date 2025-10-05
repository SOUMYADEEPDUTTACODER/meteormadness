from pathlib import Path
import rasterio

tile_path = Path("backend/data/usgs/USGS_1_n29w090_20231213.tif")

# Test coordinates inside the tile bounds
lat, lon = 28.5, -89.5

with rasterio.open(tile_path) as src:
    print("CRS:", src.crs)
    print("Bounds:", src.bounds)
    print("Width x Height:", src.width, "x", src.height)
    print("Nodata value:", src.nodata)
    arr = src.read(1)
    print("Min:", arr.min(), "Max:", arr.max())

    # Get row, col for the test coordinates
    col, row = src.index(lon, lat)
    if 0 <= row < arr.shape[0] and 0 <= col < arr.shape[1]:
        val = arr[row, col]
        print(f"Elevation at ({lat}, {lon}): {val}")
        if src.nodata is not None and val == src.nodata:
            print("  -> Warning: Value is nodata (no elevation here)")
    else:
        print(f"Coordinates ({lat}, {lon}) are outside the raster bounds.")