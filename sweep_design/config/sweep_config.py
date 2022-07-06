from ..math_signals.defaults import sweep_methods as dfsm


class SweepConfig:

    """The configuratuin file for sweep.

    > Several methods are defined for default calculations:

    **spectrogram_method_default**
    > The method by which the spectrogram will be calculated.
    > Method derived from default function:
    >> sweep_disign.math_signals.defaults.sweep_methods.get_spectrogram()

    > input:
    >> time: np.ndarray
       amplitude: np.ndarry

    > output:
    >> Tuple [
    >> time: np.ndarray,
    >> frequency: np.ndarray,
    >> spectrogram: np.ndarray
    ]

    - - -

    **get_f_t**
    > The method by which frequency versus time will be calculated.
    > Method derived from default function:
    >> sweep_disign.math_signals.defaults.sweep_methods.get_f_t

    > input:
    >> time: np.ndarray
    amplitude: np.ndarray

    > output:
    >> Relation

    - - -

    **get_a_t**
    > The method by which the time envelope of the signal will be calculated.
    > Method derived from default function:
    >> sweep_disign.math_signals.defaults.sweep_methods.get_a_t

    > input:
    >> time: np.ndarray
    amplitude: np.ndarray

    > output:
    >> Relation

    - - -

    **integrate_function**
    > A method for integrating a function rather than a sequence.
    Method derived from default function:
    >> sweep_disign.math_signals.defaults.sweep_methods.integrate_quad

    > input:
    >> f_t_function: Callable[[time: np.ndarray], frequency: np.ndarray]
    time: np.ndarray

    > output:
    >> y: np.ndarray

    - - -

    **freq2time**
    > The simple method to extract the time envelope of a sweep signal and
    the time-frequency function to generate a sweep signal from a priori data.
    Method derived from default function:
    >> sweep_disign.math_signals.defaults.sweep_methods.simple_freq2time

    > input:
    >> spectrum: Spectrum

    > output:
    >> Tuple [
    >> time : np.ndarray,
        frequency : np.ndarray,
        envelope : np.ndarray
        ]

    - - -

    The above methods can be overridden with your own here, or you can import the
    class SweepConfig somewhere and override it there.
     (They must be written according to the rules corresponding to
     the input and output parameters)
    """

    # Methods for Sweep.
    spectrogram_method = dfsm.get_spectrogram()
    get_f_t = dfsm.get_f_t
    get_a_t = dfsm.get_a_t

    # Methods for UncalculatedSweep.
    integrate_function = dfsm.integrate_quad

    # Method for ApriorUncalculatedSweep.
    freq2time = dfsm.simple_freq2time
