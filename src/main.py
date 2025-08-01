from enum import Enum
import io, random, base64
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the template engine
templates = Jinja2Templates(directory="templates")

class MeshType(str, Enum):
    curtain = "curtain"
    tube = "tube"
    cape = "cape"
    skirt = "skirt"

def generate_stl_with_seed(type: MeshType = MeshType.curtain,
                            numFolds: int = 5,
                            minRuffleWidth: float = 0.1,
                            maxRuffleWidth: float = 0.3,
                            minBaseWidth: float = 0.1,
                            maxBaseWidth: float = 0.3,
                            minHeight: float = 0.1,
                            maxHeight: float = 0.3,
                            symmetricFold: bool = False,
                            seed: int = None):
    # Use provided seed or generate one
    actual_seed = seed if seed is not None else random.randint(0, 1e9)
    random.seed(actual_seed)

    # Generate mesh here, default type is curtain
    mesh = #TODO: generate mesh with given parameters
    # if type == MeshType.curtain:
    if type == MeshType.tube:
    elif type == MeshType.cape:
    elif type == MeshType.skirt:

    # Save STL to BytesIO
    stl_io = io.BytesIO()
    mesh.save(stl_io)
    stl_io.seek(0)
    
    # Convert to base64 so it can be returned as JSON
    stl_base64 = base64.b64encode(stl_io.read()).decode('utf-8')
    
    return {"stl_data": stl_base64, "seed": actual_seed}

@app.get("/generate-stl")
def generate_stl(type: MeshType = Query(..., description="Type of mesh to generate"),
                numFolds: int = Query(5, ge=1, le=100),
                minRuffleWidth: float = Query(0.1),
                maxRuffleWidth: float = Query(0.3),
                minBaseWidth: float = Query(0.1),
                maxBaseWidth: float = Query(0.3),
                minHeight: float = Query(0.1),
                maxHeight: float = Query(0.3),
                symmetricFold: bool = Query(False),
                seed: int = Query(None)):
    result = generate_stl_with_seed(seed)
    return JSONResponse(content=result)

# Route for homepage
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})