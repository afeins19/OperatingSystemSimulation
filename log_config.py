import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name='session_log', log_file='USER_SESSION.log', level=logging.INFO):
    # setup the logger with the file its being written from
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    # Create and configure the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # check if the logger already has handlers
    if not logger.handlers:
        # create a file handler for logging
        handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
        handler.setFormatter(formatter)

        # add handler to the logger
        logger.addHandler(handler)

    return logger
