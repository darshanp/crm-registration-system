from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.users import router as users_router
from app.config import get_settings
from app.database import init_db
import os

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="CRM Application with User Registration, E-commerce, and Payment Processing",
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(users_router)

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
def read_root():
    """Serve the frontend registration page."""
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to CRM API", "docs": "/docs"}


@app.get("/verify-email")
def verify_email_page():
    """Serve the email verification page."""
    verify_path = os.path.join(frontend_path, "verify-email.html")
    if os.path.exists(verify_path):
        return FileResponse(verify_path)
    return {"message": "Email verification page not found"}


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "environment": settings.environment}


@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    print(f"\n🚀 Starting {settings.app_name} in {settings.environment} mode")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🌐 Frontend: http://localhost:8000/\n")

    # Create database tables if they don't exist
    try:
        init_db()
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
