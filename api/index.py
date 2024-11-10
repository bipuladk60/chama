from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .routers import gemini, news, telegram
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up FastAPI application...")
    
    # Initialize Telegram session
    try:
        await telegram.initialize_client()
        logger.info("Telegram client initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Telegram client: {e}")
        # Don't raise the error, let the app start anyway
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI application...")
    try:
        await telegram.disconnect_client()
        logger.info("Telegram client disconnected successfully")
    except Exception as e:
        logger.error(f"Error disconnecting Telegram client: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/py/docs",
    openapi_url="/api/py/openapi.json"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/py/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}
