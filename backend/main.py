import os

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.query import router as query_router

# Get frontend URL and API key from environment variables
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5500")
API_KEY = os.getenv("APP_TOKEN")

print(f"Allowed Frontend URL: {FRONTEND_URL}")

# Initialize FastAPI application
app = FastAPI(
    title="RAG Backend System",
    description="A FastAPI application for Chime’s visibility and discoverability on AI search platforms",
    version="1.0.0",
)

# CORS middleware for the frontend only
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to check API key
def verify_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/")
async def index():
    return {"message": "Welcome to the FastAPI application"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


app.include_router(query_router, dependencies=[Depends(verify_api_key)])
