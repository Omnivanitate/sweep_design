import numpy as np


class BlankViewRelation:

    def __init__(self, x, y, name, category):
        self._x = x
        self._y = y
        self.name = name
        self.category = category

    def __str__(self) -> str:
        return self.name
    
    def get_data(self):
        return self._x, self._y

class BlankViewSignal(BlankViewRelation):

    def __init__(self, x, y, name, category):
        super().__init__(x, y, name, category)
    
    def get_spectrum(self):
        return BlankViewSpectrum(np.array([1, 100]), np.array([1, 100]), name = 'spectum_from'+str(self), category='spectrum')


class BlankViewSpectrum(BlankViewRelation):
    
    def __init__(self, x, y, name, category):
        super().__init__(x, y, name, category)

    def get_amp_spectrum(self):
        return BlankViewRelation(self._x, self._y+10, name='amp'+str(self), category='amp_spectrum')
    
    def get_phase_spectrum(self):
        return BlankViewRelation(self._x, self._y-20, name='phase'+str(self), category='phase_spectrum')

    
class BlankViewSpectrogram:
    
    def __init__(self, t, f, S=None, category = 'f_t', name: str = 'spectrogram') -> None:
        self._name = name
        self.t = t
        self.f = f
       
        tt, ff = np.meshgrid(t, f)
        self.S = np.sin(tt)*np.cos(ff)
     
        self.category = category
    
    def __str__(self) -> str:
        return self._name

class BlankViewSweep(BlankViewSignal):

    def __init__(self, x, y, name, category):
        super().__init__(x, y, name, category)

    @property
    def f_t(self):
        return BlankViewRelation(self._x, self._y+100, 'f_t '+str(self), category='f_t')
    
    @property
    def a_t(self):
        return BlankViewRelation(self._x, self._y-100, 'a_t '+str(self), category='a_t')

    @property
    def spectrogram(self):
        f, _ = self.get_spectrum().get_data()
        return BlankViewSpectrogram(self._x, f)