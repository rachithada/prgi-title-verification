from fastapi import FastAPI
from app.config import settings
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.data.existing_titles import load_titles

app = FastAPI(title=settings.PROJECT_NAME)

# ✅ Load data BEFORE app starts accepting requests
load_titles()

app.include_router(router, prefix="/api")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "backend is running",
        "project": settings.PROJECT_NAME
    }