import os
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_directory = os.getenv("LOG_DIRECTORY", "logs")
log_file = os.path.join(log_directory, "auth.log")

# Ensure log directory exists
os.makedirs(log_directory, exist_ok=True)

# Default retention period (7 days)
retention_days = int(os.getenv("LOG_RETENTION_DAYS", "7"))

logger = logging.getLogger("auth_logger")

def setup_logger(days):
    # Remove all existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Configure timed rotating file handler
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=days
    )
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Set logging level
    logger.setLevel(logging.INFO)

# Initial setup
setup_logger(retention_days)

logger.info(f"Logging system initialized with {retention_days} days retention policy")

log_router = APIRouter()

class RetentionConfig(BaseModel):
    days: int

@log_router.post("/config/log-retention")
def set_log_retention(config: RetentionConfig):
    """
    Endpoint to configure log retention period.
    """
    global retention_days
    if config.days < 1:
        raise HTTPException(status_code=400, detail="Retention period must be at least 1 day")
    if config.days > 365:  
        raise HTTPException(status_code=400, detail="Retention period cannot exceed 365 days")
    
    retention_days = config.days
    setup_logger(retention_days)
    logger.info(f"Log retention period updated to {retention_days} days")
    return {"message": f"Log retention period set to {retention_days} days"}

@log_router.get("/config/log-retention")
def get_log_retention():
    """
    Endpoint to get current log retention period.
    """
    return {"retention_days": retention_days}
