"""The project is intended for designing sweep signals.

> The package is written in `Python` for creating and developing sweep signals 
of varying complexity. It contains not only tools for creation, but also 
tools for analysis, visualization and other purposes. It can be used both for 
educational and production purposes.  

> It is convenient to use `Jupyter Lab` or `Jupyter Notebook` to speed up the 
development of signals, to compare their parameters with other signals, and 
to visualize them. To visualize graphs, the project contains packages 
corresponding to these tasks. (In code editors or IDEs such as `vscode`, 
rendering of images, graphs may not be correct. It's better to use 
`Jupyter Lab` directly.)  

> The project is designed so that you can easily change the creation of sweep 
signals. For example, write your own methods describing how the frequency 
and amplitude will change from the time of the sweep signal.  

> The project was created to be able to produce various sweep signals: 
implemented and not implemented by a vibration source, from simple ones, like a 
linear sweep signal, to complex ones, like a pseudo-random sweep signal.  

- - -
## Install.

> You can install the library using `pip install sweep_design`, or you can 
clone or load it from GitHub, add path to the module and install requremnt 
packages using the `poetry install` or `pip install -r requirement.txt`, 
or coping pieces of code and create your own.

- - -
## Using the library.

The library consists of five sub-modules.

* `sweep_design.config` - contains the project configuration.
* `sweep_design.dataio` - contains simple functions for loading and saving 
data. For a difficult situation, write your own.
* `sweep_design.math_signals` - There is the core of project. Here is the basic 
concept of creating signals, specectra and sweep-signals realising. 
* `sweep_design.named_signals` - There is a representation of the created 
`math_signals` object. For simplicity, each represented object from 
`named_signals` has an additional field like name and category. This is 
convenient when you work with many signals, spectra and you don't to get 
confused.
* `sweep_design.view` - There is a sub-module for visualasing results. 
Contains a few `GUI` for `jupyter notebook`.

- - -
For convenient you can directly import a few objects from modules 
`sweep_design`, such as 
```python
from sweep_design import Relation
```
instead
```python
from sweep_design.math_signals.math_relation import Relation
```
But both variants are correct.
"""

from .math_signals import Relation as Relation
from .math_signals import Signal as Signal
from .math_signals import Spectrum as Spectrum
from .math_signals import Sweep as Sweep
from .math_signals import UncalculatedSweep as UncalculatedSweep
from .math_signals import ApriorUncalculatedSweep as ApriorUncalculatedSweep

from .named_signals import NamedRelation as NamedRelation
from .named_signals import NamedSignal as NamedSignal
from .named_signals import NamedSpectrum as NamedSpectrum
from .named_signals import NamedSweep as NamedSweep
from .named_signals import NamedUncalcSweep as NamedUncalcSweep
from .named_signals import NamedApriorUcalcSweep as NamedApriorUcalcSweep
