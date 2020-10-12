import numpy as np
import domain_conversions
import linear_spectrum_2_cross_spectral_density

def timeseries2crosscorrelation(x1,x2,dt):
    X1 = domain_conversions.linearspectrum2timeseries(x1,dt)[0]
    X2 = domain_conversions.linearspectrum2timeseries(x2,dt)[0]
    Sxy = cross_spectral_density(X1,X2,dt)[0]
    Rxy, Rxy_t_range = crossspectraldensity2timeseries(Sxy,dt)

    return Rxy, Rxy_t_range
