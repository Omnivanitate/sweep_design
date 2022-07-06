from typing import TypeVar

import numpy as np

from ..math_relation import Relation
from ..utility_functions.emd_analyse import get_IMFs_ceemdan

Signal = TypeVar('Signal', bound=Relation)


def correcte_sweep(signal: Signal, start_window: float = None) -> Signal:
    '''Sweep correction.

    Using the EMD to subtract the last IMF from the displacement and apply 
    a window in the star so that the displacement starts at zero.
    '''
    
    displacement = signal.integrate().integrate()
    x, y = displacement.get_data()

    x_w: np.ndarray = np.linspace(0, start_window, int(start_window/(x[1]-x[0])))
    y_w: np.ndarray = np.sin(np.pi/2*x_w/x_w.max())
    sin_corrections = np.append(y_w, np.ones(y.size-y_w.size))

    IMFs = get_IMFs_ceemdan(displacement)
    new_displacement = (displacement-IMFs[0])*Relation(x, sin_corrections)    
    
    signal = new_displacement.diff().diff()
    
    return signal

def correcte_sweep_without_window(signal: Signal) -> Signal:
    ''' Using the EMD to subtract the last IMF from the displacement.
    
    '''
    displacement = signal.integrate().integrate()
    IMFs = get_IMFs_ceemdan(displacement)
    signal = (displacement-IMFs[0]).diff().diff()
    return signal
