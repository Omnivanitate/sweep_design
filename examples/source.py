
from scipy.io import savemat
import numpy as np


from math_signals.math_relation import Relation
from math_signals.math_sweep import Sweep


from PyEMD import CEEMDAN, EMD

class Source:

    def __init__(self, mass: float, limit: float):
        self.mass = mass
        self.limit = limit
    
    def displacement(self, signal: Relation) -> Relation:
        return signal.integrate().integrate()*self.mass
    
    def force(self, displacement: Relation) ->  Relation:
        return displacement.diff().diff()*self.mass

    def correcte_sweep(self, signal: Relation, start_window: float) -> Relation:
        displacement = signal.integrate().integrate()
        x, y = displacement.get_data()
        emd = CEEMDAN(25, parallel=True, processes=2)
        IMFs = emd(y)
        
        x_w = np.linspace(0, start_window, int(start_window/(x[1]-x[0])))
        y_w = np.sin(np.pi/2*x_w/x_w.max())
        sin_corrections = np.append(y_w, np.ones(y.size-y_w.size))
        new_y = IMFs[0]*sin_corrections
        new_displacement = Sweep(x, new_y)
        
        signal = new_displacement.diff().diff()
        
        
        return signal

    def correcte_sweep_without_norm(self, signal: Relation) -> Relation:
        displacement = signal.integrate().integrate()
        x, y = displacement.get_data()
        emd = CEEMDAN(25, parallel=True, processes=2)
        IMFs = emd(y)
        new_displacement = Sweep(x, IMFs[0])
        signal = new_displacement.diff().diff()
        return signal
    
    @staticmethod
    def save_mat(file_name: str, signal: Relation) -> None:
        x, y = signal.get_data()
        data = {'t': x, 'F': y}
        savemat(file_name, data)