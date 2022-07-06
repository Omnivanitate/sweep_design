from typing import TypeVar

from ...math_relation import Relation

Signal = TypeVar('Signal', bound= Relation)

class Source:

    def __init__(self, mass: float, limit: float):
        self.mass = mass
        self.limit = limit
    
    def displacement(self, signal: Signal) -> Signal:
        return signal.integrate().integrate()/self.mass
    
    def force(self, displacement: Signal) ->  Signal:
        return displacement.diff().diff()*self.mass

    def bounds_of_displacement(self):
        pass