from typing import Callable, Optional, Union
import numpy as np

from ....math_signals.defaults.base_structures import MathOperation
from ..base_header import HeaderBase

Num = Union[float, int, complex]
InName = Union[HeaderBase, str, Callable[[], str]]


def make_default_names_operations(
    obj1: HeaderBase, obj2: Union[HeaderBase, Num], operation: MathOperation
) -> str:
    default_names_operations = {
        "__add__": "({0} + {1})",
        "__sub__": "({0} - {1})",
        "__mul__": "({0} * {1})",
        "__truediv__": "({0} / {1})",
        "__pow__": "({0} ** {1})",
        "__radd__": "({0} + {1})",
        "__rsub__": "({0} - {1})",
        "__rmul__": "({0} * {1})",
        "__rtruediv__": "({0} / {1})",
        "__rpow__": "({0}) ** {1})",
    }
    return default_names_operations[operation.value].format(obj1, obj2)


def make_default_name_select_data(obj: HeaderBase, x_start: Num, x_end: Num) -> str:
    return "{0} [{1}-{2}]".format(obj.name(), x_start, x_end)


def make_default_name_exp(obj: HeaderBase) -> str:
    return "exp({0})".format(obj.name())


def make_default_diff_name(obj: HeaderBase) -> str:
    return "diff({0})".format(obj.name())


def make_default_integrate_name(obj: HeaderBase) -> str:
    return "integrate({0})".format(obj.name())


def make_default_shift_name(obj: HeaderBase, x_shift: Num) -> str:
    return "Shift({0}) by {1}".format(obj.name(), x_shift)


def make_default_interpolate_name(obj: HeaderBase, new_x: np.ndarray) -> str:
    return "inerp({0} {1}-{2} dx:{3})".format(
        obj.name(), new_x[0], new_x[-1], new_x[1] - new_x[0]
    )


def make_default_name_correlation(obj1: HeaderBase, obj2: HeaderBase) -> str:
    return "(Corr({0} & {1}))".format(obj1._name(), obj2._name())


def make_default_name_convolution(obj1: HeaderBase, obj2: HeaderBase) -> str:
    return "(Conv({0} & {1}))".format(obj1, obj2)


def make_default_relation_name(name: int) -> str:
    return "R_{0}".format(name)


def make_diff_category_name(name: str) -> str:
    return "diff_{0}".format(name)


def make_integrate_category_name(name: str) -> str:
    return "integrate_{0}".format(name)


# ==============================================================================


def get_default_spectrum_name(obj: HeaderBase) -> str:
    return "{0}".format(obj)


def make_default_spectrum2signal_name(obj: HeaderBase) -> str:
    return "({0})toS".format(obj)


def make_default_signal2spectrum_name(obj: HeaderBase) -> str:
    return "({0})toSP".format(obj)


def make_default_spectrum_from_amp_phase_name(
    obj_amp: HeaderBase, obj_phase: HeaderBase
) -> str:
    return "SP(amp({0}) phase({1}))".format(obj_amp, obj_phase)


def make_default_spectrum_from_phase_name(obj_phase: HeaderBase) -> str:
    return "SP(phase({0}))".format(obj_phase)


def make_default_spectrum_from_amp_name(obj_amp: HeaderBase) -> str:
    return "SP(amp({0}))".format(obj_amp)


def make_default_name_reverse_filter(obj: HeaderBase) -> str:
    return "reverse filter ({0})".format(obj)


def make_default_name_reverse_signal(obj: HeaderBase) -> str:
    return "recerse signal ({0})".format(obj)


def make_default_add_phase_name(obj1: HeaderBase, obj2: HeaderBase) -> str:
    return "{0}+phase({1})".format(obj1, obj2)


def make_default_sub_phase_name(obj1: HeaderBase, obj2: HeaderBase) -> str:
    return "{0}-phase({1})".format(obj1, obj2)


def make_default_spectrum_name(name) -> str:
    return "SP_{0}".format(name)


def make_default_signal_name(name) -> str:
    return "S_{0}".format(name)


def make_default_phase_category_name(name) -> str:
    return "phase_{0}".format(name)


def make_default_amp_category_name(name) -> str:
    return "amp_{0}".format(name)


# #============================================================================


def default_sweep_name(name) -> str:
    return "SW_{0}".format(name)


def make_default_a_t_name(obj: HeaderBase) -> str:
    return "a_t({0})".format(obj)


def make_default_f_t_name(obj: HeaderBase) -> str:
    return "f_t({0})".format(obj)


def make_default_spectrogram_name(obj: HeaderBase) -> str:
    return "sp_f_t({0})".format(obj)


# ==============================================================================


def make_spectrogram_name(name) -> str:
    return "Spectrogram_{0}".format(name)


# ==============================================================================


def default_name_uncalc_sweep(name) -> str:
    return "USW_{0}".format(name)


def default_name_aprior_uncalc_sweep(name) -> str:
    return "AUSW_{0}".format(name)


def default_name_call_uncalc_sweep(dt: float, T: float, obj: HeaderBase) -> str:
    return "{0} dt: {1} T: {2}".format(obj, dt, T)
