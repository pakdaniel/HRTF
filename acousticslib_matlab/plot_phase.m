function [h] = plot_phase(f_range, X, varargin)
DEFAULT_WIDTH = 600;
DEFAULT_HEIGHT = 400;
FONT_SIZE = 16;
LINE_WIDTH = 2;
DEFAULT_UNITS = 'rad';

p = inputParser;
addRequired(p, 'f_range')
addRequired(p, 'X')
addOptional(p, 'Units', DEFAULT_UNITS)
addOptional(p, 'PlotType', 'default')
addOptional(p, 'Title', 'Phase angle vs Frequency')
parse(p, f_range, X, varargin{:})

if strcmp(p.Results.PlotType, 'default')
    plotfunc = @plot;
elseif strcmp(p.Results.PlotType, 'semilogx')
    plotfunc = @semilogx;
elseif strcmp(p.Results.PlotType, 'semilogy')
    plotfunc = @semilogy;
end

if nargout > 0
    h = plotfunc(f_range, angle(X), 'LineWidth', LINE_WIDTH);
else
    plotfunc(f_range, angle(X), 'LineWidth', LINE_WIDTH);
end

set(gcf,'position',[50,50, DEFAULT_WIDTH, DEFAULT_HEIGHT])
title(p.Results.Title, 'Interpreter', 'latex', 'FontSize', FONT_SIZE);
xlabel('Frequency (Hz)', 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
ylabel(strcat(['Phase angle (' p.Results.Units ')']), 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
set(gca,'TickLabelInterpreter', 'latex','fontsize',FONT_SIZE)
grid on
set(gcf, "Renderer", "Painters")
end
