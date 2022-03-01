import logging
from typing import Callable
import unittest

import numpy as np
from scipy import signal

from math_signals.defaults.base_structures import Spectrogram
from math_signals.math_relation import Relation, DefaultMethod
from math_signals.math_signal import Spectrum, Signal
from math_signals.math_sweep import Sweep, UncalculatedSweep
from functions.func_f_t import dwell
from test.test_relation import PreTestRelation
from test.test_signal import PreTestSignal

log = logging.getLogger()
log.setLevel(logging.INFO)


def pre_get_spectrogramm() -> Callable[[np.ndarray, np.ndarray], Spectrogram]:
    def extract(x: np.ndarray, y: np.ndarray) -> Spectrogram:
        log.debug('In getter spectrogram')
        t = x, 
        f = y, 
        S = 1
        return Spectrogram(f=f, t=t, S=S, category='f_t') 
    return extract

def get_ricker(points, a=4.):
   return signal.ricker(points, a)


Sweep.spectrogram_method = DefaultMethod(pre_get_spectrogramm())

class TestUncalculatedSweep(unittest.TestCase):
    
    def test_input_data(self):
        
        dt = 0.001
        t = np.linspace(0.,10., int(10./dt)+1)

        a_t_array  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13]
        a_t_Relation = Relation(x=t, y=t)
        def a_t_func(t):
            return t*2

        f_t_array = [1, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        f_t_Relation = Relation(x=t, y=t*10)
        def f_t_func(t):
            return t**2
        
        ts = np.linspace(0., 1., int(1./dt)+1)
        aprior_signal = Signal(ts, get_ricker(ts.size))
        aprior_spectr = aprior_signal.get_spectrum()
        _, aprior_spectr_raw = aprior_spectr.get_data()
        abs_aprior_spectr = aprior_spectr.get_amp_spectrum() 

        l_a_t = [a_t_array, a_t_Relation, a_t_func, None]
        l_f_t = [f_t_array, f_t_Relation, f_t_func, None]
        l_apr = [aprior_signal, aprior_spectr, abs_aprior_spectr, None]

        for t_k in [t]:
            for a_t_k in l_a_t:
                for f_t_k in l_f_t:
                    for apr_k in l_apr:
                        for k_start in [None, 0.25]:
                            for k_end in [None, 9.]:
                                with self.subTest(t_k=t_k, a_t_k=a_t_k, 
                                    f_t_k=f_t_k, apr_k=apr_k, k_start=k_start,
                                    k_end=k_end):

                                    result = UncalculatedSweep(t=t_k, f_t=f_t_k, 
                                    a_t=a_t_k, aprior_data=apr_k, 
                                    x_start=k_start, x_end=k_end, 
                                    f_a_t_method=dwell(fc=10))
                                    self.assertIsInstance(result, UncalculatedSweep)

                                    sweep = result(t_k)
                                    self.assertIsInstance(sweep, Sweep)

                                    sweep2 = result()
                                    self.assertIsInstance(sweep2, Sweep)



class TestSweep(unittest.TestCase):

    pre_relation = PreTestRelation
    pre_signal = PreTestSignal
    
    def test_input(self):
        self.pre_relation.pre_test_input(self, Sweep)

    def test_math(self):
        self.pre_relation.pre_test_math(self, Sweep)
        self.pre_signal.pre_test_math(self, Sweep)

    def test_integrate_diff(self):
        self.pre_relation.pre_test_integrate_diff(self, Sweep)
    
    def test_interpolate_extrapolate(self):
        self.pre_relation.pre_test_interpolate_extrapolate(self, Sweep)
    
    def test_names(self):
        self.pre_relation.pre_test_names(self, Sweep, 'SW_')
       

    def test_convolve_correlate(self):
        s1 = Sweep([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
        sp1 = s1.get_spectrum()
        s2 = Sweep([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
        sp2 = s2.get_spectrum()

        l = [s1, sp1, s2, sp2]

        for k in l:
            for k2 in l:
                self.subTest(k=k, k2=k2)
                self.pre_relation.pre_test_convolve_correlate(
                    self, k, k2, Sweep)


