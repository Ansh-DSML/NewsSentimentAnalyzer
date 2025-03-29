import logging
import os

# Define log file path
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Create log directory if not exists
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def get_logger(name: str):
    """Returns a logger instance with the given name."""
    return logging.getLogger(name)
