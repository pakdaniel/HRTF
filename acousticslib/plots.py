import matplotlib.pyplot as plt
from .unit_conversions import acousticmag2db
from .domain_conversions import timeseries2linearspectrum, linearspectrum2timeseries, linearspectrum2powerspectraldensity
import numpy as np
from math import floor
from matplotlib.ticker import FuncFormatter

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
    plt.title(title, {"fontsize": font_size})
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
    plt.title(title, {"fontsize": font_size})
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
    plt.title(title, {"fontsize": font_size})
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
    plt.title(title, {"fontsize": font_size})
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
    plt.figure(figsize = (width, height))
    h = plot(np.atleast_2d(f_range).T, Sxx.T, linewidth = line_width)
    plt.title(title, {"fontsize": font_size})
    plt.xlabel('Frequency ({})'.format(x_units), fontsize=font_size)
    plt.ylabel('Power ({})'.format(units), fontsize=font_size)
    plt.xlim([f_range[0], f_range[-1]])
    plt.xticks(fontsize=font_size)
    plt.grid(True, which='both')

    if legend:
        plt.legend(legend, loc=legend_loc)

    return h

def plot_spectrogram(x, dt, record_length = 0, num_bins = 0, percent_overlap = 0,
    plot_type = "default", title="Spectrograph", convert_to_dB = False,
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, font_size=DEFAULT_FONTSIZE, num_xticks = 10):

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
    fig = plt.figure(figsize = (width, height))
    h = plt.imshow(spectrogram_matrix, cmap="jet", origin="lower", extent=[0, end_time, 0, binned_Gxx_f_range[-1]], aspect="auto")
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