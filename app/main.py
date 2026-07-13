from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base
from .api.v1.router import router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie API",
    version="1.0.0",
    debug=settings.DEBUG,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# CORS - FIXED
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Movie API is running", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}