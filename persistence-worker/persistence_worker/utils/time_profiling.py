import time

from persistence_worker.utils.config import ENABLE_PROFILING
from persistence_worker.utils.logger_config import setup_logger


def measure_time(func):
    logger = setup_logger("time_profiling")

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        if ENABLE_PROFILING:
            logger.info(f"{func.__name__} executed in {end - start:.4f} seconds")
        return result

    return wrapper
