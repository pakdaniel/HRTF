function h = plot_linear_spectrum_amplitude(f_range, X, varargin)
DEFAULT_WIDTH = 600;
DEFAULT_HEIGHT = 400;
FONT_SIZE = 14;
LINE_WIDTH = 2;
DEFAULT_PLOT_TYPE = 'default';

p = inputParser;
addRequired(p, 'f_range')
addRequired(p, 'Sxx')
addOptional(p, 'PlotType', DEFAULT_PLOT_TYPE)
addOptional(p, 'Title', 'Linear spectrum (absolute magnitude)')
addOptional(p, 'XUnits', 'Hz');
addOptional(p, 'Units', 'wu/Hz')
parse(p, f_range, X, varargin{:})

if strcmp(p.Results.PlotType, 'default')
    plotfunc = @plot;
elseif strcmp(p.Results.PlotType, 'semilogx')
    plotfunc = @semilogx;
end

X = abs(X);

if strcmp(p.Results.Units, 'dB')
   X = mag2db(X/max(X)); 
end

if strcmp(p.Results.XUnits, 'rad/sec')
   f_range = 2*pi*f_range;
end


if nargout > 0
    h = plotfunc(f_range, X, 'LineWidth', LINE_WIDTH);
else
    plotfunc(f_range, X, 'LineWidth', LINE_WIDTH);
end

plot_title = p.Results.Title;

set(gcf,'position',[50,50, DEFAULT_WIDTH, DEFAULT_HEIGHT])
title(plot_title, 'Interpreter', 'latex', 'FontSize', FONT_SIZE);
xlabel(strcat(['Frequency (' p.Results.XUnits ')']), 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
ylabel(strcat(['Absolute Amplitude (' p.Results.Units ')']), 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
xlim([f_range(1) f_range(end)])
set(gca,'TickLabelInterpreter', 'latex','fontsize',FONT_SIZE)
grid on
set(gcf, "Renderer", "Painters")
end