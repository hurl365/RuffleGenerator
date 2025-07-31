from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import io, random

app = FastAPI()

@app.get("/generate-stl")
def generate_stl(
    numFolds: int = Query(5, ge=1, le=100),
    minRuffleWidth: float = Query(0.1),
    maxRuffleWidth: float = Query(0.3),
    minBaseWidth: float = Query(0.1),
    maxBaseWidth: float = Query(0.3),
    minHeight: float = Query(0.1),
    maxHeight: float = Query(0.3),
    symmetricFold: bool = Query(True),
    seed: int = Query(None)
):
    if seed is None:
        seed = random.randint(0, 1e9)
    random.seed(seed)

    # Dummy mesh example — replace with your actual control point logic
    mesh = #TDOD: generate mesh using given parameters

    stl_io = io.BytesIO()
    mesh.export(stl_io, file_type='stl')
    stl_io.seek(0)
    return StreamingResponse(stl_io, media_type="application/sla")