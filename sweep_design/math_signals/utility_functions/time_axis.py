import numpy as np
from loguru import logger


def get_time(end=10, dt=0.001, start=0):
    """Create and return time axis."""
    time = np.linspace(start, end, int((end - start) / dt) + 1)
    logger.info(
        "Time axis was created with next parameters: start - {}, end - {} dt - {}",
        time[0],
        time[-1],
        dt,
    )
    return time
