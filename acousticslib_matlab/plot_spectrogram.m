function h = plot_spectrogram(x, dt, varargin)

DEFAULT_WIDTH = 1000;
DEFAULT_HEIGHT = 500;
FONT_SIZE = 16;

p = inputParser;
addRequired(p, 'x')
addRequired(p, 'dt')
addOptional(p, 'RecordLength', 0)
addOptional(p, 'NumBins', 0)
addOptional(p, 'PercentOverlap', 0, @isnumeric);
addOptional(p, 'PlotType', 'default')
addOptional(p, 'Title', 'Spectrograph')
addOptional(p, 'ConvertToDb', false)
parse(p, x, dt, varargin{:})

num_bins = p.Results.NumBins;
record_length = p.Results.RecordLength;
percent_overlap = p.Results.PercentOverlap;

num_samples = length(x);
if num_bins && record_length
    error('Cannot specify both number of records and record length')
elseif record_length
    num_bins = floor((num_samples - record_length)/((1 - 0.01*percent_overlap)*record_length) + 1);
elseif num_bins
    record_length = floor(num_samples / (1 + (1 - 0.01*percent_overlap)*(num_bins - 1)));
end

% reshape as bins
spectrogram_matrix = zeros(floor(record_length/2)+1, num_bins);

for i = 0 : num_bins - 1
   start_index = 1 + floor((1 - 0.01*percent_overlap)*(record_length)*i);
   binned_x = x(start_index:start_index+record_length);
   [binned_X, ~] = timeseries2linearspectrum(binned_x, dt);
   [~, binned_Gxx, binned_Gxx_f_range] = linearspectrum2powerspectraldensity(binned_X, dt);
   if p.Results.ConvertToDb
      binned_Gxx = acousticmag2db(binned_Gxx); 
   end
   spectrogram_matrix(:, i+1) = binned_Gxx.';
end

% compute time range
num_samples_used = start_index+record_length;
end_time = num_samples_used*dt;
t_range = linspace(0, end_time, num_bins);

if nargout > 0
    h = imagesc(t_range, binned_Gxx_f_range, spectrogram_matrix);
else
    imagesc(t_range, binned_Gxx_f_range, spectrogram_matrix);
end

if p.Results.ConvertToDb
    units = 'dB';
else
    units = 'wu$^2$/Hz';
end

set(gca, 'YDir', 'normal')
colormap('jet')
c = colorbar('eastoutside');
c.Label.Interpreter='latex';
c.TickLabelInterpreter = 'latex';
c.Label.String = strcat(['Magnitude (' units ')']);
c.Label.FontSize = FONT_SIZE;

xticks(0:t_range(end));
set(gcf,'position',[50,50, DEFAULT_WIDTH, DEFAULT_HEIGHT])
title(strcat([p.Results.Title ' (' int2str(num_bins) ' records, ' int2str(record_length) ' samples/record), ' num2str(percent_overlap) '\% Overlap']), 'Interpreter', 'latex', 'FontSize', FONT_SIZE);
xlabel('Time (s)', 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
ylabel('Frequency (Hz)', 'Interpreter', 'latex', 'FontSize', FONT_SIZE)
set(gca,'TickLabelInterpreter', 'latex','fontsize',FONT_SIZE)
grid on
set(gcf, "Renderer", "Painters")

end