import logging
import os

# Ensure logs directory exists
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Configure the logger
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "cybertoolkit.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def get_logger(name):
    """
    Returns a configured logger instance with the given name.
    """
    logger = logging.getLogger(name)
    # Also log to console for debugging purposes
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(console_handler)
    return logger
