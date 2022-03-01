import inspect
from typing import Optional, Tuple, Type, TypeVar, Union, Callable

import numpy as np

from math_signals.math_relation import Relation
from math_signals.defaults.base_structures import TypeFuncError
from header_signals.base_header import NamedBase
import header_signals.defaults.names as dfn
from header_signals.defaults.methods import make_name, make_category

Num = Union[float, int, complex]
InName = Union[NamedBase, str, Callable[[], str]]
NR = TypeVar('NR', bound='NamedRelation')

class BadNameCategory(Exception):
    pass

SET_VARNAME_AS_DEFAULT = True

class NamedRelation(NamedBase):
   
    _quantity = 1
    _make_default_name = dfn.make_default_relation_name

    def __init__(self, name: InName = None, 
                category: Optional[str] = 'relation', **kwargs) -> None:
        
        if name is None:
            if not SET_VARNAME_AS_DEFAULT:
                name = type(self)._make_default_name(NamedRelation._quantity)
                type(self)._quantity += 1
            else:
                name = NamedRelation._get_name_by_trace()
        if category is None:
            category = 'relation'

        super().__init__(name, category)
    
    @staticmethod
    def _get_name_by_trace():
        frames_callers = inspect.stack()
        for n, k in enumerate(frames_callers):
            if 'IPython' in k.filename:
                break
            name = frames_callers[n].frame.f_code.co_names[-1]
        return name

    @property
    def category(self) -> str:
        return self._category
    
    @category.setter
    def category(self, value) -> None:
        self._category = value
        
    @property
    def name(self) -> Callable[..., str]:
        return self._name
    
    @name.setter
    def name(self, value: InName) -> None:
        if callable(value) and isinstance(value(), str):
            self._name = value
        elif isinstance(value, NamedBase):
            self._name = value._name
        else:
            str(value)
            def call() -> str:
                return str(value)
            self._name = call

    def __str__(self) -> str:
        return self.name()
    
    def __repr__(self) -> str:
        return f'Name: {self.name()} category: {self.category}'
   
    def select_data(self, x_start: Num, x_end: Num,
            name: InName = None, 
            category='relation', **kwargs) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_name_select_data, 
                self, x_start, x_end)
        category = make_category(self, category)
        return NamedRelation(name, category, **kwargs)
    
    def exp(self, name: InName = None, 
                category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_name_exp, self)
        category = make_category(self, category)
        return NamedRelation(name, category)
    
    def diff(self, name: InName = None,
                category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_diff_name, self)
        category = make_category(self, category, dfn.make_diff_category_name)
        return NamedRelation(name, category)
    
    def integrate(self, name: InName = None, 
            category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_integrate_name, self)
        category = make_category(self, category, dfn.make_integrate_category_name)
        return NamedRelation(name, category)

    def interpolate_extrapolate(self, new_x: Union[np.ndarray, Relation], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        if isinstance(new_x, Relation):
            new_x, _ = new_x.get_data()
        name = make_name(name, dfn.make_default_interpolate_name, self, new_x)
        category = make_category(self, category)
        return NamedRelation(name, category)
    
    def shift(self, x_shift: Num, name: InName = None, 
                        category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_shift_name, self, x_shift)
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __add__(self, other: Union['NamedRelation', Num],
            name: InName = None, category: str = None) -> 'NamedRelation':
        
        name = make_name(name, dfn.make_default_names_operations, self, 
                            other, '__add__')
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __radd__(self, other: Union['NamedRelation', Num],
            name: InName = None, category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_names_operations, self, 
                            other, '__radd__')
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __sub__(self, other: Union['NamedRelation', Num], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_names_operations, self,
                            other, '__sub__')
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __rsub__(self, other: Union['NamedRelation', Num], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_names_operations, self, 
                            other, '__rsub__')
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __mul__(self, other: Union['NamedRelation', Num], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_names_operations, self, 
                            other, '__mul__')
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __rmul__(self, other: Union['NamedRelation', Num], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_names_operations, self, 
                            other, '__rmul__')
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __truediv__(self, other: Union['NamedRelation', Num], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_names_operations, self, 
                            other, '__truediv__')
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __rtruediv__(self, other: Union['NamedRelation', Num], 
            name: InName =  None, category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_names_operations, self, 
                            other, '__rtruediv__')
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __pow__(self, other: Union['NamedRelation', Num], 
            name: InName =  None, category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_names_operations, self, 
                            other, '__pow__')
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __rpow__(self, other: Union['NamedRelation', Num], 
            name: InName =  None, category: str = None) -> 'NamedRelation':
        name = make_name(name, dfn.make_default_names_operations, self, 
                            other, '__rpow__')
        category = make_category(self, category)
        return NamedRelation(name, category)

    def __iadd__(self, other: Union['NamedRelation', Num], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        return self.__add__(other, name, category)

    def __isub__(self, other: Union['NamedRelation', Num], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        return self.__sub__(other, name, category)

    def __imul__(self, other: Union['NamedRelation', Num], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        return self.__mul__(other, name, category)

    def __idiv__(self, other: Union['NamedRelation', Num], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        return self.__truediv__(other, name, category)

    def __ipow__(self, other: Union['NamedRelation', Num], 
            name: InName = None, category: str = None) -> 'NamedRelation':
        return self.__pow__(other, name, category)
    
    @staticmethod
    def equalize(
            r1: 'NamedRelation', r2: 'NamedRelation',
            new_x: Union[Relation, np.ndarray],
            name1: InName = None,
            name2: InName = None, 
            category1: str = None, 
            category2: str = None
            ) -> Tuple[NamedBase, NamedBase]:
        r1 = r1.interpolate_extrapolate(new_x, name1, category1)
        r2 = r2.interpolate_extrapolate(new_x, name2, category2)
        return r1, r2

    @classmethod
    def correlate(cls: Type['NamedRelation'], r1: 'NamedRelation', 
            r2: 'NamedRelation', name: InName = None, 
            category=None, **kwargs) -> 'NamedRelation':

        if isinstance(r1, NamedRelation) and isinstance(r2, NamedRelation):
            name = make_name(name, dfn.make_default_name_correlation, r1, r2)
            category = make_category(r1, category)
            return cls(name, category)
        else:
            raise TypeFuncError('Correlation', type(r1), type(r2))

    @classmethod
    def convolve(cls: Type['NamedRelation'], r1: 'NamedRelation', 
            r2: 'NamedRelation', name: InName = None, 
            category: str = None, **kwargs) -> 'NamedRelation':
        
        if isinstance(r1, NamedRelation) and isinstance(r2, NamedRelation):
            name = make_name(name, dfn.make_default_name_convolution, r1, r2)
            category = make_category(r1, category)
            return cls(name, category)
        else:
            raise TypeFuncError('Convolution', type(r1), type(r2))

