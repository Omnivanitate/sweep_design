from typing import Callable, Union, TypeVar, Optional

import header_signals.defaults.names as dfn
from header_signals.base_header import NamedBase
from header_signals.relation_header import NamedRelation
from header_signals.defaults.methods import make_name, make_category

InName = Union[NamedBase, str, Callable[[], str]]
NSP = TypeVar('NSP', bound='NamedSpectrum')

class NamedSpectrum(NamedRelation):
    
    _quantity = 1

    def __init__(self, name: InName = None, category: str = None) -> None:
        
        if category is None:
            category = 'spectrum'
             
        if name is None:
            name = dfn.make_default_spectrum_name(NamedSpectrum._quantity)
            NamedSpectrum._quantity += 1

        super().__init__(name, category)
    
    def get_signal(self, name: InName = None, 
                            category: str = None) -> 'NamedSignal':
        name = make_name(name, dfn.make_default_spectrum2signal_name, self)
        return NamedSignal(name, category)

    def get_amp_spectrum(self, name: InName = None, 
                            category: str = None) -> 'NamedSpectrum':
        name = make_name(name, dfn.get_default_spectrum_name, self)
        category = make_category(self, category, dfn.make_default_amp_category_name)
        return NamedSpectrum(name, category)
    
    def get_phase_spectrum(self, name: InName = None, 
                            category: str = None) -> 'NamedSpectrum':
        name = make_name(name, dfn.get_default_spectrum_name, self)
        category = make_category(self, category, dfn.make_default_phase_category_name)
        return NamedSpectrum(name, category)

    def get_reverse_filter(self, name: InName = None,
                            category: str = None) -> 'NamedSpectrum':
        name = make_name(name, dfn.make_default_name_reverse_filter, self)
        category = make_category(self, category)
        return NamedSpectrum(name, category)
    
    def add_phase(self, other: NamedBase, name: InName = None, 
                            category: str = None) -> 'NamedSpectrum':
        name = make_name(name, dfn.make_default_add_phase_name, self, other)
        category = make_category(self, category)
        return NamedSpectrum(name, category)
    
    def sub_phase(self, other: NamedBase, name: InName = None,
                            category: str = None) -> 'NamedSpectrum':
        name = make_name(name, dfn.make_default_sub_phase_name, self, other)
        category = make_category(self, category)
        return NamedSpectrum(name, category)
    
    @staticmethod
    def get_spectrum_from_amp_phase(amp: NamedBase, phase: NamedBase, 
            name:  InName = None, category = 'spectrum') -> 'NamedSpectrum':
        name = make_name(name, 
            dfn.make_default_spectrum_from_amp_phase_name, amp, phase)
        return NamedSpectrum(name, category)

    
class NamedSignal(NamedRelation):

    _quantity = 1
    _make_default_name = dfn.make_default_signal_name

    def __init__(self, name: InName = None, 
                        category: str = None) -> None:
        
        if category is None:
            category = 'signal'

        super().__init__(name, category)
    
    def get_spectrum(self, name: InName = None, 
                                category='spectrum') -> 'NamedSpectrum':
        name = make_name(name, dfn.make_default_signal2spectrum_name, self)
        category = make_category(self, category)
        return NamedSpectrum(name, category)
    
    def get_reverse_signal(self, name: InName = None, 
                                category: str = None) -> 'NamedSignal':
        name = make_name(name, dfn.make_default_name_reverse_signal, self)
        category = make_category(self, category)
        return NamedSignal(name, category)
    
    def add_phase(self, other: NamedBase, name: InName = None, 
                                category: str = None) -> 'NamedSignal':
        name = make_name(name, dfn.make_default_add_phase_name, self, other)
        category = make_category(self, category)
        return NamedSignal(name, category)

    def sub_phase(self, other: NamedBase, name: InName = None, 
                                category: str = None) -> 'NamedSignal':
        name = make_name(name, dfn.make_default_sub_phase_name, self, other)
        category = make_category(self, category)
        return NamedSignal(name, category)
