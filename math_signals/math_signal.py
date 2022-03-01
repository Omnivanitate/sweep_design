from typing import  Optional, TypeVar, Union, Any, Type

import numpy as np

from math_signals.math_relation import Relation
import math_signals.defaults.methods as dfm
from math_signals.defaults.base_structures import ConvertingError


Num = Union[float, int, complex]
R = TypeVar('R', bound=Relation)
SP = TypeVar('SP', bound='Spectrum')
S = TypeVar('S', bound='Signal')
SPRN = Union['Spectrum', 'Relation', Num]
SSPR = Union['Spectrum', 'Signal', 'Relation']
SSPRN = Union['Spectrum', 'Signal', 'Relation', Num]


def input2spectrum_operation(inp: SSPRN) -> Union['Relation', 'Spectrum', Num]:
    if isinstance(inp, Signal):
        return inp.get_spectrum()
    elif isinstance(inp, (Spectrum, Relation, int, float, complex)):
        return inp
    else:
        raise ConvertingError(type(inp), Spectrum)
     
def input2spectrum(inp: SSPR) -> 'Spectrum':
    if isinstance(inp, Signal):
        return inp.get_spectrum()
    
    elif isinstance(inp, Spectrum):
        return inp
    
    elif isinstance(inp, Relation):
            return Spectrum(inp)  
    else:
        raise ConvertingError(type(inp), Spectrum)

class Spectrum(Relation):
    '''Класс описывающий какой-либо спектр сигнала.
    
    Класс Spectrum наследует класс Realtion

    Параметры
    ---------
    t: any
        Объект Relation, или наследумый от него объект, или
        сущность, из которой будет извелечен объект array_like 
        (или извленчены объекты array_like), 
        содержащий(ие) только числа (простые и(или) комплексные).

    A: any
        None или сущность, из которого будет извелечен объект 
        array_like, содержащий только числа (простые и(или) 
        комплексные).
    
    is_require_signal: Bool
        Параметр указывает нужноли для экземпляра класса создавать сигнал. 
        По умолчанию True.

        Если параметр is_require_signal истенен, то при создание экземпляра 
        класса расчитывается сигнал последовательности, который передается 
        конструктору класса Signal, для которого задан параметр 
        is_require_spectrum = False. Созданный экземпляр класса присваевается 
        атрибуту signal.

    time: float. По умолчанию None.
        Параметр указывает на то, с какого времени следует вести отсчет.
        
    Определен статический метода преобразования из частотной 
    области во временную:
        spectrum2signal_method_default
        Метод полученный из функции по умолчанию: 
            sweep_analysis.math_signals.defaults.methods.spectrum2sigmal
        input:
            f: np.ndarray
            s_a: np.ndarray
            start_time: float. По умолчанию None.
        output:
            BaseXY
    
    При выполнении арифметических операций с экземплярами класса Signal, 
    из экземпляра Signal будет извлечен экземплар класса Spectrum,
    и с этим экземпляром будут выполняться ариметические операции. 
    '''

    spectrum2signal_method_default = staticmethod(dfm.spectrum2sigmal)

    def __init__(self, f: Union[Relation, np.ndarray], 
                            sA: np.ndarray = None, **kwargs) -> None:
        super().__init__(f, sA)
        self.signal: Optional[Signal] = None
        

      
    def get_signal(self, recalculate=False, start_time: float = None) -> 'Signal':
        '''Расчитывется сигнал из cпектра.'''
        if self.signal is None or recalculate:
            t, A = self._spectrum2signal_method_default(self._x, self._y, start_time)
            self.signal = Signal(t, A)
        return self.signal
    
    def get_amp_spectrum(self: R, **kwargs) -> 'Relation':
        '''Расчитывается связь частоты и абсолютного занчения амплитуды спектра.'''
        x, y = self.get_data()
        return Relation(x, np.abs(y))

    def get_phase_spectrum(self: R, **kwargs) -> 'Relation':
        '''Расчитывается связь частоты и фазы спектра.'''
        x, y = self.get_data()
        return Relation(x, np.unwrap(np.angle(y)))

    def get_reverse_filter(self: SP, percent: Union[float, int] = 5.,
                           subtrack_phase=True,  
                           f_start: float = None, 
                           f_end: float = None, **kwargs) -> SP:
        '''Расчет фильтра обратного сигнала.

        Параметры:
        ---------
            percent: Union[float, int] 
                уровень добовляемого белого шума
            
            subtrack_phase: True
                Если True выполняет, вычитание фазы,
                False выполняет, добавление фазы.

            f_start: float.
                Начальная частота.

            f_end: float
                Конечная частота.

        '''
        spectrum = self.select_data(f_start, f_end)
        abs_spectrum = spectrum.get_amp_spectrum()
        abs_spectrum = (abs_spectrum+abs_spectrum.max()*percent/100)
        reversed_abs_spectrum = 1/abs_spectrum

        if subtrack_phase:
            phase_spectrum = -1*spectrum.get_phase_spectrum()
        else:
            phase_spectrum = 1*spectrum.get_phase_spectrum()

        result_spectrum = type(self).get_spectrum_from_amp_phase(
            reversed_abs_spectrum, phase_spectrum, **kwargs)
        return result_spectrum
   
    def add_phase(self: SP, other: SSPR, **kwargs) -> SP:
        sp_other = input2spectrum(other)
        return type(self).get_spectrum_from_amp_phase(
            self.get_amp_spectrum(),
            self.get_phase_spectrum()+\
            sp_other.get_phase_spectrum(),
            **kwargs
            )
        
    def sub_phase(self: SP, other: SSPR, **kwargs) -> SP:
        sp_other = input2spectrum(other)
        return type(self).get_spectrum_from_amp_phase(
            self.get_amp_spectrum(),
            self.get_phase_spectrum() -\
            sp_other.get_phase_spectrum(),
            **kwargs
            )

    @classmethod
    def get_spectrum_from_amp_phase(cls: Type[SP], s1: Relation, 
            s2: Relation, **kwargs) -> SP:
        '''Расчёт спектра из амплитудного и частотного спектра.
        
        Спектр расчитывается через амплитудный и фазовый спектр 
        по формуле abs*exp(1j*phase).'''
        
        return cls(s1*((1.j*s2).exp()), **kwargs)
    
    @classmethod
    def convolve(cls: Type[SP], r1: SSPR, r2: SSPR, **kwargs) -> SP:
        sp_r1 = input2spectrum(r1)
        sp_r2 = input2spectrum(r2)
        return super().convolve(sp_r1, sp_r2, **kwargs)
    
    @classmethod
    def correlate(cls: Type[SP], r1: SSPR, r2: SSPR, **kwargs) -> SP:
        sp_r1 = input2spectrum(r1)
        sp_r2 = input2spectrum(r2)
        return super().correlate(sp_r1, sp_r2, **kwargs)
    
    def __add__(self: SP, a: SSPRN, **kwargs) -> SP:
        r_a = input2spectrum_operation(a)
        return super().__add__(r_a, **kwargs)

    def __sub__(self: SP, a: SSPRN, **kwargs) -> SP:
        r_a = input2spectrum_operation(a)
        return super().__sub__(r_a, **kwargs)

    def __mul__(self: SP, a: SSPRN, **kwargs) -> SP:
        r_a = input2spectrum_operation(a)
        return super().__mul__(r_a, **kwargs)

    def __truediv__(self: SP, a: SSPRN, **kwargs) -> SP:
        r_a = input2spectrum_operation(a)
        return super().__truediv__(r_a, **kwargs)
 
    def __pow__(self: SP, a: SSPRN, **kwargs) -> SP:
        r_a = input2spectrum_operation(a)
        return super().__pow__(r_a, **kwargs)


def inp2signal_operation(inp: SSPRN) -> Union['Relation', 'Signal', Num]:
    if isinstance(inp, Spectrum):
        return inp.get_signal()
    elif isinstance(inp, (Signal, Relation, int, complex, float)):
        return inp
    else:
        raise ConvertingError(type(inp), Signal)

def inp2signal(inp: SSPR) -> 'Signal':
    if isinstance(inp, Spectrum):
        return inp.get_signal()

    elif isinstance(inp, Signal):
        return inp

    elif isinstance(inp, Relation):
        return Signal(inp)
    else:
        raise ConvertingError(type(inp), Signal)
        

class Signal(Relation):
    ''' Класс описывающий какой-либо сигнал.

    Класс Signal наследует класс Realtion.

    Параметры:
        ---------
        t: any
            Объект Relation, или наследумый от него объект, или
            сущность, из которой будет извелечен объект array_like 
            (или извленчены объекты array_like), содержащий(ие) только 
            числа (простые и(или) комплексные).

        A: any
            None или сущность, из которого будет извелечен объект 
            array_like, содержащий только числа (простые и(или) 
            комплексные).

        is_require_signal: Bool
            Параметр указывает нужноли для экземпляра класса создавать спектр. 
            По умолчанию True.

            Если параметр is_require_signal истенен, то при создание экземпляра 
            класса расчитывается спектр последовательности, который передается 
            конструктору класса Spectrum, для которого задан параметр 
            is_require_signal = False. Созданный экземпляр класса присваевается 
            атрибуту spectrum.
        
        is_start_zero: Bool. По по умолчанию False.
            Параметр указывает на то, что при вычислении преобразования Фурье,
            рассматривать последовательность изменений амплитуды с нулевого
            времени. 
    
    Определен статический метода преобразования из временой 
    области в частотную:
        signal2spectrum_method_default
        Метод полученный из функции по умолчанию: 
            sweep_analysis.math_signals.defaults.methods.spectrum2sigmal
        input:
            t: np.ndarray
            a: np.ndarray
            is_start_zero. По умолчанию False.
         output:
            BaseXY

    При выполнении арифметических операций с экземплярами класса Spectrum, 
    из экземпляра Spectrum будет извлечен экземплар класса Signal,
    и с этим экземпляром будут выполняться ариметические операции. 
    '''

    signal2spectrum_method_default = staticmethod(dfm.signal2spectrum)

    def __init__(self, t: Union[Relation, np.ndarray], A: np.ndarray = None, **kwargs) -> None:
     
        super().__init__(t, A)
        self._spectrum: Optional[Spectrum] = None
    
    
    def get_spectrum(self, recalculate=False, is_start_zero=False) -> 'Spectrum':

        if self._spectrum is None or recalculate:
            f, A = self.signal2spectrum_method_default(*self.get_data(), is_start_zero)
            self._spectrum = Spectrum(f, A)

        return self._spectrum
            
    def get_reverse_signal(self: S, percent: Union[float, int] = 5.,
                           subtrack_phase: bool = True, 
                           f_start: float = None, 
                           f_end: float = None,
                           **kwargs) -> S:
        '''Расчет обратного сигнала.

        Параметры:
        ---------
           percent: Union[float, int]
              уровень добовляемого белого шума

            subtrack_phase: True
              Если True выполняет, вычитание фазы,
               False выполняет, добавление фазы.

            f_start: float.
              Начальная частота.

            f_end: float
              Конечная частота.

        '''
        signal =  self.get_spectrum().\
            get_reverse_filter(percent, subtrack_phase, f_start, f_end).\
                get_signal()
        
        return type(self)(signal, **kwargs)

    def add_phase(self: S, other: SSPR, **kwargs) -> S:
        sp_other = input2spectrum(other)
        self_spectrum = self.get_spectrum()
        new_spectrum = Spectrum.get_spectrum_from_amp_phase(
            self_spectrum.get_amp_spectrum(),
            self_spectrum.get_phase_spectrum()+\
                sp_other.get_phase_spectrum()
            )
        return type(self)(new_spectrum.get_signal(), **kwargs)

    def sub_phase(self: S, other: SSPR, **kwargs) -> S:
        sp_other = input2spectrum(other)
        self_spectrum = self.get_spectrum()
        new_spectrum = Spectrum.get_spectrum_from_amp_phase(
            self_spectrum.get_amp_spectrum(),
            self_spectrum.get_phase_spectrum()-\
                sp_other.get_phase_spectrum()
            )
        return type(self)(new_spectrum.get_signal(), **kwargs)

    @classmethod
    def convolve(cls: Type[S], r1: SSPR, r2: SSPR, **kwargs) -> S:
        s_r1 = inp2signal(r1)
        s_r2 = inp2signal(r2)
        return cls(super().convolve(s_r1, s_r2), **kwargs)

    @classmethod
    def correlate(cls: Type[S], r1: SSPR, r2: SSPR, **kwargs) -> S:
        s_r1 = inp2signal(r1)
        s_r2 = inp2signal(r2)
        return cls(super().correlate(s_r1, s_r2), **kwargs)

    def __add__(self: S, a: SSPRN, **kwargs) -> S:
        s_a = inp2signal_operation(a)
        return super().__add__(s_a, **kwargs)

    def __sub__(self: S, a: SSPRN, **kwargs) -> S:
        s_a = inp2signal_operation(a)
        return super().__sub__(s_a, **kwargs)

    def __mul__(self: S, a: SSPRN, **kwargs) -> S:
        s_a = inp2signal_operation(a)
        return super().__mul__(s_a, **kwargs)

    def __truediv__(self: S, a: SSPRN, **kwargs) -> S:
        s_a = inp2signal_operation(a)
        return super().__truediv__(s_a, **kwargs)

    def __pow__(self: S, a: SSPRN, **kwargs) -> S:
        s_a = inp2signal_operation(a)
        return super().__pow__(s_a, **kwargs)
