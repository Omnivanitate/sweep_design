'''
This module extends the math_signal module.

Repeats classes methods from the `sweep_design.math_signals` module and using composition 
of the `math_signals classes`. These methods have the same purposes.

Almost every repeating method has additional parameters: 'name' and 'category'.

How they will operate with each other is described by the 
`sweep_design.named_signals.header_signals` module.

The method used to create default names and categories is described in 
`header_signals.defaults.names`

And the configuration file `named_config.py` (`sweep_design.config.sweep_config`) 
contains important variables and methods that you can change.

You can also simply create a `NamedRelation` class from an instance of 
the `Relation` class by passing an instance of the `Relation` class 
to the constructor of the `NamedRelation` class. Also works for others.

The purpose of creating this module is to simplify the work with many 
examples of signals, spectra, sweeps and relations. Simplify their 
visualization, comparison and storage.

'''

from .named_relation import NamedRelation as NamedRelation
from .named_signal import NamedSignal as NamedSignal, NamedSpectrum
from .named_signal import NamedSpectrum as NamedSpectrum
from .named_sweep import NamedSweep as NamedSweep
from .named_uncalcsweep import NamedUncalcSweep as NamedUncalcSweep
from .named_uncalcsweep import NamedApriorUcalcSweep as NamedApriorUcalcSweep
