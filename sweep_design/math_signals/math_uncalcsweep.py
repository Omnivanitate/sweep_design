import logging
from math import sqrt
from typing import Any, Callable, Tuple, Union

import numpy as np
from numpy.typing import NDArray

from ..config.sweep_config import SweepConfig

from .defaults import sweep_methods as dfsm
from .defaults.base_structures import BadInputError
from .defaults.sweep_methods import Ftatr
from .math_relation import Relation
from .math_signal import Spectrum
from .math_sweep import Sweep

CallFtatMethod = Callable[[Spectrum], Tuple[np.ndarray, np.ndarray, np.ndarray]]


class UncalculatedSweep:
    '''The UncalculatedSweep class prepares for the calculation of the signal sweep (Sweep).
    
    The get_info_from_ftat function is used to extract the frequency versus time 
    and amplitude versus time functions from the passed f_t and a_t parameters.
        
    Properties:
    ---------------------------------------------------------------------------
        t: Union[RelationProtocol, NDArray] = None
            The Relation class, or a class derived from the Relation class, or 
            an array_like object containing numbers(real or complex).

        f_t: Ftatr = None
            This parameter, which describes changes in frequency over time, 
            can be either an array_like, or an object from which an instance 
            of the Relation class will be created, or an instance of the 
            Relation class, or a callable object that returns a numeric sequence.

            If None, then the linear function f = t will be used.

        a_t: Ftatr = None
            This parameter, which describes changes in amplitude modulation 
            over time, can be either an array_like, or an object from which 
            an instance of the Relation class will be created, or an instance 
            of the Relation class, or a callable object that 
            returns a numeric sequence.
            
            If None, then the function will be assumed to be constant 
            and equal to 1.
        
    '''
    
    def __init__(self, time: NDArray = None, f_t: Union[Ftatr, NDArray] = None, 
                                    a_t: Union[Ftatr, NDArray] = None) -> None:
        
        self._integrate_function_default = SweepConfig.integrate_function
        
        time = time if time is None else np.array(time)
        if not (isinstance(f_t, (np.ndarray, Relation)) or callable(f_t) or f_t is None):
            f_t = np.array(f_t)
        
        if not (isinstance(a_t, (np.ndarray, Relation)) or callable(a_t) or a_t is None):
            a_t = np.array(a_t)


        self._time, self._f_t, self._a_t \
                                = dfsm.get_info_from_ftat(time, f_t, a_t)

    def __call__(self, time: NDArray = None, tht0=0.) -> Sweep:
        '''Calling an instance of the class to calculate the sweep signal.
        
        Properties:
        ----------------------------------------------------------------------
            time: NDArray = None
                The number sequence determines the time.

            tht0: float = 0.
                Zero phase
            
            return Sweep
            Returns an instance of the Sweep class - the calculated sweep signal. 

        If time is not passed or equals None, then the time sequence created 
        when the class instance was initialized will be used.
        
        '''
        logging.info('Calling uncalculated sweep.\n'\
                    'with params:\nf_t={0}\na_t={1}\ntime={2}'\
                    ''.format(self._f_t, self._a_t, time))

        if time is None and self._time is None:
            raise BadInputError('Not enough data: time')
        
        elif time is None and self._time is not None:
            calc_time = self._time
        elif time is not None: 
            calc_time = time
        
        if self._f_t.__name__ == "interpolate_time":
            tht = self._array_tht(self._f_t(calc_time)) 
        else:
            tht = self._func_tht(self._f_t)

        sweep = self._a_t(calc_time)*np.sin(tht(calc_time)+tht0) 
        
        a_t = Relation(calc_time, self._a_t(calc_time))
        f_t = Relation(calc_time, self._f_t(calc_time))

        return Sweep(time=calc_time, amplitude=sweep, f_t=f_t, a_t=a_t)


    def _func_tht(self, f_t: Callable[[np.ndarray], np.ndarray]) \
                                    -> Callable[[np.ndarray], np.ndarray]:
        '''Functional representation of angular sweep.'''                            
        def result(time: np.ndarray) -> np.ndarray:
            return self._integrate_function_default(f_t, time)
        return result

    def _array_tht(self, f_t: np.ndarray) -> Callable[[np.ndarray], np.ndarray]:
        '''Angular sweep represented by a numerical sequence.'''
        def result(time: np.ndarray) -> np.ndarray: 
            f_t_relation = Relation(time, f_t)
            return np.append(
            [0.], 2*np.pi*f_t_relation.integrate().y)
        return result


class ApriorUncalculatedSweep(UncalculatedSweep):
    '''ApriorUncalculatedSweep
    
    Class for constructing a sweep signal from a priori data 
    (from another signal or spectrum)
    
    The calculation of the change in frequency with time (f_t) and 
    the amplitude envelope with time (a_t) will depend on the a priori data 
    (aprior_data) and on the method (ftat_method) by which they will be calculated.

    If the conversion method (ftat_method) is not defined or None, 
    then the method is taken from the Config class freq2time. Method can be 
    overridden if necessary (sweep_design.math_signals.config.Config.freq2time).
    The extracted frequency over time (f_t) and the amplitude envelope over time (a_t) 
    will be send to the UncalculatedSweep constructor.
    '''
    
    def __init__(self, t: Any = None, aprior_data: Any = None, 
                 ftat_method: CallFtatMethod = None) -> None:
    
        if not ftat_method:
            ftat_method = SweepConfig.freq2time

        f_t, a_t, self._aprior_signal \
            = dfsm.get_info_from_aprior_data(t, aprior_data, ftat_method)
        super().__init__(t, f_t, a_t)
        
    def __call__(self, time: Any = None, tht0 = 0., is_normolize = True) -> Sweep:
        '''Calculate the sweep and normolise it.'''
        sweep = super().__call__(time=time, tht0 = tht0)
        
        if is_normolize:
            norm_sweep = sweep.get_norm()
            norm_aprior = self._aprior_signal.get_norm()
            norm = sqrt(norm_aprior)/sqrt(norm_sweep)
            sweep.a_t *= norm
            sweep *= norm
    
        sweep.aprior_signal = self._aprior_signal
        return sweep
        

