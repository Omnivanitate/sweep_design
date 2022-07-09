import numpy as np


def f_t_linear_function(f_start, f_end, time):
    return lambda t: t * (f_end - f_start) / (time[-1] - time[0]) + f_start


def f_t_linear_array(time: np.ndarray, f_start=0.0, f_end=1.0):
    return time * (f_end - f_start) / (time[-1] - time[0]) + f_start
