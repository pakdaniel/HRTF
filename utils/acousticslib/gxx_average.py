from math import floor
from numpy import zeros
from acousticslib.domain_conversions import *

def gxx_average(x, dt, num_bins):

    # rms average

    truncated_length = floor(len(x)/num_bins)

    rms_avged_gxx = zeros((1, floor(truncated_length/2)+1))
    for ii in range(num_bins):
        binned_x = x[truncated_length*ii: truncated_length*(ii+1)]
        binned_X, _ = timeseries2linearspectrum(binned_x, dt)
        _, binned_Gxx, _ = linearspectrum2powerspectraldensity(binned_X, dt)
        rms_avged_gxx += binned_Gxx
    
    rms_avged_gxx = rms_avged_gxx / num_bins

    # linear average

    linear_avged_X = zeros((1, truncated_length))
    for jj in range(num_bins):
        binned_x = x[truncated_length*jj: truncated_length*(jj+1)]
        binned_X, _ = timeseries2linearspectrum(binned_x, dt)
        linear_avged_X = linear_avged_X + binned_X
    linear_avged_X = linear_avged_X / num_bins
    _, linear_avged_gxx, _ = linearspectrum2powerspectraldensity(linear_avged_X, dt)

    # time average

    time_avged_x = zeros((1, truncated_length))
    for kk in range(num_bins):
        binned_x = x[truncated_length*kk: truncated_length*(kk+1)]
        time_avged_x = time_avged_x + binned_x.T
    time_avged_x = time_avged_x / num_bins
    time_avged_X, _ = timeseries2linearspectrum(time_avged_x, dt)
    _, time_avged_gxx, f_range = linearspectrum2powerspectraldensity(time_avged_X, dt)
    return rms_avged_gxx, linear_avged_gxx, time_avged_gxx, f_range