"""
This module extends the `sweep_design.math_signals` module.

Repeats classes methods from the `sweep_design.math_signals` module and using 
composition of the math_signals classes. These methods have the same purposes.

Almost every repeating method has additional parameters: '**name**' 
and '**category**'.

How they will operate with each other is described by the 
`sweep_design.named_signals.header_signals` module.

The method used to create default names and categories is described in 
`sweep_design.named_signals.header_signals.defaults.names`

The configuration file `sweep_design.config.named_config` and 
`sweep_design.config.named_config.NamedConfig` contains important variables 
and methods that you can change.

You can also simply create a 
`sweep_design.named_signals.named_relation.NamedRelation` class from an 
instance of the `sweep_design.math_signals.math_relation.Relation` class by 
passing an instance of the `sweep_design.math_signals.math_relation.Relation` 
class to the constructor of the 
`sweep_design.named_signals.named_relation.NamedRelation` class. Also 
works for others.

The purpose of creating this module is to simplify the work with many 
examples of signals, spectra, sweeps and relations. Simplify their 
visualization, comparison and storage.

"""

from .named_relation import NamedRelation as NamedRelation
from .named_signal import NamedSignal as NamedSignal, NamedSpectrum
from .named_signal import NamedSpectrum as NamedSpectrum
from .named_sweep import NamedSweep as NamedSweep
from .named_uncalcsweep import NamedUncalcSweep as NamedUncalcSweep
from .named_uncalcsweep import NamedApriorUcalcSweep as NamedApriorUcalcSweep
