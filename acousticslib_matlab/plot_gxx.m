function h = plot_gxx(Gxx_f_range, Gxx, varargin)

DEFAULT_WIDTH = 600;
DEFAULT_HEIGHT = 400;
FONT_SIZE = 16;
LINE_WIDTH = 2;
DEFAULT_UNITS = 'wu$^2$/Hz';

p = inputParser;
addRequired(p, 'Gxx_f_range')
addRequired(p, 'Gxx')
addOptional(p, 'Units', DEFAULT_UNITS)
addOptional(p, 'PlotType', 'default')
addOptional(p, 'Title', 'One-sided power spectral density')
parse(p, Gxx_f_range, Gxx, varargin{:})

if strcmp(p.Results.PlotType, 'default')
    plotfunc = @plot;
elseif strcmp(p.Results.PlotType, 'semilogx')
    plotfunc = @semilogx;
elseif strcmp(p.Results.PlotType, 'semilogy')
    plotfunc = @semilogy;
end

if nargout > 0
    h = plotfunc(Gxx_f_range, Gxx, 'LineWidth', LINE_WIDTH);
else
    plotfunc(Gxx_f_range, Gxx, 'LineWidth', LINE_WIDTH);
end

set(gcf,'position',[50,50, DEFAULT_WIDTH, DEFAULT_HEIGHT])
title(p.Results.Title, 'Interpreter', 'latex', 'FontSize', FONT_SIZE);
xlabel('Frequency (Hz)', 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
ylabel(strcat(['Power (' p.Results.Units ')']), 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
xlim([Gxx_f_range(1) Gxx_f_range(end)])
set(gca,'TickLabelInterpreter', 'latex','fontsize',FONT_SIZE)
grid on
set(gcf, "Renderer", "Painters")
end