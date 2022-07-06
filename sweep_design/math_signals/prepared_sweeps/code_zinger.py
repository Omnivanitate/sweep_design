from pyrsistent import s
from ..math_relation import Relation
from ..math_sweep import Sweep
import numpy as np

def get_code_zinger(segment_sweep: Sweep, code_zinger = [-1, -1, -1, 1], period = 1):
    '''Repeat the transmitted signal according to the Zniger code for n periods (n times).
    
    '''

    new_sweep = segment_sweep()*code_zinger[0]

    # for cnt, v in enumerate(code_zinger[1:]):
    #     new_sweep = new_sweep+segment_sweep.shift(cnt*segment_sweep.t_end+cnt+segment_sweep.dt)    
    
    

    # dt = time_sweep[1] -time_sweep[0]
    # # time = get_time(0, sequence.size-1, dt)
    # full_code_zinger = Relation(time, sequence)
    # segment_sweep = Relation.convolve(full_code_zinger, segment_sweep)

    # sweep = segment_sweep

    # for k in range(period-1):
    #     sweep += segment_sweep.shift(k*segment_sweep.x[-1]+dt)


    return new_sweep