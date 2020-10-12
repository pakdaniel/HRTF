function h = plot_time_series(t_range, x, varargin)
DEFAULT_WIDTH = 600;
DEFAULT_HEIGHT = 400;
FONT_SIZE = 14;
LINE_WIDTH = 2;
DEFAULT_UNITS = 'wu';

p = inputParser;
addRequired(p, 't_range')
addRequired(p, 'x')
addOptional(p, 'Units', DEFAULT_UNITS)
addOptional(p, 'PlotType', 'default')
addOptional(p, 'Title', 'Time-series data')
addOptional(p, 'LineWidth', LINE_WIDTH)
addOptional(p, 'Legend', {})
addOptional(p, 'LegendLoc', 'northeast');
addOptional(p, 'PlotWidth', DEFAULT_WIDTH);
addOptional(p, 'PlotHeight', DEFAULT_HEIGHT);
parse(p, t_range, x, varargin{:})

line_width = p.Results.LineWidth;

if strcmp(p.Results.PlotType, 'default')
    plotfunc = @plot;
elseif strcmp(p.Results.PlotType, 'semilogx')
    plotfunc = @semilogx;
elseif strcmp(p.Results.PlotType, 'semilogy')
    plotfunc = @semilogy;
end

if nargout > 0
    h = plotfunc(t_range, x, 'LineWidth', line_width);
else
    plotfunc(t_range, x, 'LineWidth', line_width)
end

plot_title = p.Results.Title;

set(gcf,'position',[50,50, p.Results.PlotWidth, p.Results.PlotHeight])
title(plot_title, 'Interpreter', 'latex', 'FontSize', FONT_SIZE);
xlabel('Time (s)', 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
ylabel(strcat(['Amplitude (' p.Results.Units ')']), 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
xlim([t_range(1) t_range(end)])
set(gca,'TickLabelInterpreter', 'latex','fontsize',FONT_SIZE)
grid on
grid minor

if ~isempty(p.Results.Legend)
   legend(p.Results.Legend{:}, 'Location', p.Results.LegendLoc, 'Interpreter', 'latex');
end

set(gcf, "Renderer", "Painters")
end