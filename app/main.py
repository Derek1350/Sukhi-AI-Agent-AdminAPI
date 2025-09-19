from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from .routers import auth, prompts, agents, sukhi_profile # Import the new router

# This command creates/updates all database tables defined in models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sukhi Multi-Agent Admin Backend",
    description="API for managing the global Sukhi Profile and multiple AI Agents.",
    version="3.0.0", # Version updated for new features
)

# CORS Middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the API routers
app.include_router(auth.router)
app.include_router(sukhi_profile.router)
app.include_router(agents.router)
app.include_router(prompts.router)

@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Sukhi Multi-Agent Admin Backend API!"}

