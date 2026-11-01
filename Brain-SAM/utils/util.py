import logging
import os


def setup_logger(logger_name, root, screen=False, tofile=False):
    """Configure the logger used by training and inference."""
    os.makedirs(root, exist_ok=True)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    if screen:
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    if tofile:
        file_handler = logging.FileHandler(os.path.join(root, f"{logger_name}.log"))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.propagate = False
    return logger
