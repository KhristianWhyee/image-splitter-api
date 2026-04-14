from fastapi import FastAPI, UploadFile
from PIL import Image
import io
import base64
import numpy as np

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


def is_tile_useful(tile, threshold=240):
    """
    Detect if tile is mostly empty (white/light background)
    """
    gray = tile.convert("L")
    arr = np.array(gray)

    # % of pixels that are NOT white
    non_white_ratio = np.mean(arr < threshold)

    return non_white_ratio > 0.02  # tweakable


@app.post("/split")
async def split_image(file: UploadFile):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    width, height = img.size

    # 🔥 Dynamic grid (KEY OPTIMIZATION)
    if width > 3000:
        grid = 6
    elif width > 1500:
        grid = 4
    else:
        grid = 3

    overlap = 0.15

    tile_w = width // grid
    tile_h = height // grid

    tiles = []

    for y in range(grid):
        for x in range(grid):

            left = int(x * tile_w * (1 - overlap))
            top = int(y * tile_h * (1 - overlap))
            right = min(left + tile_w, width)
            bottom = min(top + tile_h, height)

            tile = img.crop((left, top, right, bottom))

            # 🔥 FILTER EMPTY TILES
            if not is_tile_useful(tile):
                continue

            # 🔥 Resize for faster inference
            tile = tile.resize((512, 512))

            buf = io.BytesIO()
            tile.save(buf, format="JPEG", quality=70)

            tiles.append({
                "image": base64.b64encode(buf.getvalue()).decode(),
                "x": x,
                "y": y,
                "grid": grid
            })

    return {
        "tile_count": len(tiles),
        "tiles": tiles
    }
