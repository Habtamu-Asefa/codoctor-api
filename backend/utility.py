import time
import functools
from setup import logger

def timing_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Function {func.__name__} executed in {end_time - start_time:.4f} seconds", extra={"performance": True, "function_name": func.__name__, "execution_time": end_time - start_time})
        return result
    return wrapper

