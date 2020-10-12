import matplotlib.pyplot as plt
from .unit_conversions import acousticmag2db
import numpy as np

def plot_time_series(t_range, x, width=15, height=5, font_size=14, line_width=2, units="wu", plot_type="default", title="Time-series data", legend=[], legend_loc = "northeast"):

    if plot_type == "default":
        plotfunc = plt.plot
    elif plot_type == "semilogx":
        plotfunc = plt.semilogx
    elif plot_type == "semilogy":
        plotfunc = plt.semilogy

    plt.figure(figsize = (width, height))
    h = plotfunc(t_range, x, linewidth = line_width)
    plt.title(title, {"fontsize": font_size})

    plt.xlabel('Time (s)', fontsize=font_size)
    plt.ylabel('Amplitude ({})'.format(units), fontsize=font_size)
    plt.xlim([t_range[0], t_range[-1]])
    plt.xticks(fontsize=font_size)
    plt.grid(True, which='both')

    if legend:
        plt.legend(legend, loc=legend_loc)

    return h

def plot_linear_spectrum_amplitude(f_range, X, width=15, height=5, font_size=14, line_width=2,
    x_units = "Hz", units="wu/Hz", plot_type="default", title="Linear spectrum (absolute magnitude)", legend=[], legend_loc = "northeast"):

    if plot_type == "default":
        plotfunc = plt.plot
    elif plot_type == "semilogx":
        plotfunc = plt.semilogx
    elif plot_type == "semilogy":
        plotfunc = plt.semilogy

    X_amp = abs(X)

    if units == "dB":
        X_amp = acousticmag2db(X_amp/max(X_amp))

    if x_units == 'rad/sec':
        f_range = 2*np.pi*f_range

    plt.figure(figsize = (width, height))
    h = plotfunc(f_range, X_amp, linewidth = line_width)

    plt.xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    plt.ylabel('Absolute Amplitude ({})'.format(units), fontsize=font_size)
    plt.xlim([f_range[0], f_range[-1]])
    plt.xticks(fontsize=font_size)
    plt.grid(True, which='both')

    if legend:
        plt.legend(legend, loc=legend_loc)

    return h