from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from utils import ottieni_palette_da_immagine

app = FastAPI()

path = Path("data")
path.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {"messaggio": "Estrai palette dei colori da qualasi immagine"}


@app.post("/carica-immagine/")
async def carica_immagine(file: UploadFile = File(...)):
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(
            status_code=400, detail="Carica un file immagine (PNG, JPG, JPEG)"
        )

    percorso_file = Path.joinpath(path, file.filename)
    with open(percorso_file, "wb") as f:
        f.write(await file.read())

    try:
        palette = ottieni_palette_da_immagine(str(percorso_file))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Errore nell'elaborazione dell'immagine: {str(e)}"
        )

    percorso_file.unlink(missing_ok=True)

    return JSONResponse(content={"palette": palette})
