import logging
from typing import Union, Callable, Any, Tuple
from math import sqrt

from scipy import integrate  # type: ignore
import numpy as np

from math_signals.math_relation import Relation
from math_signals.math_signal import Signal, Spectrum
from math_signals.math_sweep import Sweep

import math_signals.defaults.sweep_methods as dfsm
from math_signals.defaults.base_structures import BadInputError

CallFtatMethod = Callable[[Spectrum], Tuple[np.ndarray, np.ndarray, np.ndarray]]

IntegrateFuction = Callable[[
    Callable[[np.ndarray], np.ndarray], Any, Any], Any]

IntegrateArray = Callable[[np.ndarray, np.ndarray], np.ndarray]

Ftat = Union[np.ndarray, Callable[[np.ndarray], np.ndarray]]
Ftatr = Union[Relation, np.ndarray, Callable[[np.ndarray], np.ndarray]]


class UncalculatedSweep:
    '''Класс UncalculatedSweep выполняет подготовку для расчета свип сигнала (Sweep)

    В зависимости от того какий параметры будут переданы, будут вычислены 
    соответствующие функции изменения частоты от времени и амплитуды от времени.
    Если пераданы параметры aprior_signal и параметр(ы) f_t и(или) a_t, то 
    функции будут вычеслены по параметру aprior_signal. 
    
    Для расчета функций изменения частоты от времени и амплитуды от 
    времени из априорного сигнала применяется функция get_info_from_aprior_data
    Для извлечении функций изменения частоты от времени и амплитуды от времени 
    из переданныйх параметров f_t и a_t применяется функция get_info_from_f_t_a_t
        
    Параметры:
        t: Any
            None, или объект Relation, или наследумый от него объект, или
            сущность, из которой будет извелечен объект array_like 
            (или извленчены объекты array_like), 
            содержащий(ие) только числа (простые и(или) комплексные).

        f_t: Any
            None, или объект Relation, или наследумый от него объект, или
            сущность, из которой будет извелечен объект array_like 
            (или извленчены объекты array_like), 
            содержащий(ие) только числа (простые и(или) комплексные) или
            вызываемы объект (функция изменения частоты от времени).
            
            Данный параметр, описывающий отношение изменения частоты и времени, 
            может быть или array_like, или объектом, 
            из которого будет создан экземпляр калсса Relation, 
            или экземпляр класса Relation,
            или вызываемы объект, возращающий числовую последовательность, или None.

            Если None, то будет использована линейная функция f = t.

        a_t: Any 
            None, или объект Relation, или наследумый от него объект, или
            сущность, из которой будет извелечен объект array_like 
            (или извленчены объекты array_like), 
            содержащий(ие) только числа (простые и(или) комплексные) или
            вызываемы объект (функция изменения амплитуды от времени).
            
            Данный параметр, описывающий изменения амплитудной модуляции от 
            времени, может быть или array_like, или объектом, из которого будет
            создан экземпляр калсса Relation, или экземпляр класса Relation,
            или вызываемы объект, возращающий числовую последовательность.

            Если None, то будет пологаться, что функция сонстанта и равна 1.

        aprior_data: Signal или Spectrum или None
            Сигнал или спектр, по кторому будет построен свип-сигнал.
        
        ftat_method: Callable
            вызываемый объект, по которому из априорного сигнала будут 
            расчитаны функция изменений частоты от времени и
            функция изменения амплитуды от времени.
    '''
    integrate_function_default = staticmethod(integrate.quad)
    integrate_array_default = staticmethod(integrate.cumtrapz)
    
    def __init__(self, t: np.ndarray = None, f_t: Ftat = None, 
                                            a_t: Ftat = None) -> None:
        self._t, self._f_t, self._a_t \
                                = dfsm.get_info_from_ftat(t, f_t, a_t)

    def __call__(self, time: np.ndarray = None, tht0=0.) -> Sweep:
        '''Фызов экземпляра класса для рассчета свип-сигнала.
        
        Параметры:
            time: array_like or None
                Числовая последовательность определяющая время
            
        Возращаемое значение: Sweep
            Возращает экземляр класса Sweep - расчитаного свип сигнала. 

        Если time не передан и равен None, то будет использована 
        последовательность _t, созданая при инициализации экземпляра класса. 
        
        '''
        logging.debug('Calling uncalculated sweep.\n'\
                    'with params:\nf_t={0}\na_t={1}\ntime={2}'\
                    ''.format(self._f_t, self._a_t, time))

        if time is None and self._t is not None:
            time = self._t
        else:
            raise BadInputError('Not enough data: time')
        
        if self._f_t.__name__ == "interpolate_time":
            tht = self._array_tht(self._f_t(time)) 
        else:
            tht = self._func_tht(self._f_t)

        sweep = self._a_t(time)*np.sin(tht(time)+tht0) 
        
        a_t = Relation(time, self._a_t(time))
        f_t = Relation(time, self._f_t(time))

        logging.debug('Make sweep.')
        return Sweep(t=time, A=sweep, f_t=f_t, a_t=a_t)


    def _func_tht(self, f_t: Callable[[np.ndarray], np.ndarray]) \
                                    -> Callable[[np.ndarray], np.ndarray]:
            def result(time: np.ndarray) -> np.ndarray:
                return np.append([0.], np.array(
                [2*np.pi*UncalculatedSweep.integrate_function_default(f_t, time[0], t)[0] for t in time[1:]]))
            return result

    def _array_tht(self, f_t: np.ndarray) -> Callable[[np.ndarray], np.ndarray]:
        def result(time: np.ndarray) -> np.ndarray: 
            return np.append(
            [0.], 2*np.pi*UncalculatedSweep.integrate_array_default(f_t, time))
        return result


class ApriorUncalculatedSweep(UncalculatedSweep):

    freq2time_default = staticmethod(dfsm.simple_freq2time)

    def __init__(self, t: Any = None, aprior_data: Any = None, 
                 ftat_method: CallFtatMethod = None) -> None:
    
        if not ftat_method:
            ftat_method = self.freq2time_default

        f_t, a_t, self._aprior_signal \
            = dfsm.get_info_from_aprior_data(t, aprior_data, ftat_method)
        super().__init__(t, f_t, a_t)
        
    def __call__(self, time: Any = None, tht0 = 0.) -> Sweep:
        sweep = super().__call__(time=time, tht0 = tht0)
        norm_sweep = sweep.get_norm()
        norm_aprior = self._aprior_signal.get_norm()
        norm = sqrt(norm_aprior)/sqrt(norm_sweep)
        sweep.a_t *= norm
        sweep *= norm
        sweep.aprior_signal = self._aprior_signal
        return sweep
        

