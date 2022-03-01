import logging
from typing import Any, Tuple, Union, Type, TypeVar

import numpy as np

from math_signals.defaults import methods as dfm
from math_signals.defaults.base_structures import BadInputError, TypeFuncError, BaseXY, RelationProtocol

Num = Union[float, int, complex]
R = TypeVar('R', bound='Relation')
R2 = TypeVar('R2', bound='Relation')

class Relation:
    '''Представление зависимости y и x (y = f(x)) в точках.

    Объект описывает зависимость между двумя последовательностями x, y, 
    представленные чилсами(простыми или комплексными). Длины числовых 
    последовательностей должны быть равны, и шаг дискретизации должен быть 
    одинаковый.  

    Параметры:
        ---------
        x: Any
            Объект Relation, или наследумый от него объект, или
            сущность, из которой будет извелечен объект array_like 
            (или извленчены объекты array_like), 
            содержащий(ие) только числа (простые и(или) комплексные).

        y: Any
            None или сущность, из которого будет извелечен объект 
            array_like, содержащий только числа (простые и(или) 
            комплексные).

    Определены несколько статических методов для вычислений:
        ---------------------
        extract_input_method_default:
            Статический метод для извлечения данных из параметров x и y
            Метод полученный из функции по умолчанию: 
                sweep_analysis.math_signals.defaults.methods.extract_input
            input:
                x: Any
                y: Any
            output:
                BaseXY
                
        interpolate_extrapolate_method_default:
            Статический метод, по которому выполнятся интерполяция и 
            экстраполяция.
            Метод полученный из функции по умолчанию: 
                sweep_analysis.math_signals.defaults.methods.interpolate_extrapolate
            input:
                r1: Relation
                r2: Relation
            output:
                Callable[[np.ndarray], np.ndarray]
            
        math_operation_method_default:
            Статический метод, по которому выполнятся базовые арифметические 
            операции: сложение (+), вычитание(-), умножение(*), деление(/), 
            возведние в степень (**) и их унарные операции. 
            Метод полученный из функции по умолчанию: 
                sweep_analysis.math_signals.defaults.methods.operation
            input:
                x: np.ndarray
                y1: np.ndarray
                y2: np.ndarray | Number
                name_operation: str
                (name_operation может быть из списка:
                '__add__', '__sub__', '__mul__', '__truediv__', '__pow__',
                '__radd__', '__rsub__', '__rmul__', '__rtruediv__', '__rpow__')
            output:
                BaseXY
            
        integrate_one_method_default:
            Статический метод для расчета интеграла последовантельности на 
            отрезке.
            Метод полученный из функции по умолчанию:
                sweep_analysis.math_signals.defaults.methods.one_integrate
            input:
                x: np.ndarray
                y: np.ndarray
            output:
                float
            
        integrate_method_default:
            Статический метод, по которому выполняется интегрирование.
            Метод полученный из функции по умолчанию: 
                sweep_analysis.math_signals.defaults.methods.integrate
            input:
                x: np.ndarray
                y: np.ndarray
            output:
                BaseXY
            
        differentiate_method_default:
            Статический метод, по которому выполнятся дифференцирование.
            Метод полученный из функции по умолчанию:
                sweep_analysis.math_signals.defaults.methods.differentiation
            input:
                x: np.ndarray
                y: np.ndarray
            output:
                BaseXY
            
        correlate_method_default:
            Статический метод, по которому выполнятся корреляция
            Метод полученный из функции по умолчанию:
                sweep_analysis.math_signals.defaults.methods.correlate
            input:
                cls: Relation
                r1: Relation
                r2: Relation
            output:
                BaseXY
           
        convolve_method_default:
            Статический метод, по которому выполнятся свертка
            Метод полученный из функции по умолчанию:
                sweep_analysis.math_signals.defaults.methods.convolve
            input:
                cls: Relation
                r1: Relation
                r2: Relation
            output:
                BaseXY
        
        get_common_x_default:
            Статичесекий метод, по которому выполняется нахождение 
            общей последовательности чисел по оси х, полученной из двух 
            других последовательностей по оси х.
            Метод полученный из функции по умолчанию:
                sweep_analysis.math_signals.defaults.methods.get_common_x
            input:
                x1: np.ndarray
                x2: np.ndarray
            output:
                np.ndarray

    Выше перечисленные методы по умолчанию можно переопределить своими.
    (Они должны быть написаны по правилам, соответствующие входным и выходным 
    параметрам)
    
    Для класс Relation определены базавые арифметические опперации: 
    сложение (+), вычитание(-), умножение(*), деление(/), возведние в 
    степень (**), унарное сложение (+=), унарное вычитание (-=), 
    унарное умножение (*=), унарное деление (/=)
    Результатом операций является новый экземпляр класса Realation.

    Если нельзя выполнить свертку, или корреляцию, 
    то возникнет исключение TypeFuncError

    ВЫЖНО!!! При наслодовании класса Relation важно правильно написать 
    конструктор. Он должен соответствовать конструктору класса Relation.
    Так как некоторые методы возращают объект Relation(...). Например, 
    метод сложения (def __add__(self: R, other: Union['Relation', Num]) 
    -> R). Либо преопределить данные методы в наследуемом классе. 

    '''

    interpolate_extrapolate_method_default = staticmethod(dfm.interpolate_extrapolate)
    math_operation_default = staticmethod(dfm.math_operation)
    integrate_one_method_default = staticmethod(dfm.one_integrate)
    integrate_method_default = staticmethod(dfm.integrate)
    differentiate_method_default = staticmethod(dfm.differentiate)
    correlate_method_default = staticmethod(dfm.correlate)
    convolve_method_default = staticmethod(dfm.convolve)
    get_common_x_default = staticmethod(dfm.get_common_x) 
    
    def __init__(self, x: Union[RelationProtocol, np.ndarray], y: np.ndarray = None, **kwargs) -> None:

        if isinstance(x, RelationProtocol):
            self._x, self._y = x.get_data()
            if y is not None:
                logging.warning('x is instance of Relation, "y" was ignored')
        else:
            if y is None:
                raise BadInputError('y absent. Not enough data!')
            self._x, self._y = x, y
    
    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        '''Return the data of the called object.'''
        return self._x.copy(), self._y.copy()
    
    def max(self) -> Num:
            return self._y.max()

    def min(self) -> Num:
        return self._y.min()

    def get_norm(self) -> float:
        '''Получить норму сигнала.

        Расчитывается через энергию сигнала.
        '''
        x, y = self._x, self._y
        return self.integrate_one_method_default(y**2, x)/(x[1]-x[0])

    def select_data(
            self: R, x_start: Num = None, x_end: Num = None , **kwargs
            ) -> R:
        x, y = self.get_data()
        
        if x_start is None:
            x_start = x[0]
        
        if x_end is None:
            x_end = x[-1]
        
        is_selected = np.logical_and(np.greater_equal(
            self._x, x_start), np.less_equal(self._x, x_end))

        return type(self)(
            x[is_selected], y[is_selected], **kwargs 
            )

    def exp(self: R, **kwargs) -> R:
        x, y = self.get_data()
        return type(self)(x, np.exp(y), **kwargs)

    def diff(self: R, **kwargs) -> R:
        x, y = self.get_data()
        result = self.differentiate_method_default(x, y)
        return type(self)(*result, **kwargs)

    def integrate(self: R, **kwargs) -> R:
        x, y = self.get_data()
        result = self.integrate_method_default(x, y)  
        return type(self)(*result, **kwargs)

    def interpolate_extrapolate(self: R, new_x: np.ndarray, **kwargs) -> R:
        new_y = self.interpolate_extrapolate_method_default(self._x, self._y)(new_x)
        return type(self)(new_x, new_y, **kwargs)
    
    def shift(self: R, x_shift: Num = 0, **kwargs) -> R:
        x, y = self.get_data()
        return type(self)(x+x_shift, y, **kwargs)

    @staticmethod
    def _operation(a: 'Relation', b: Union['Relation',  Num],
                  name_operation: str) -> BaseXY:
        logging.debug(f'Type of a: {type(a)}')
        logging.debug(f'Type of b: {type(b)}')
        if isinstance(b, Relation):
            r1, r2 = Relation.equalize(a, b)
            x, y1 = r1.get_data()
            _, y2 = r2.get_data()
            return a.math_operation_default(x, y1, y2, name_operation)
        elif isinstance(b, (float, int, complex)):
            x, y = a.get_data()
            return a.math_operation_default(x, y, b, name_operation)
        else:
            raise TypeFuncError(name_operation.strip('_'), type(a), type(b))


    def __add__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return type(self)(*self._operation(self, 
                other, '__add__'), **kwargs)

    def __radd__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return type(self)(*self._operation(self, 
            other, '__radd__'), **kwargs)

    def __sub__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return type(self)(*self._operation(self, 
            other, '__sub__'), **kwargs)

    def __rsub__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return type(self)(*self._operation(self, 
            other, '__rsub__'), **kwargs)

    def __mul__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return type(self)(*self._operation(self, 
            other, '__mul__'), **kwargs)

    def __rmul__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return type(self)(*self._operation(self, 
            other, '__rmul__'), **kwargs)

    def __truediv__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return type(self)(*self._operation(self, 
            other, '__truediv__'), **kwargs)

    def __rtruediv__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return type(self)(*self._operation(self, 
            other, '__rtruediv__'), **kwargs)

    def __pow__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return type(self)(*self._operation(self, 
            other, '__pow__'), **kwargs)

    def __rpow__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return type(self)(*self._operation(self, 
            other, '__rpow__'), **kwargs)

    def __iadd__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return self.__add__(other, **kwargs)

    def __isub__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return self.__sub__(other, **kwargs)

    def __imul__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return self.__mul__(other, **kwargs)

    def __idiv__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return self.__truediv__(other, **kwargs)

    def __ipow__(self: R, other: Union['Relation', Num], **kwargs) -> R:
        return self.__pow__(other, **kwargs)

    def __len__(self) -> int:
        return self._x.size
    
    @staticmethod
    def equalize(r1: R, r2: R2) -> Tuple[R, R2]:
        x1, _ = r1.get_data()
        x2, _ = r2.get_data()
        comparation = x1==x2
        if isinstance(comparation, np.ndarray):
            if all(comparation):
                return r1, r2
        x_new = Relation.get_common_x_default(x1, x2)
        r1 = r1.interpolate_extrapolate(x_new)
        r2 = r2.interpolate_extrapolate(x_new)
        return r1, r2

    @classmethod
    def correlate(cls: Type[R], r1: 'Relation', r2: 'Relation', **kwargs) -> R:

        if isinstance(r1, Relation) and isinstance(r2, Relation):
            result = Relation.correlate_method_default(cls, r1, r2)
            return cls(*result, **kwargs)
        else:
            raise TypeFuncError('Correlation', type(r1), type(r2))

    @classmethod
    def convolve(cls: Type[R], r1: 'Relation', r2: 'Relation', **kwargs) -> R:
        
        if isinstance(r1, Relation) and isinstance(r2, Relation):
            result = Relation.convolve_method_default(cls, r1, r2)
            return cls(*result, **kwargs)
        else:
            raise TypeFuncError('Convolution', type(r1), type(r2))
