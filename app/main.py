from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
# Updated import: agents is now included, sukhi is removed
from .routers import auth, prompts, agents

# This command creates/updates all database tables defined in models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sukhi Multi-Agent Admin Backend",
    description="API for managing multiple AI Agents, their profiles, and their prompts.",
    version="2.0.0", # Version updated to reflect major refactor
)

# CORS (Cross-Origin Resource Sharing) Middleware
origins = [
    "*", # For development, allow all origins.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routers from the other files
app.include_router(auth.router)
app.include_router(prompts.router)
app.include_router(agents.router) # <-- Using the new agents router

@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Sukhi Multi-Agent Admin Backend API!"}

