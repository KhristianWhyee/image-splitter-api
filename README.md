# Image Splitter API

FastAPI service that splits an image into a 4x4 grid of tiles with 15% overlap and returns them as base64-encoded JPEGs.

## Endpoints

- `GET /health` — health check
- `POST /split` — multipart form upload with field `file`. Returns `{ "tiles": [<base64 jpeg>, ...] }` (16 tiles)

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Deploy to Railway

1. Connect this repo to a new Railway service.
2. Railway auto-detects the `Dockerfile` and deploys.
3. Railway injects `$PORT`; the container binds to it.

## Example usage

```bash
curl -X POST -F "file=@blueprint.png" https://<your-railway-url>/split
```
