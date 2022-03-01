from typing import Any, Callable, Optional, Tuple, Type, Union, TypeVar

import numpy as np

from compose_signals.defaults.methods import extract_input
from header_signals.base_header import NamedBase
from math_signals.math_relation import  Relation
from header_signals.relation_header import NamedRelation
from math_signals.defaults.base_structures import TypeFuncError
from math_signals.defaults.base_structures import BaseXY

Num = Union[float, int, complex]
CR = TypeVar('CR', bound='ComposedRelation')
CR2 = TypeVar('CR2', bound='ComposedRelation')
InName = Union[NamedBase, str, Callable[[], str]]
InData = Union[CR, Relation]
Any = Union[InData, Num]
T = TypeVar('T')

default_name_composed_relation = 'DR'

class ComposedRelation:
    
    extract_input_default = staticmethod(extract_input)

    def __init__(self, x: Any, y: Any = None, name: InName = None, category: str = None) -> None:

        x, y = self.extract_input_default(x, y)        

        if category is None:
            category = 'relation'
        
        self.relation = Relation(x, y)
        self.header = NamedRelation(name, category)        

    @property
    def category(self):
        return self.header.category

    @classmethod
    def _convert_input(cls: Type[CR], data: Any, name: InName = None) -> 'ComposedRelation':
        if not isinstance(data, ComposedRelation):
            if not name:
                name = default_name_composed_relation
            return ComposedRelation(cls.extract_input_default(data, None), name=name)
        return data

    def _operate(self: CR, other: Any, operation: str, 
            name: Optional[InName], category: Optional[str], 
            ) -> CR:

        if not isinstance(other, (ComposedRelation, float, int, complex)):
            other = self._convert_input(other)

        relation = getattr(self.relation, operation)(other)
        header = getattr(self.header, operation)(other, name, category)
        return type(self)(relation, name=header)

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.relation.get_data()
        
    def select_data(self: CR, x_start: Num = None, x_end: Num = None, 
        name: InName = None, category: str = None) -> CR:
         
        if x_start is None:
            x_start = self.relation._x[0]
    
        if x_end is None:
            x_end = self.relation._x[-1]

        header = self.header.select_data(x_start, x_end, name, 
                                                    category)
        relation = self.relation.select_data(x_start, x_end)
        return type(self)(relation, name = header)
        
    def exp(self: CR, name: InName = None, category='c_relation') -> CR:
        header = self.header.exp(name, category) 
        relation = self.relation.exp()
        return type(self)(relation, name = header)

    def diff(self: CR, name: InName = None, category='c_relation') -> CR:
        header = self.header.diff(name, category)
        relation = self.relation.diff()
        return type(self)(relation, name = header)
    
    def integrate(self: CR, name: InName = None, 
                            category='c_relation') -> CR:
        header = self.header.integrate(name, category)  
        relation = self.relation.integrate()
        return type(self)(relation, name = header)

    def interpolate_extrapolate(self: CR, new_x, name: InName = None, 
                                category='c_relation') -> CR:
        header = self.header.interpolate_extrapolate(new_x, name, category)  
        relation = self.relation.interpolate_extrapolate(new_x)
        return type(self)(relation, name=header)
    
    def shift(self: CR, x_shift: Num = 0., name: InName = None, 
                                category='c_relation') -> CR:
        header = self.header.shift(x_shift, name, category)
        relation = self.relation.shift(x_shift)
        return type(self)(relation, name=header)

    def __str__(self) -> str:
        return str(self.header)

    def __add__(self: CR, other: Any, name: InName = None, 
                                category='c_relation') -> CR:
        return self._operate(other, '__add__', name, category)
        
    def __radd__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self._operate(other, '__radd__', name, category)
    
    def __sub__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self._operate(other, '__sub__', name, category)
    
    def __rsub__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self._operate(other, '__rsub__', name, category)

    def __mul__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self._operate(other, '__mul__', name, category)

    def __rmul__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self._operate(other, '__rmul__', name, category)

    def __truediv__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self._operate(other, '__truediv__', name, category)
    
    def __rtruediv__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self._operate(other, '__rtruediv__', name, category)

    def __pow__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self._operate(other, '__pow__', name, category)

    def __rpow__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self._operate(other, '__rpow__', name, category)

    def __iadd__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self.__add__(other, name, category)
   
    def __isub__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self.__sub__(other, name, category)

    def __imul__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self.__mul__(other, name, category)
    
    def __idiv__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self.__truediv__(other, name, category)
    
    def __ipow__(self: CR, other: Any, name: InName = None,
                                category='c_relation') -> CR:
        return self.__pow__(other, name, category)

    @classmethod
    def equalize(cls: Type[CR], cr1: Any, cr2: Any, name1: InName = None, 
            name2: InName = None, category1: str = None,
            category2: str = None) -> Tuple[CR, CR2]: 
        cr1 = cls._convert_input(cr1)
        cr2 = cls._convert_input(cr2)
        r1, r2 = Relation.equalize(cr1.relation, cr2.relation)
        header1, header2 = NamedRelation.equalize(cr1.header, cr2.header, r1,
                                                    name1, name2, category1, category2)
        return type(cr1)(r1, name=header1), type(cr2)(r2, name=header2)

    @classmethod
    def convolve(cls: Type[CR], cr1: Any, cr2: Any, name: InName = None, 
            category: str = 'c_relation') -> CR:
        cr1 = cls._convert_input(cr1)
        cr2 = cls._convert_input(cr2)
        relation = Relation.convolve(cr1.relation, cr2.relation)
        header = NamedRelation.convolve(cr1.header, cr2.header, name, category)
        return cls(relation, name=header)    
            
           
    @classmethod
    def correlate(cls: Type[CR], cr1: Any, cr2: Any, name: InName = None, 
            category: str = 'c_relation') -> CR:
        cr1 = cls._convert_input(cr1)
        cr2 = cls._convert_input(cr2)
        named = NamedRelation.convolve(cr1.header, cr2.header, name, category)
        relation = Relation.correlate(cr1.relation, cr2.relation) 
        return cls(relation, name=named)
            
