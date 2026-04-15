from fastapi import FastAPI, UploadFile
from PIL import Image
import io
import base64

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/split")
async def split_image(file: UploadFile):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))

    width, height = img.size
    grid = 2
    overlap = 0.10

    tile_w = width // grid
    tile_h = height // grid

    tiles = []

    for y in range(grid):
        for x in range(grid):
            left = int(x * tile_w * (1 - overlap))
            top = int(y * tile_h * (1 - overlap))
            right = left + tile_w
            bottom = top + tile_h

            tile = img.crop((left, top, right, bottom))

            buf = io.BytesIO()
            tile.save(buf, format="JPEG")

            tiles.append(base64.b64encode(buf.getvalue()).decode())

    return {"tiles": tiles}
