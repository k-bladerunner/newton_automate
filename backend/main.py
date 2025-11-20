from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, assignments, schedule, solver, performance
from config import settings
import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Newton Autopilot API",
    description="AI-powered automation for Newton School portal",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Newton Autopilot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api": "operational"
    }


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(assignments.router, prefix="/api/assignments", tags=["Assignments"])
app.include_router(schedule.router, prefix="/api/schedule", tags=["Schedule"])
app.include_router(solver.router, prefix="/api/solve", tags=["AI Solver"])
app.include_router(performance.router, prefix="/api/performance", tags=["Performance"])


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Newton Autopilot API starting up...")
    logger.info(f"Frontend URL: {settings.frontend_url}")
    logger.info(f"API configured with database: {settings.database_url}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Newton Autopilot API shutting down...")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )
