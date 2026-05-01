from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
import os

app = FastAPI(
    title="Election Process Education API",
    description="Backend service for interactive election education.",
    version="1.0.0"
)

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(router, prefix="/api/v1")

# Serve React Frontend
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

# Mount the static assets folder specifically
assets_dir = os.path.join(STATIC_DIR, "assets")
if os.path.isdir(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Catch-all to serve index.html for the root UI
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.isfile(index_file):
        return FileResponse(index_file)
    return {"message": "API is running. Frontend build not found. Please run Docker build."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
