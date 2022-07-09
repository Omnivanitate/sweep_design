import unittest

from ..math_relation import Relation
from ..math_signal import Signal, Spectrum
from .test_relation import PreTestRelation


class PreTestSignal:
    @staticmethod
    def pre_test_get_specrum(test_case: unittest.TestCase, signal_class: Signal):
        s = signal_class([0, 1, 2, 3, 4, 5], [0, 10, 20, 30, 40, 50])  # type: Signal
        sp = s.get_spectrum()
        test_case.assertIsInstance(sp, Spectrum)

    @staticmethod
    def pre_test_get_reverse(test_case: unittest.TestCase, signal_class: Signal):
        s = signal_class([0, 1, 2, 3, 4, 5], [0, 10, 20, 30, 40, 50])  # type: Signal

        rs = s.get_reverse_signal()
        test_case.assertIsInstance(rs, signal_class)

    @staticmethod
    def pre_test_math(test_case: unittest.TestCase, signal_class: Signal):
        s = signal_class([0, 1, 2, 3, 4, 5], [1, 2, 4, 6, 8, 10])  # type: Signal
        sp = s.get_spectrum()

        operation = ["__add__", "__sub__", "__mul__", "__truediv__", "__pow__"]
        for k in [s, sp]:
            for k2 in [s, sp]:
                for m in operation:
                    with test_case.subTest(k=k, k2=k2, m=m):
                        if isinstance(k2, Spectrum) and m in ["__truediv__"]:
                            continue
                        result = k.__getattribute__(m)(k2)
                        test_case.assertIsInstance(result, type(k))


class PreTestSpectrum:
    @staticmethod
    def pre_test_spectrum(test_case: unittest.TestCase, spectrum_class: Spectrum):

        sp = spectrum_class([0, 1, 2, 3, 4, 5], [1, 2, 4, 6, 8, 10])  # type: Spectrum

        amp = sp.get_amp_spectrum()
        test_case.assertIsInstance(amp, Relation)
        phase = sp.get_phase_spectrum()
        test_case.assertIsInstance(phase, Relation)
        s = sp.get_signal()
        test_case.assertIsInstance(s, Signal)
        rsp = sp.get_reverse_filter()
        test_case.assertIsInstance(rsp, spectrum_class)

        r1 = Relation([0, 1, 2, 3, 4, 5], [1, 2, 4, 6, 8, 10])
        r2 = Relation([0, 1, 2, 3, 4, 5], [1, 2, 4, 6, 8, 10])

        new_sp = spectrum_class.get_spectrum_from_amp_phase(r1, r2)
        test_case.assertIsInstance(new_sp, spectrum_class)


class TestSignalSpectrum(unittest.TestCase):
    pre_relation = PreTestRelation
    pre_signal = PreTestSignal
    pre_spectrum = PreTestSpectrum

    def test_input(self):
        self.pre_relation.pre_test_input(self, Signal)
        self.pre_relation.pre_test_input(self, Spectrum)

    def test_math(self):
        self.pre_relation.pre_test_math(self, Signal)
        self.pre_relation.pre_test_math(self, Spectrum)
        self.pre_signal.pre_test_math(self, Signal)

    def test_integrate_diff(self):
        self.pre_relation.pre_test_integrate_diff(self, Signal)
        self.pre_relation.pre_test_integrate_diff(self, Spectrum)

    def test_interpolate_extrapolate(self):
        self.pre_relation.pre_test_interpolate_extrapolate(self, Signal)
        self.pre_relation.pre_test_interpolate_extrapolate(self, Spectrum)

    def test_convolve_correlate(self):
        s1 = Signal([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
        sp1 = s1.get_spectrum()
        s2 = Signal([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
        sp2 = s2.get_spectrum()

        l = [s1, sp1, s2, sp2]

        for k in l:
            for k2 in l:
                for m in [Signal, Spectrum]:
                    self.subTest(k=k, k2=k2, m=m)
                    self.pre_relation.pre_test_convolve_correlate(self, k, k2, m)

    def test_spectrum(self):
        self.pre_spectrum.pre_test_spectrum(self, Spectrum)
