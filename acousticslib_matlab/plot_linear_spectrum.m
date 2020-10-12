function h = plot_linear_spectrum(f_range, X, varargin)

DEFAULT_WIDTH = 600;
DEFAULT_HEIGHT = 400;
FONT_SIZE = 14;
LINE_WIDTH = 2;
DEFAULT_PLOT_TYPE = 'default';

p = inputParser;
addRequired(p, 'f_range')
addRequired(p, 'X')
addOptional(p, 'PlotType', DEFAULT_PLOT_TYPE)
addOptional(p, 'Title', 'Linear spectrum')
addOptional(p, 'Units', 'wu/Hz')
parse(p, f_range, X, varargin{:})

if strcmp(p.Results.PlotType, 'default')
    plotfunc = @plot;
elseif strcmp(p.Results.PlotType, 'semilogx')
    plotfunc = @semilogx;
end

if strcmp(p.Results.Units, 'dB')
   X = mag2db(X); 
end

if nargout > 0
    h = plotfunc(f_range, X, 'LineWidth', LINE_WIDTH);
else
    plotfunc(f_range, X, 'LineWidth', LINE_WIDTH);
end

set(gcf,'position',[50,50, DEFAULT_WIDTH, DEFAULT_HEIGHT])
title(p.Results.Title, 'Interpreter', 'latex', 'FontSize', FONT_SIZE);
xlabel('Frequency (Hz)', 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
ylabel(strcat(['Real-valued Amplitude (' p.Results.Units ')']), 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
xlim([f_range(1) f_range(end)])
set(gca,'TickLabelInterpreter', 'latex','fontsize',FONT_SIZE)
grid on
set(gcf, "Renderer", "Painters")
end