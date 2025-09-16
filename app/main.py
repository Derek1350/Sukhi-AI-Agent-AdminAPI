from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from .routers import auth, prompts, sukhi

# This command creates all the database tables defined in models.py
# It will not recreate tables that already exist.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sukhi Admin Backend",
    description="API for managing the Sukhi AI Agent, its profile, and its prompts.",
    version="1.0.0",
)

# CORS (Cross-Origin Resource Sharing) Middleware
# This allows your frontend application to make requests to this backend.
# You can restrict the origins for production environments.
origins = [
    "*", # For development, allow all origins.
    # "http://localhost:3000", # Example for a React frontend
    # "https://your-frontend-domain.com",
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
app.include_router(sukhi.router)

@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Sukhi Admin Backend API!"}