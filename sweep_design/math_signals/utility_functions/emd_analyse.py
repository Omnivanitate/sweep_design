from typing import Any, List

from PyEMD import CEEMDAN, EMD
from ..math_signal import Signal


def get_IMFs_ceemdan(
    data: Signal,
    number_seedman=30,
    epsilon=0.005,
    ext_EMD: Any = None,
    parallel=False,
    processes=None,
    noise_scale=1,
    noise_kind="normal",
    range_thr=0.01,
    total_power_thr=0.05,
) -> List[Signal]:
    """Empirical mode decomposition (EMD).

    Using CEEMDAN from PyEMD (https://pyemd.readthedocs.io/) to calulate IMFs
    and return them as a list of Signals.

    About empirical mode decomposition on
    https://en.wikipedia.org/wiki/Hilbert%E2%80%93Huang_transform#Techniques
    """
    x, y = data.get_data()
    emd = CEEMDAN(
        number_seedman,
        epsilon,
        ext_EMD,
        parallel,
        processes=processes,
        noise_scale=noise_scale,
        noise_kind=noise_kind,
        range_thr=range_thr,
        total_power_thr=total_power_thr,
    )
    IMFs = emd(y)
    result = [Signal(x, k) for k in IMFs]
    return result


def get_IMFs_emd(data: Signal) -> List[Signal]:

    x, y = data.get_data()
    emd = EMD()
    IMFs = emd(y)
    result = [Signal(x, k) for k in IMFs]
    return result
