from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.query import router as query_router

app = FastAPI(
    title="RAG Backend System",
    description="A FastAPI application for analysing and comparing survey datasets using AI.",
    version="1.0.0"
)

@app.get("/")
async def index():
    return {"message": "Welcome to the FastAPI application"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(query_router)

# Allow CORS from your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development purposes. In production, specify your frontend URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)