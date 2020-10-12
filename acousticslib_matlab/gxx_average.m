function [rms_avged_gxx, linear_avged_gxx, time_avged_gxx, f_range] = gxx_average(x, dt, num_bins)

% rms average

truncated_length = floor(length(x)/num_bins);

rms_avged_gxx = zeros(1, floor(truncated_length/2)+1);
for ii = 0 : num_bins - 1
   binned_x = x(1 + truncated_length*ii: truncated_length*(ii+1));
   [binned_X, ~] = timeseries2linearspectrum(binned_x, dt);
   [~, binned_Gxx, ~] = linearspectrum2powerspectraldensity(binned_X, dt);
   rms_avged_gxx = rms_avged_gxx + binned_Gxx;
end
rms_avged_gxx = rms_avged_gxx ./ num_bins;

% linear average

linear_avged_X = zeros(1, truncated_length);
for jj = 0: num_bins - 1
    binned_x = x(1 + truncated_length*jj: truncated_length*(jj+1));
    [binned_X, ~] = timeseries2linearspectrum(binned_x, dt);
    linear_avged_X = linear_avged_X + binned_X.';
end
linear_avged_X = linear_avged_X ./ num_bins;
[~, linear_avged_gxx, ~] = linearspectrum2powerspectraldensity(linear_avged_X, dt);

% time average

time_avged_x = zeros(1, truncated_length);
for kk = 0 : num_bins - 1
   binned_x = x(1 + truncated_length*kk: truncated_length*(kk+1));
   time_avged_x = time_avged_x + binned_x.';
end
time_avged_x = time_avged_x ./ num_bins;
[time_avged_X, ~] = timeseries2linearspectrum(time_avged_x, dt);
[~, time_avged_gxx, f_range] = linearspectrum2powerspectraldensity(time_avged_X, dt);

end