import matplotlib.pyplot as plt
from .unit_conversions import acousticmag2db
import numpy as np

DEFAULT_WIDTH = 15
DEFAULT_HEIGHT = 5
DEFAULT_FONTSIZE = 14
DEFAULT_LINEWIDTH = 2

def _get_plot_func(plot_type):
    if plot_type == "default":
        plotfunc = plt.plot
    elif plot_type == "semilogx":
        plotfunc = plt.semilogx
    elif plot_type == "semilogy":
        plotfunc = plt.semilogy
    return plotfunc

def plot_time_series(t_range, x, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, font_size=DEFAULT_FONTSIZE, line_width=DEFAULT_LINEWIDTH, units="wu", plot_type="default", title="Time-series data", legend=[], legend_loc = "northeast"):

    plot = _get_plot_func(plot_type)

    plt.figure(figsize = (width, height))
    h = plot(np.atleast_2d(t_range).T, np.atleast_2d(x).T, linewidth = line_width)
    plt.title(title, {"fontsize": font_size})

    plt.xlabel('Time (s)', fontsize=font_size)
    plt.ylabel('Amplitude ({})'.format(units), fontsize=font_size)
    plt.xlim([t_range[0], t_range[-1]])
    plt.xticks(fontsize=font_size)
    plt.grid(True, which='both')

    if legend:
        plt.legend(legend, loc=legend_loc)

    return h

def plot_linear_spectrum_amplitude(f_range, X, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, font_size=DEFAULT_FONTSIZE, line_width=DEFAULT_LINEWIDTH,
    x_units = "Hz", units="wu/Hz", plot_type="default", title="Linear spectrum (absolute magnitude)", legend=[], legend_loc = "northeast"):

    plot = _get_plot_func(plot_type)

    X_amp = np.atleast_2d(abs(X))

    if units == "dB":
        X_amp = acousticmag2db(X_amp/max(X_amp))

    if x_units == 'rad/sec':
        f_range = 2*np.pi*f_range

    plt.figure(figsize = (width, height))
    h = plot(np.atleast_2d(f_range).T, X_amp.T, linewidth = line_width)

    plt.xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    plt.ylabel('Absolute Amplitude ({})'.format(units), fontsize=font_size)
    plt.xlim([f_range[0], f_range[-1]])
    plt.xticks(fontsize=font_size)
    plt.grid(True, which='both')

    if legend:
        plt.legend(legend, loc=legend_loc)

    return h

def plot_phase(f_range, X, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, font_size=DEFAULT_FONTSIZE, line_width=DEFAULT_LINEWIDTH,
    x_units = "Hz", units="rad", plot_type="default", title="Phase angle vs Frequency", legend=[], legend_loc = "northeast"):

    plot = _get_plot_func(plot_type)

    X_amp = np.atleast_2d(X)

    if units == "dB":
        X_amp = acousticmag2db(X_amp/max(X_amp))

    if x_units == 'rad/sec':
        f_range = 2*np.pi*f_range

    plt.figure(figsize = (width, height))
    h = plot(np.atleast_2d(f_range).T, np.angle(X_amp).T, linewidth = line_width)

    plt.xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    plt.ylabel('Phase Angle ({})'.format(units), fontsize=font_size)
    plt.xlim([f_range[0], f_range[-1]])
    plt.xticks(fontsize=font_size)
    plt.grid(True, which='both')

    if legend:
        plt.legend(legend, loc=legend_loc)

    return h

def plot_linear_spectrum(f_range, X, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, font_size=DEFAULT_FONTSIZE,
    line_width=DEFAULT_LINEWIDTH, x_units = "Hz", units="wu/Hz", plot_type="default",
    title="Real-valued linear spectrum", legend=[], legend_loc = "northeast"):

    plot = _get_plot_func(plot_type)

    X = np.atleast_2d(X)

    if units == "dB":
        X = acousticmag2db(X/max(X))

    if x_units == 'rad/sec':
        f_range = 2*np.pi*f_range

    plt.figure(figsize = (width, height))
    h = plot(np.atleast_2d(f_range).T, X.T, linewidth = line_width)

    plt.xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    plt.ylabel('Real-valued Amplitude ({})'.format(units), fontsize=font_size)
    plt.xlim([f_range[0], f_range[-1]])
    plt.xticks(fontsize=font_size)
    plt.grid(True, which='both')

    if legend:
        plt.legend(legend, loc=legend_loc)

    return h

def plot_gxx(Gxx_f_range, Gxx, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, font_size=DEFAULT_FONTSIZE,
    line_width=DEFAULT_LINEWIDTH, x_units = "Hz", units="wu$^2$/Hz", plot_type="default",
    title="One-sided power spectral density", legend=[], legend_loc = "northeast"):

    plot = _get_plot_func(plot_type)

    Gxx = np.atleast_2d(Gxx)

    if x_units == 'rad/sec':
        Gxx_f_range = 2*np.pi*Gxx_f_range

    plt.figure(figsize = (width, height))
    h = plot(np.atleast_2d(Gxx_f_range).T, Gxx.T, linewidth = line_width)

    plt.xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    plt.ylabel('Power ({})'.format(units), fontsize=font_size)
    plt.xlim([Gxx_f_range[0], Gxx_f_range[-1]])
    plt.xticks(fontsize=font_size)
    plt.grid(True, which='both')

    if legend:
        plt.legend(legend, loc=legend_loc)

    return h


def plot_sxx(f_range, Sxx, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, font_size=DEFAULT_FONTSIZE,
    line_width=DEFAULT_LINEWIDTH, x_units = "Hz", units="wu$^2$/Hz", plot_type="default",
    title="Two-sided power spectral density", legend=[], legend_loc = "northeast"):

    Sxx = np.atleast_2d(Sxx)

    if x_units == 'rad/sec':
        f_range = 2*np.pi*f_range

    plot = _get_plot_func(plot_type)
    h = plot(np.atleast_2d(f_range).T, Sxx.T, linewidth = line_width)

    plt.xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    plt.ylabel('Power ({})'.format(units), fontsize=font_size)
    plt.xlim([f_range[0], f_range[-1]])
    plt.xticks(fontsize=font_size)
    plt.grid(True, which='both')

    if legend:
        plt.legend(legend, loc=legend_loc)

    return h