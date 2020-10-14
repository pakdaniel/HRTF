import numpy as np
from math import ceil

def time_series(Sxy,dt):
    N = len(Sxy)
    shift_amount = 1-ceil(N/2)
    Sxy = np.roll(Sxy, shift_amount)

    time_series = np.fft.ifft(Sxy,dt)
    time_series = np.roll(time_series,shift_amount)

    t_range = np.arange(0,N)*dt
    t_range = t_range - (ceil(N/2)-1)*dt

    return(time_series,t_range)