import numpy as np
from scipy.signal.windows import tukey


def tukey_a_t(time: np.ndarray, t_tapper: float) -> np.ndarray:
    '''Tukey function to build the envelop for sweep signal.
    
    Parametrs:
    > time: np.ndarray - time axis
    > t_tapper: float - shape of tukey window in time.
    Returns:
    > envelope: np.ndarray
    '''
    

    if t_tapper<=time[int(time.size/2)]:
        tapper = time[time<=t_tapper].size*2/time.size
    else:
        tapper = 1.
    return tukey(time.size, alpha=tapper)
