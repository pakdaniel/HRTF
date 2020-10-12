import numpy as np
from math import ceil,floor

def cross_spectral_density(X1,X2,dt):
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


