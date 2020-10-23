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

def ts2ls(*args, **kwargs):
    return timeseries2linearspectrum(*args, **kwargs)

def linearspectrum2timeseries(X, dt):
    X = np.atleast_2d(X)
    N = X.shape[1]

    shift_amount = 1 - ceil(N/2)
    X = np.roll(X, shift_amount)
    time_series = np.fft.ifft(X)/dt
    t_range = np.arange(N)*dt
    return time_series, t_range

def ls2ts(*args, **kwargs):
    return linearspectrum2timeseries(*args, **kwargs)

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
    # Size of Gxx is N - (floor(N+1)/2) + 1
    Gxx = np.zeros((1, N-(zero_index)))
    Gxx[0, 0] = Sxx[0, zero_index]
    Gxx[0, 1:N-(zero_index)] = 2*Sxx[0, zero_index+1:]

    if shifted_frequency_range[-1] == sampling_frequency/2:
        Gxx[0, -1] = Gxx[0, -1]/2

    Gxx_f_range = shifted_frequency_range[zero_index:]
    return Sxx, Gxx, Gxx_f_range

def ls2psd(*args, **kwargs):
    return linearspectrum2powerspectraldensity(*args, **kwargs)

def crossspectraldensity2timeseries(Sxy,dt):
    """
    Inputs are cross PSD (Sxy), and sampling time
    Outputs are time series equivalent and time vector
    """
    N = len(Sxy)
    shift_amount = 1-ceil(N/2)
    Sxy = np.roll(Sxy, shift_amount)

    time_series = np.fft.ifft(Sxy,dt)
    time_series = np.roll(time_series,shift_amount)

    t_range = np.arange(0,N)*dt
    t_range = t_range - (ceil(N/2)-1)*dt

    return time_series,t_range

def csd2ts(*args, **kwargs):
    return crossspectraldensity2timeseries(*args, **kwargs)

def linearspectrum2crossspectraldensity(X1,X2,dt):
    """
    function [Sxy, Gxy, Gxy_f_range] = linearspectrum2crossspectraldensity(X1, X2, dt)
    Inputs are 2 linear spectrums (frequency) and sample time
    Outputs are Sxy (cross PSD), Gxy (single sided cross PSD), and frequency range
    Inputs X1 and X2 are individual numpy row arrays
    """
    if len(X1) != len(X2):
        raise ValueError("Lengths of input linear spectrums are NOT the same")
    N = len(X1)
    fs = 1/dt 
    T = N*dt
    df = 1/(N*dt)

    Sxy = (X1)*np.conj(X2)/T 
    f_range = np.arange(0,N)*df
    shifted_f_range = f_range-(ceil(N/2)-1)*df
    zero_index = floor((N+1)/2)
    Gxy = np.zeros(len(Sxy))
    Gxy[0] = Sxy[zero_index]
    Gxy[1:len(Sxy)-(zero_index-1)] = 2*Sxy[zero_index:] 

    if shifted_f_range[-1] == fs/2:
        Gxy[-1] = Gxy[-1]/2

    Gxy_f_range = shifted_f_range[zero_index:]

    return Sxy, Gxy, Gxy_f_range

def ls2csd(*args, **kwargs):
    return linearspectrum2crossspectraldensity(*args, **kwargs)

def timeseries2crosscorrelation(x1,x2,dt):
    """
    Inputs are two time series and sample time
    Ouputs are Rxy (cross correlation) and time vector
    """

    X1 = linearspectrum2timeseries(x1,dt)[0]
    X2 = linearspectrum2timeseries(x2,dt)[0]
    Sxy = linearspectrum2crossspectraldensity(X1,X2,dt)[0]
    Rxy, Rxy_t_range = crossspectraldensity2timeseries(Sxy,dt)
    return Rxy, Rxy_t_range

def ts2cc(*args, **kwargs):
    return timeseries2crosscorrelation(*args, **kwargs)

def linearspectrum2crossspectraldensity(X1,X2,dt):
    """
    function [Sxy, Gxy, Gxy_f_range] = linearspectrum2crossspectraldensity(X1, X2, dt)
    Input are 2 linear spectrums (frequency) and output are Sxy and Gxy
    Inputs X1 and X2 are individual numpy row arrays
    """
    if len(X1) != len(X2):
        raise ValueError("Lengths of input linear spectrums are NOT the same")
    N = len(X1)
    fs = 1/dt 
    T = N*dt
    df = 1/(N*dt)

    Sxy = (X1)*np.conj(X2)/T 
    f_range = np.arange(0,N)*df
    shifted_f_range = f_range-(ceil(N/2)-1)*df
    zero_index = floor((N+1)/2)
    Gxy = np.zeros(len(Sxy))
    Gxy[0] = Sxy[zero_index]
    Gxy[1:len(Sxy)-(zero_index-1)] = 2*Sxy[zero_index:] 

    if shifted_f_range[-1] == fs/2:
        Gxy[-1] = Gxy[-1]/2

    Gxy_f_range = shifted_f_range[zero_index:]

    return Sxy, Gxy, Gxy_f_range

def ls2csd(*args, **kwargs):
    return linearspectrum2crossspectraldensity(*args, **kwargs)

def timeseries2crosscorrelation(x1, x2, dt):
    X1, _ = timeseries2linearspectrum(x1, dt)
    X2, _ = timeseries2linearspectrum(x2, dt)
    Sxy, _, _= linearspectrum2crossspectraldensity(X1, X2, dt)
    Rxy, Rxy_t_range = crossspectraldensity2timeseries(Sxy, dt)
    return Rxy, Rxy_t_range

def ts2cc(*args, **kwargs):
    return timeseries2crosscorrelation(*args, **kwargs)