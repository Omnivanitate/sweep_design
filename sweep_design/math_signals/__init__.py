'''The core of representation of project.

- - - 

The basic unit is the `Relation` class 
(`sweep_design.math_signals.math_relation`). It describes the relationship between 
two sequences as a function of one variable *y = f(x)*. It introduces basic math 
operations (-, +, *, /, exponentiation(**)), derivation, integration, 
correlation, convolution, and other operations.

- - -

The next two classes are `Signal` and `Spectrum` 
(`sweep_design.math_signals.math_signal`), which inherit from the `Relation` class, 
are covered and can be obtained from the other through a transformation. 
The `Signal` class provides a method to get the instance of `Spectrum` class 
(the forward Fourier transformation is used by default). 
In the Spectrum class, the method for obtaining an instance of the Signal class 
(the inverse Fourier transform is used by default). 

The following methods are defined in the Spectrum class: 

* phase subtraction 
* phase addition 
* obtaining an inverse filter 
* amplitude spectrum acquisition
* phase spectrum acquisition
* static method for obtaining the spectrum from the amplitude and phase spectra

Methods are presented in the Signal class:

* obtaining a phase spectrum  
* obtaining an amplitude spectrum  
* obtaining an inverse signal  
* adding a phase  
* subtracting a phase  

They also have the same methods from the inherited Relation class.

- - -

The following `Sweep` class (`sweep_design.math_signals.math_sweep`) 
inherits from the `Signal` class. It does not have additional methods, but 
only contains the fields of frequency versus time (f_t), 
the amplitude envelope (a_t), the spectrogram (spectrogram) and 
the a priori signal (aprior_signal).

- - -

The `Sweep` class is the result of the `UncalculatedSweep` and 
`ApriorUncalculatedSweep` (`sweep_design.math_signals.math_uncalcsweep`) 
classes as a result of calling their instances.

The constructor of the `UncalculatedSweep` class receives as input time (time), 
a function of frequency change from time (f_t), and a function of 
amplitude envelope from time (a_t). And when calling an instance of the 
`UncalculatedSweep` class, you can get a sweep signal corresponding to the 
passed functions of changing the frequency from time and the amplitude 
envelope from time. Envelope functions with respect to time and frequency 
with respect to time can be represented as either sequences or 
functions (or callables).

The constructor of the `ApriorUncalculatedSweep` class accepts a priori data 
(an instance of the `Relation`, `Signal`, `Spectrum`, or `Sweep`, which will be 
cast to a `Spectrum` instance) and a method to extract from the `Spectrum` instance
functions of frequency versus time, amplitude envelope versus time, and a priori signal.

- - - 

The above classes use methods defined in configuration files and classes: 
`sweep_design.config.config` (`Config` class) 
and `sweep_design.config.sweep_config` (`SweepConfig` class).
The execution of methods in the above Classes can be changed by changing the 
methods in the configuration files, either by changing them or by importing 
configuration classes and changing their methods.

The default methods to use are defined in `sweep_design.math_signals.defaults.methods` 
and `sweep_design.math_signals.defaults.sweep_methods`

- - -

`utility_functions` defines useful functions such as:

> * Function get_IMFs_ceedman (`sweep_design.math_signals.utility_finctions.emd_analyse`)
to analyse a signal using Complete Ensemble Empirical Mode Decomposition with 
Adaptive Noise and return `NamedSignal` instances that contain Intrinsic 
Mode Functions (IMFs).

> * `get_time` (`sweep_design.math_signals.utility_finctions.time_axis`)
function to create time axis descrided by np.ndarray retruning reault
equal np.linspace. 

> * `tukey_a_t` (`sweep_design.math_signals.utility_finctions.tukey.`) 
function to build the envelope for sweep signal.

> * `f_t_linear_array` or `f_t_linear_function` to get the linear mean of the 
frequency-time function as function or array

> * simple_freq2time - function to get frequency versus time and amplitude versus time changes 
    from an a priori spectrum to create a sweep signal. **In this implementation, 
    the amplitude of change over time is a constant.** The spectrum of the 
    resulting sweep signal will be equal to the prior spectrum.

> * dwell - function to get frequency versus time and amplitude versus time changes 
    from an a priori spectrum to create a sweep signal. **In this 
    implementation, the amplitude of the envelope monotonously increases 
    in proportion to the change in frequency up to the cutoff frequency fc, 
    after which the amplitude of the envelope is constant.** The spectrum of the 
    resulting sweep signal will be equal to the prior spectrum.

> * correct_sweep_without_window - Using the EMD to subtract the last IMF from the displacement.  

> * correct_sweep - Using the EMD to subtract the last IMF from the displacement and apply 
    a window in the star so that the displacement starts at zero.

> * get_correction_for_source - Using correcte_sweep and applay 
    Use correct_sweep and then attenuate the displacement where it goes beyond 
    the threshold of limitations. It is necessary for the vibration source to 
    be able to realize the sweep signal.

To easy import, these functions have been moved to 
`sweep_design.utility_function`.

- - -

`sweep_design.math_signals.prepared_sweeps` contains various ready-made sweep signals. 
To create them, you need to call the appropriate functions with the necessary parameters.

Functions are defined to create the following sweep signals:

* Linear sweep (get_linear_sweep)
* Dwell sweep (get_dwell_sweep)
* Code Zinger (get_code_zinger)
* m - sequence ()
* shuffle (get_shuffle)

For convenience, you can import functions in the following way
```python
from sweep_design.prepared_sweeps import get_linear_sweep
```

'''

from .math_relation import Relation as Relation
from .math_signal import Spectrum as Spectrum
from .math_signal import Signal as Signal
from .math_sweep import Sweep as Sweep
from .math_uncalcsweep import UncalculatedSweep as UncalculatedSweep
from .math_uncalcsweep import ApriorUncalculatedSweep as ApriorUncalculatedSweep