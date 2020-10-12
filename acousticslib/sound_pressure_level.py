import numpy as np

def sound_pressure_level(x):
    p_ref = 20*10^(-6)
    return 20*np.log10(time_series_rms(x)/p_ref)

def time_series_rms(x):
    return np.sqrt(sum(x**2)/len(x))