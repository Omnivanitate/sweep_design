from typing import Any, Union

import numpy as np
from numpy.typing import NDArray
from ..config.sweep_config import SweepConfig

from .math_relation import Relation
from .math_signal import Signal

from .defaults.base_structures import Spectrogram


class Sweep(Signal):
    """Class `Sweep`.

    A class for analyzing changes in a signal over time, inherited from
    the `Signal` class.

    For analysis, you can use not only the sweep signal, but also other
    signals for which the spectrogram needs to be considered.

    When creating an instance of the class, the spectrogram is calculated.
    The method used to calculate the spectrogram is defined in the
    `SweepConfig` class. You can override it with your own.

    If the frequency vs. time and amplitude vs. time functions have not
    been passed, they are also calculated, the `get_frequency_time`,
    `get_amplitude_time` methods defined in the `SweepConfig` class are used.

    Perform the same operations as for the inherited class.

    **Properties**:
    > **time**: `Union[RelationProtocol, NDArray]`
    The Relation class, or a class derived from the Relation class, or
    an array_like object containing numbers(real or complex).

    > **amplitude**: `NDArray` = `None`
    `None` or array_like object containing real or complex numbers.

    > **frequency_time**: `Relation` = `None`
    This parameter describes the change in frequency versus time of the
    transmitted signal.

    > **amplitude_time**: `Relation` = `None`
    This parameter describes the change in amplitude envelop of signal
    from the time of the transmitted signal.

    > **aprior_signal**: `Signal` = `None`
    The signal used to create the sweep signal.

    """

    def __init__(
        self,
        time: Union[Relation, NDArray],
        amplitude: NDArray = None,
        frequency_time: Relation = None,
        amplitude_time: Relation = None,
        aprior_signal: Signal = None,
    ) -> None:

        super().__init__(time, amplitude)

        self.frequency_time = (
            frequency_time
            if frequency_time is not None
            else SweepConfig.get_f_t(self.x, self.y)
        )
        self.amplitude_time = (
            amplitude_time
            if amplitude_time is not None
            else SweepConfig.get_a_t(self.x, self.y)
        )

        spectrogram = SweepConfig.spectrogram_method(self.x, self.y, self.dx)
        self.spectrogram = Spectrogram(
            time=spectrogram[0],
            frequency=spectrogram[1],
            spectrogram_matrix=spectrogram[2],
        )
        self.aprior_signal = aprior_signal
