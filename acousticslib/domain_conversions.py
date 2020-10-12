import numpy as np
from math import ceil

# Note: assumption for these plots is that time is a ROW vector.

def timeseries2linearspectrum(x, dt):
    x = np.atleast_2d(x)
    N = x.shape[1]
    X = np.fft.fft(x)*dt

    shift_amount = ceil(N/2) - 1
    linear_spectrum = np.roll(X, shift_amount)

    df = 1/(N*dt)
    f_range = np.arange(N)*df
    shifted_frequency_range = f_range - (ceil(N/2) - 1)*df
    return linear_spectrum, shifted_frequency_range

def linearspectrum2timeseries(X, dt):
    X = np.atleast_2d(X)
    N = X.shape[1]
    shift_amount = 1 - ceil(N/2)
    X = np.roll(X, shift_amount)
    time_series = np.fft.ifft(X)/dt
    t_range = np.arange(N)*dt
    return time_series, t_range