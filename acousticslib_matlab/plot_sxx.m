function h = plot_sxx(f_range, Sxx, varargin)

DEFAULT_WIDTH = 600;
DEFAULT_HEIGHT = 400;
FONT_SIZE = 14;
LINE_WIDTH = 2;
DEFAULT_UNITS = 'wu$^2$/Hz';

p = inputParser;
addRequired(p, 'f_range')
addRequired(p, 'Sxx')
addOptional(p, 'Units', DEFAULT_UNITS)
parse(p, f_range, Sxx, varargin{:})

if nargout > 0
    h = plot(f_range, Sxx, 'LineWidth', LINE_WIDTH);
else
    plot(f_range, Sxx, 'LineWidth', LINE_WIDTH);
end

set(gcf,'position',[50,50, DEFAULT_WIDTH, DEFAULT_HEIGHT])
title('Two-sided power spectral density', 'Interpreter', 'latex', 'FontSize', FONT_SIZE);
xlabel('Frequency (Hz)', 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
ylabel(strcat(['Power (' p.Results.Units ')']), 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
xlim([f_range(1) f_range(end)])
set(gca,'TickLabelInterpreter', 'latex','fontsize',FONT_SIZE)
grid on
set(gcf, "Renderer", "Painters")
end