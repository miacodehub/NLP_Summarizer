from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routes.files import router as files_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files_router)

# Path to frontend folder
frontend_path = Path("../frontend")


# Serve static files (CSS, JS, images)
app.mount(
    "/static",
    StaticFiles(directory=frontend_path),
    name="static"
)


# Serve frontend UI
@app.get("/")
def serve_frontend():
    return FileResponse(frontend_path / "index.html")