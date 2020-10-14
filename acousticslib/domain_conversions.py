import numpy as np
from math import ceil, floor

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

def linearspectrum2powerspectraldensity(X, dt):
    X = np.atleast_2d(X)
    N = X.shape[1]

    sampling_frequency = 1/dt
    sample_time = N*dt

    Sxx = np.real(np.multiply(X,np.conjugate(X)))/sample_time

    df = 1/(N*dt)
    f_range = np.arange(N)*df
    shifted_frequency_range = f_range - (ceil(N/2) - 1)*df

    zero_index = floor((N+1)/2) - 1
    Gxx = np.zeros((1, N-(zero_index)))
    Gxx[0, 0] = Sxx[0, zero_index]
    Gxx[0, 1:N-(zero_index)] = 2*Sxx[0, zero_index+1:]

    if shifted_frequency_range[-1] == sampling_frequency/2:
        Gxx[0, -1] = Gxx[0, -1]/2

    Gxx_f_range = shifted_frequency_range[zero_index:]
    return Sxx, Gxx, Gxx_f_range