import matplotlib.pyplot as plt
from .unit_conversions import acousticmag2db
from .domain_conversions import timeseries2linearspectrum, linearspectrum2timeseries, linearspectrum2powerspectraldensity
import numpy as np
from math import floor
from matplotlib.ticker import FuncFormatter

DEFAULT_WIDTH = 15
DEFAULT_HEIGHT = 5
DEFAULT_FONTSIZE = 25
DEFAULT_LINEWIDTH = 2
DEFAULT_FIGSIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)

def update_plotting_params(params):
    plt.rcParams.update(params)

def _get_plot_func(plot_type, ax):
    if plot_type == "default":
        plotfunc = ax.plot
    elif plot_type == "semilogx":
        plotfunc = ax.semilogx
    elif plot_type == "semilogy":
        plotfunc = ax.semilogy
    else:
        raise NotImplementedError
    return plotfunc

def plot_time_series(t_range, x, ax = None, usefig = False, figsize = DEFAULT_FIGSIZE, font_size=DEFAULT_FONTSIZE, line_width=DEFAULT_LINEWIDTH, units="wu", plot_type="default", title="Time-series data", legend=[], legend_loc = "upper right"):

    if usefig and not ax:
        fig, ax = plt.subplots(figsize=figsize)
    elif not ax:
        ax = plt.gca()
    plot = _get_plot_func(plot_type, ax)

    
    plot(np.atleast_2d(t_range).T, np.atleast_2d(x).T, linewidth = line_width)

    if title:
        ax.title(title, {"fontsize": font_size})

    ax.set_xlabel('Time (s)', fontsize=font_size)
    ax.set_ylabel('Amplitude ({})'.format(units), fontsize=font_size)
    ax.set_xlim([t_range[0], t_range[-1]])
    ax.tick_params(labelsize=font_size)
    ax.grid(True, which='both')

    if legend:
        ax.legend(legend, loc=legend_loc)

    return ax

def plot_linear_spectrum_amplitude(f_range, X, ax = None, usefig = False, figsize = DEFAULT_FIGSIZE, font_size=DEFAULT_FONTSIZE, line_width=DEFAULT_LINEWIDTH,
    x_units = "Hz", units="wu/Hz", plot_type="default", title="Linear spectrum (absolute magnitude)", legend=[], legend_loc = "upper right"):

    if usefig and not ax:
        fig, ax = plt.subplots(figsize=figsize)
    elif not ax:
        ax = plt.gca()
    plot = _get_plot_func(plot_type, ax)

    X_amp = np.atleast_2d(abs(X))

    if units == "dB":
        X_amp = acousticmag2db(X_amp/max(X_amp))

    if x_units == 'rad/sec':
        f_range = 2*np.pi*f_range

    plot(np.atleast_2d(f_range).T, X_amp.T, linewidth = line_width)
    if title:
        ax.title(title, {"fontsize": font_size})
    ax.set_xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    ax.set_ylabel('Absolute Amplitude ({})'.format(units), fontsize=font_size)
    ax.set_xlim([f_range[0], f_range[-1]])
    ax.tick_params(labelsize=font_size)
    ax.grid(True, which='both')

    if legend:
        ax.legend(legend, loc=legend_loc)

    return ax

def plot_phase(f_range, X, ax = None, usefig = False, figsize = DEFAULT_FIGSIZE, font_size=DEFAULT_FONTSIZE, line_width=DEFAULT_LINEWIDTH,
    x_units = "Hz", units="rad", plot_type="default", title="Phase angle vs Frequency", legend=[], legend_loc = "upper right"):

    if usefig and not ax:
        fig, ax = plt.subplots(figsize=figsize)
    elif not ax:
        ax = plt.gca()
    plot = _get_plot_func(plot_type, ax)

    X_amp = np.atleast_2d(X)

    if units == "deg":
        y = np.angle(X_amp, deg=True)
        units = "$^{\circ}$"
    else:
        y = np.angle(X_amp)

    if x_units == 'rad/sec':
        f_range = 2*np.pi*f_range
    elif x_units == 'deg/sec':
        f_range = 360*f_range
        x_units = "$^{\circ}$/sec"


    plot(np.atleast_2d(f_range).T, y.T, linewidth = line_width)

    if title:
        ax.title(title, {"fontsize": font_size})
    ax.set_xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    ax.set_ylabel('Phase Angle ({})'.format(units), fontsize=font_size)
    ax.set_xlim([f_range[0], f_range[-1]])
    ax.tick_params(labelsize=font_size)
    ax.grid(True, which='both')

    if legend:
        ax.legend(legend, loc=legend_loc)

    return ax

def plot_linear_spectrum(f_range, X, ax = None, usefig = False, figsize = DEFAULT_FIGSIZE, font_size=DEFAULT_FONTSIZE,
    line_width=DEFAULT_LINEWIDTH, x_units = "Hz", units="wu/Hz", plot_type="default",
    title="Real-valued linear spectrum", legend=[], legend_loc = "upper right"):

    if usefig and not ax:
        fig, ax = plt.subplots(figsize=figsize)
    elif not ax:
        ax = plt.gca()
    plot = _get_plot_func(plot_type, ax)

    X = np.atleast_2d(X)

    if units == "dB":
        X = acousticmag2db(X/max(X))

    if x_units == 'rad/sec':
        f_range = 2*np.pi*f_range

    
    plot(np.atleast_2d(f_range).T, X.T, linewidth = line_width)
    if title:
        ax.title(title, {"fontsize": font_size})
    ax.set_xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    ax.set_ylabel('Real-valued Amplitude ({})'.format(units), fontsize=font_size)
    ax.set_xlim([f_range[0], f_range[-1]])
    ax.tick_params(labelsize=font_size)
    ax.grid(True, which='both')

    if legend:
        ax.legend(legend, loc=legend_loc)

    return ax

def plot_gxx(Gxx_f_range, Gxx, ax = None, usefig = False, figsize = DEFAULT_FIGSIZE, font_size=DEFAULT_FONTSIZE,
    line_width=DEFAULT_LINEWIDTH, x_units = "Hz", units="wu$^2$/Hz", plot_type="default",
    title="One-sided power spectral density", legend=[], legend_loc = "upper right"):

    if usefig and not ax:
        fig, ax = plt.subplots(figsize=figsize)
    elif not ax:
        ax = plt.gca()
    plot = _get_plot_func(plot_type, ax)

    Gxx = np.atleast_2d(Gxx)

    if x_units == 'rad/sec':
        Gxx_f_range = 2*np.pi*Gxx_f_range

    
    plot(np.atleast_2d(Gxx_f_range).T, Gxx.T, linewidth = line_width)

    if title:
        ax.title(title, {"fontsize": font_size})
    ax.set_xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    ax.set_ylabel('Power ({})'.format(units), fontsize=font_size)
    ax.set_xlim([Gxx_f_range[0], Gxx_f_range[-1]])
    ax.tick_params(labelsize=font_size)
    ax.grid(True, which='both')

    if legend:
        ax.legend(legend, loc=legend_loc)

    return ax


def plot_sxx(f_range, Sxx, ax = None, usefig = False, figsize = DEFAULT_FIGSIZE, font_size=DEFAULT_FONTSIZE,
    line_width=DEFAULT_LINEWIDTH, x_units = "Hz", units="wu$^2$/Hz", plot_type="default",
    title="Two-sided power spectral density", legend=[], legend_loc = "upper right"):

    Sxx = np.atleast_2d(Sxx)

    if x_units == 'rad/sec':
        f_range = 2*np.pi*f_range

    if usefig and not ax:
        fig, ax = plt.subplots(figsize=figsize)
    elif not ax:
        ax = plt.gca()
    plot = _get_plot_func(plot_type, ax)
    
    plot(np.atleast_2d(f_range).T, Sxx.T, linewidth = line_width)

    if title:
        ax.title(title, {"fontsize": font_size})
    ax.set_xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    ax.set_ylabel('Power ({})'.format(units), fontsize=font_size)
    ax.set_xlim([f_range[0], f_range[-1]])
    plt.xticks(fontsize=font_size)
    ax.grid(True, which='both')

    if legend:
        ax.legend(legend, loc=legend_loc)

    return ax

def plot_spectrogram(x, dt, record_length = 0, num_bins = 0, percent_overlap = 0,
    plot_type = "default", title="Spectrograph", convert_to_dB = False,
    figsize = DEFAULT_FIGSIZE, font_size=DEFAULT_FONTSIZE, num_xticks = 10):
    
    binned_Gxx_f_range = None

    num_samples = len(x)
    if not num_bins and record_length <= 1:
        raise Exception('Record length must be an integer 2 or greater')
    if num_bins and record_length:
        raise Exception('Cannot specify both number of records and record length')
    elif record_length:
        num_bins = floor((num_samples - record_length)/((1 - 0.01*percent_overlap)*record_length) + 1)
    elif num_bins:
        record_length = floor(num_samples / (1 + (1 - 0.01*percent_overlap)*(num_bins - 1)))
    
    if record_length <= 1:
        raise Exception("Computed record length of {} must be an integer 2 or greater; please use fewer bins".format(record_length))

    spectrogram_matrix = np.zeros(( floor(record_length/2 + 1),
        # if record_length is 2, X is 2, Gxx is 2
        # if record_length is 3, Gxx is 2
        # if record_length is 4, Gxx is 3
        # if record_length is 5, Gxx is 3
        num_bins))
    
    for i in range(num_bins):
        start_index = floor((1 - 0.01*percent_overlap)*(record_length)*i)
        binned_x = x[start_index:start_index+record_length]
        binned_X, _ = timeseries2linearspectrum(binned_x, dt)
        _, binned_Gxx, binned_Gxx_f_range = linearspectrum2powerspectraldensity(binned_X, dt)
        if convert_to_dB:
            binned_Gxx = acousticmag2db(binned_Gxx)
        
        spectrogram_matrix[:, i] = binned_Gxx.T.flatten()

    num_samples_used = num_bins*record_length
    end_time = num_samples_used*dt
    t_range = np.linspace(0, end_time, num_bins)

    

    if convert_to_dB:
        units = 'dB'
    else:
        units = 'wu$^2$/Hz'
    fig = plt.figure(figsize=figsize)
    h = plt.imshow(spectrogram_matrix, cmap="jet", origin="lower", extent=[0, end_time, 0, binned_Gxx_f_range[-1]], aspect="auto")

    if title:
        plt.title("{} ({} records, {} samples/record), {}% Overlap".format(title, num_bins, record_length, percent_overlap), {"fontsize": font_size})
    cbar = fig.colorbar(h)
    cbar.set_label("Magnitude ({})".format(units))
    cbar.ax.tick_params(labelsize=font_size)
    plt.xticks(fontsize = font_size)
    
    # also add 0:end of t range for x ticks
    # plt.gca().get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format((x*dt), ',')))
    
    plt.xlabel('Time (s)', fontsize=font_size)
    plt.ylabel('Frequency (Hz)', fontsize=font_size)

    return h