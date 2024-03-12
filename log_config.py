import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name='session_log', log_file='USER_SESSION.log', level=logging.INFO):
    """Function to setup a logger for a specific module."""
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    # Create and configure the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Check if the logger already has handlers
    if not logger.handlers:
        # Create a file handler for logging
        handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
        handler.setFormatter(formatter)

        # Add handler to the logger
        logger.addHandler(handler)

    return logger
