"""The core of representation of project.

- - - 

The basic unit is the `sweep_design.math_signals.math_relation.Relation` class. 
It describes the relationship between two sequences as a function of one 
variable *y = f(x)*. It introduces basic math operations (-, +, *, /, 
exponentiation(**)), derivation, integration, 
correlation, convolution, and other operations.

- - -

The next two classes are `sweep_design.math_signals.math_signal.Signal` and 
`sweep_design.math_signals.math_signal.Spectrum`, which inherit from the 
`sweep_design.math_signals.math_relation.Relation` class, are covered 
and can be obtained from the other through a transformation. 
The `sweep_design.math_signals.math_signal.Signal` class provides a method 
to get the instance of `sweep_design.math_signals.math_signal.Spectrum` class 
(the forward Fourier transformation is used by default). 
In the `sweep_design.math_signals.math_signal.Spectrum` class, the method for 
obtaining an instance of the `sweep_design.math_signals.math_signal.Signal` class 
(the inverse Fourier transform is used by default). 

The following methods are defined in the 
`sweep_design.math_signals.math_signal.Spectrum` class: 

* phase subtraction 
* phase addition 
* obtaining an inverse filter 
* amplitude spectrum acquisition
* phase spectrum acquisition
* static method for obtaining the spectrum from the amplitude and phase spectra

Methods are presented in the `sweep_design.math_signals.math_signal.Signal` 
class:

* obtaining a phase spectrum  
* obtaining an amplitude spectrum  
* obtaining an inverse signal  
* adding a phase  
* subtracting a phase  

They also have the same methods from the inherited 
`sweep_design.math_signals.math_relation.Relation` class.

- - -

The following `sweep_design.math_signals.math_sweep.Sweep` class
inherits from the `sweep_design.math_signals.math_signal.Signal` class. 
It does not have additional methods, but only contains the fields of frequency 
versus time (**frequency_time**), the amplitude envelope (**amplitude_time**), 
the spectrogram (**spectrogram**) and the a priori signal (**aprior_signal**).

- - -

The `sweep_design.math_signals.math_sweep.Sweep` class is the result of 
the `sweep_design.math_signals.math_uncalcsweep.UncalculatedSweep` 
or `sweep_design.math_signals.math_uncalcsweep.ApriorUncalculatedSweep` 
classes as a result of calling their instances.

The constructor of the 
`sweep_design.math_signals.math_uncalcsweep.UncalculatedSweep` class receives 
as input time (**time**), a function of frequency change from time 
(**frequency_time**), and a function of amplitude envelope from time 
(**amplitude_time**). And when calling an instance of the 
`sweep_design.math_signals.math_uncalcsweep.UncalculatedSweep` class, 
you can get a sweep signal corresponding to the passed functions of changing 
the frequency from time and the amplitude envelope from time. 
Envelope functions with conform to time and frequency with conform to 
time can be represented as either sequences or functions (or callables).

The constructor of the 
`sweep_design.math_signals.math_uncalcsweep.ApriorUncalculatedSweep` class 
accepts **apriori_data** (an instance of the 
`sweep_design.math_signals.math_relation.Relation`, 
`sweep_design.math_signals.math_signal.Signal`, 
`sweep_design.math_signals.math_signal.Spectrum`, 
or `sweep_design.math_signals.math_sweep.Sweep`, which will be cast to a 
`sweep_design.math_signals.math_signal.Spectrum` instance) and a method to 
extract from the `sweep_design.math_signals.math_signal.Spectrum` 
instance functions of frequency versus time, amplitude envelope versus time, 
and a priori signal.

- - - 

The above classes use methods defined in configuration files and classes: 
`sweep_design.config.config.Config` class and
`sweep_design.config.sweep_config.SweepConfig`.
The execution of methods in the above Classes can be changed by changing the 
methods in the configuration files, either by changing them or by importing 
configuration classes and changing their methods.

The default methods to use are defined in 
`sweep_design.math_signals.defaults.methods` 
and `sweep_design.math_signals.defaults.sweep_methods`

- - -

`utility_functions` defines useful functions such as:

> * Function `sweep_design.math_signals.utility_functions.emd_analyse.get_IMFs_emd`
to analyse a signal using Empirical Mode Decomposition and contains instances that 
contain Intrinsic Mode Functions (IMFs).

> * Function `sweep_design.math_signals.utility_functions.emd_analyse.get_IMFs_ceemdan`
to analyse a signal using Complete Ensemble Empirical Mode Decomposition with 
Adaptive Noise and return `NamedSignal` instances that contain Intrinsic 
Mode Functions (IMFs).

> * `sweep_design.math_signals.utility_functions.time_axis.get_time`
function to create time axis descrided by np.ndarray retruning reault
equal np.linspace. 

> * `sweep_design.math_signals.utility_functions.tukey.tukey_a_t` 
function to build the envelope for sweep signal.

> * `sweep_design.math_signals.utility_functions.linear_f_t.f_t_linear_array` or 
`sweep_design.math_signals.utility_functions.linear_f_t.f_t_linear_function` 
to get the linear mean of the frequency-time function as function or array

> * `sweep_design.math_signals.utility_functions.ftat_functions.simple_freq2time`
function to get frequency versus time and amplitude 
versus time changes from an a priori spectrum to create a sweep signal. 
**In this implementation, the amplitude of change over time is a 
constant.** The spectrum of the resulting sweep signal will be equal to 
the prior spectrum.

> * `sweep_design.math_signals.utility_functions.ftat_functions.dwell` - 
function to get frequency versus time and amplitude versus time 
changes from an a priori spectrum to create a sweep signal. **In this 
implementation, the amplitude of the envelope monotonously increases 
in proportion to the change in frequency up to the cutoff frequency fc, 
after which the amplitude of the envelope is constant.** The spectrum 
of the resulting sweep signal will be equal to the prior spectrum.

> * `sweep_design.math_signals.utility_functions.sweep_correction.correct_sweep_without_window` - 
Using the EMD to extract the first IMF from the displacement.  

> * `sweep_design.math_signals.utility_functions.sweep_correction.correct_sweep` - 
Using the EMD to extract the first IMF from the displacement and apply a 
window in the star so that the displacement starts at zero.

> * `sweep_design.math_signals.utility_functions.sweep_correction_source.get_correction_for_source` - 
Sweep signal correction for realization on the vibration source.

For convenience, you can import functions in the following way
```python
from sweep_design.math_signals.utility_functions import get_time
```

- - -

Module `sweep_design.math_signals.prepared_sweeps` contains various ready-made sweep 
signals. To create them, you need to call the appropriate functions with 
the necessary parameters.

Functions are defined to create the following sweep signals:

* Linear sweep 
(`sweep_design.math_signals.prepared_sweeps.linear_sweep.get_linear_sweep`)
* Dwell sweep 
(`sweep_design.math_signals.prepared_sweeps.dwell_sweep.get_dwell_sweep`)
* Code Zinger 
(`sweep_design.math_signals.prepared_sweeps.code_zinger.get_code_zinger`)
* m - sequence 
(`sweep_design.math_signals.prepared_sweeps.m_sequence.get_m_sequence`)
* shuffle 
(`sweep_design.math_signals.prepared_sweeps.pseudorandom_shuffle.get_shuffle`)

For convenience, you can import functions in the following way
```python
from sweep_design.math_signals.prepared_sweeps import get_linear_sweep
```

"""

from .math_relation import Relation as Relation
from .math_signal import Spectrum as Spectrum
from .math_signal import Signal as Signal
from .math_sweep import Sweep as Sweep
from .math_uncalcsweep import UncalculatedSweep as UncalculatedSweep
from .math_uncalcsweep import ApriorUncalculatedSweep as ApriorUncalculatedSweep
