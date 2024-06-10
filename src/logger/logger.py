from pathlib import Path
from typing import Callable
import logging
import os, sys

# Setup for logging and root_path for referencing files/dirs consistently
project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.abspath(project_root))

wrapper_log_path = Path(f"{project_root}/logs/func_wrapper.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


# Generic logger for use inside of functions or other objects
def setup_logger(name: str, log_file: Path, level=logging.DEBUG) -> logging.Logger:
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# Wrapper for logging functions specifically
def func_log(func: Callable) -> Callable:
    wrapper_logger = setup_logger("wrapper_log_path", wrapper_log_path)

    def wrapper(*args, **kwargs):
        wrapper_logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        wrapper_logger.info(f"{func.__name__} returned {func(*args, **kwargs)}")
        return func(*args, **kwargs)

    return wrapper
