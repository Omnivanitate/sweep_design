from pathlib import Path
from ..math_signals.defaults import methods as dfm


class Config:
    """The configuratuin file.

    The methods used to calculate the various parameters are provided in the
    configuration file. Also the file contain an other parameters.
    -----------------------------------------------------------------------

    **DEFAULT_PATH** - This is the path using to write and read data.
    This directory defaults to the current working derectiory, from where
    functions are called.

    - - -

    **CONVERT2ARRAY** - If parameter is True, then converted input array to np.ndarray
    in the constructor of class Relation.

    - - -

    **interpolate_extrapolate_method**:
    > The method by which interpolation and extrapolation are performed.
    > The methods returns a function that takes a new x sequence and
    return a new y sequence.

    > new_x = np.ndarray
    > new_y = np.ndarray

    > Method derived from default function:
    >> sweep_design.math_signals.defaults.methods.interpolate_extrapolate

    > input:
    >> x: np.ndarray
    >> y: np.ndarray

    > output:
    >> Callable[[new_x], new_y]

    - - -

    **math_operation_method**:
    > The method of basic mathematical operations of addition (+),
    subtraction(-), multiplication (*), division(/), exponentiation (**)
    and their unary operations (+=, -=, *=, /=).

    > Method derived from default function:
    >> sweep_design.math_signals.defaults.methods.operation

    > input:
    >> x: np.ndarray
    >> y1: np.ndarray
    >> y2: Union[np.ndarray, float, int, complex]
    >> name_operation: sweep_design.math_signals.defaults.base_structures.MathOperation

    > output:
    >> Tuple [
    >> x: np.ndarray,
    >> y: np.ndarray
    >>]

    - - -

    **integrate_one_method**:
    > Method for calculating the integral of a sequence on a segment.
    > Method derived from default function:
    >> sweep_design.math_signals.defaults.methods.one_integrate

    > input:
    >> x: np.ndarray
    >> y: np.ndarray

    > output:
    >> float

    - - -

    **integrate_method**:
    > The method by which the integration is performed.
    > Method derived from default function:
    >>sweep_design.math_signals.defaults.methods.integrate

    > input:
    >> x: np.ndarray
    >> y: np.ndarray

    > output:
    >> Tuple [
        x: np.ndarray,
        y: np.ndarray
    ]

    - - -

    **differentiate_method**:
    > The method by which differentiation is performed.
    > Method derived from default function:
    >> sweep_design.math_signals.defaults.methods.differentiation

    > input:
    >> x: np.ndarray
    >> y: np.ndarray

    > output:
    >>Tuple [
        x: np.ndarray,
        y: np.ndarray
    ]

    - - -

    **correlate_method**:
    > The method by which the correlation is performed
    > Method derived from default function:
    >> sweep_design.math_signals.defaults.methods.correlate

    > input:
    >> cls: Relation
    >> r1: Relation
    >> r2: Relation

    > output:
    >> Tuple [
        x: np.ndarray,
        y: np.ndarray
    ]

    - - -

    **convolve_method**:
    > The method by which the convolution is performed
    > Method derived from default function:
    >> sweep_design.math_signals.defaults.methods.convolve

    > input:
    >> cls: Relation
    >> r1: Relation
    >> r2: Relation

    > output:
    >> Tuple [
        x: np.ndarray,
        y: np.ndarray
    ]

    - - -

    **get_common_x**:
    > A method by which to find the common sequence of numbers along
    > the x-axis, obtained from two other sequences along the x-axis.
    > Method derived from default function:
    >> sweep_design.math_signals.defaults.methods.get_common_x

    > input:
    >> x1: np.ndarray
    >> x2: np.ndarray

    > output:
    >> x: np.ndarray

    - - -

    **spectrum2signal_method**:
    > Method for converting a spectrum into a signal. (Using Fourier transform)
    > Method derived from default function:
    >> sweep_design.math_signals.defaults.methods.spectrum2sigmal

    > input:
    >> frequenc: np.ndarray
    specturm: np.ndarray
    start_time: float = None

    > output:
    >> Tuple [
        time: np.ndarray,
        amplitude: np.ndarray
    ]

    - - -

    **signal2spectrum_method**:
    > Method for converting a signal into a spectrum. (Using Fourier transform)
    > Method derived from default function:
    >> sweep_design.math_signals.defaults.methods.spectrum2sigmal

    > input:
    >> time: np.ndarray
    >> amplitude: np.ndarray
    >> is_start_zero = False

    > output:
    >> Tuple [
        frequency: np.ndarray,
        spectrum: np.ndarray
    ]

    - - -

    The above methods can be overridden with your own here, or you can import the
    class Config somewhere and override it there.
    (They must be written according to the rules corresponding to
    the input and output parameters)

    """

    # Path for io_data module
    DEFAULT_PATH = Path(".")

    # Conver array for Relation.
    CONVERT2ARRAY = True

    # Methods for the Relation.
    interpolate_extrapolate_method = dfm.interpolate_extrapolate
    math_operation = dfm.math_operation
    integrate_one_method = dfm.one_integrate
    integrate_method = dfm.integrate
    differentiate_method = dfm.differentiate
    correlate_method = dfm.correlate
    convolve_method = dfm.convolve
    get_common_x = dfm.get_common_x

    # Methods for Spectrum and Signal.
    spectrum2signal_method = dfm.spectrum2sigmal
    signal2spectrum_method = dfm.signal2spectrum
