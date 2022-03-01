import logging
from typing import Callable, Union, Any, TYPE_CHECKING, Type
from numbers import Number

import numpy as np
from scipy.interpolate import interp1d  # type: ignore
from scipy.integrate import cumulative_trapezoid, trapz  # type: ignore

from math_signals.defaults.base_structures import BaseXY, TypeFuncError, NotEqualError

if TYPE_CHECKING:
    from math_signals.math_relation import Relation


def math_operation(
        x: np.ndarray,
        y1: np.ndarray,
        y2: Union[np.ndarray, Number],
        name_operation: str,
    ) -> BaseXY:
    if name_operation == '__pow__':
        y = np.abs(y1).__getattribute__(name_operation)(y2)*np.sign(y1)
    else:
        y = y1.__getattribute__(name_operation)(y2)

    return BaseXY(x, y)

def extract_input(x: Any, y: Any) -> BaseXY:
    if y is None:
        if isinstance(x, (tuple, list,)):
            x, y = x[0], x[1]
        if isinstance(x, dict):
            x = list(x.values())
            x, y = x[0], x[1]
        
    x, y = np.array(x), np.array(y)
    if x.size != y.size:
        raise NotEqualError(x.size, y.size)
    return BaseXY(np.array(x), np.array(y))


def one_integrate(y: np.ndarray, x: np.ndarray = None) -> float:
    '''Интегрирование.

    Определение интеграла функции на отрезке.
    '''
    return trapz(y, x)


def integrate(x: np.ndarray, y: np.ndarray) -> BaseXY:
    '''Интегрирование. 
        
    Примение функции scipy.integrate.cumtrapz.
    '''
    return BaseXY(x[1:], cumulative_trapezoid(y)*(x[1]-x[0]))


def differentiate(x: np.ndarray, y: np.ndarray) -> BaseXY:
    '''Интегрирование.

    Примение функции np.diff'''
    return BaseXY(x[:-1]+(x[1]-x[0])/2, np.diff(y)/(x[1]-x[0]))

def interpolate_extrapolate(x: np.ndarray, y: np.ndarray, bounds_error=False,
                            fill_value=0.) -> Callable[[np.ndarray], np.ndarray]:
    '''Интерполяция.

    Применение функции scyipy.interpolate.interp1d.
    Возращается функция интерполяции.
    '''
    return interp1d(x, y, bounds_error=bounds_error, fill_value=fill_value)

def get_common_x(x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
    dx1 = x1[1]-x1[0]
    dx2 = x2[1]-x2[0]
    dx = dx1 if dx1 <= dx2 else dx2
    x_start = x1[0] if x1[0] <= x2[0] else x2[0]
    x_end = x1[-1] if x1[-1] >= x2[-1] else x2[-1]
    X = x_end-x_start
    return np.linspace(x_start, (np.ceil(X/dx)+1)*dx, int(np.ceil(X/dx))+1)


def correlate(cls:  Type['Relation'], r1: 'Relation', r2: 'Relation') \
            -> BaseXY:
    '''Корреляция.

    Применяется функция numpy.correlate
    '''
    r1 = r1.shift(-r1._x[0])
    r2 = r2.shift(-r2._x[0])
    r1, r2 = cls.equalize(r1, r2)
    x, y1 = r1.get_data()
    _, y2 = r2.get_data()
    return BaseXY(np.append(np.sort(-1*x)[:-1], x), np.correlate(y1, y2, 'full'))


def convolve(cls: Type['Relation'], r1: 'Relation', r2: 'Relation') \
            -> BaseXY:
    '''Свертка.

    Применяется функция numpy.convlove
    '''
    r1 = r1.shift(-r1._x[0])
    r2 = r2.shift(-r2._x[0])
    r1, r2 = cls.equalize(r1, r2)
    x, y1 = r1.get_data()
    _, y2 = r2.get_data()
    return BaseXY(np.append(np.sort(-1*x)[:-1], x), np.convolve(y1, y2, 'full'))

#==============================================================================

def signal2spectrum(t: np.ndarray, a: np.ndarray, 
                        is_start_zero=False) -> BaseXY:
    '''Прямое преобразование фурье.'''
    
    if not is_start_zero:
        if t[0] > 0.:
            t = np.linspace(0., t[-1], int(t[-1]/(t[1]-t[0]))+1)
            a = np.append(np.zeros(t.size-a.size), a)
        elif t[-1] < 0.:
            t = np.linspace(t[0], 0., int(abs(t[0])/(t[1]-t[0]))+1)
            a = np.append(a, np.zeros(t.size-a.size))
        
        a = np.append(a[t>=0.], a[t<0.])
    
    s_a = np.fft.rfft(a)
    f = np.fft.rfftfreq(a.size, d=(t[-1]-t[0])/(a.size))
    return BaseXY(f, s_a)


def spectrum2sigmal(f: np.ndarray, s_a: np.ndarray, 
                    time: float = None) -> BaseXY:
    '''Обратное преобразование фурье.'''
    a = np.fft.irfft(s_a) # type: np.ndarray
    if time is None:
        t = np.linspace(0, (a.size-1)/(2*(f[-1]-f[0])), a.size)
    else:
        t = np.linspace(time, time+(a.size-1)/(2*(f[-1]-f[0])), a.size)
        a = np.append(a[t>=0.], a[t<0.])

    return BaseXY(t, a)
