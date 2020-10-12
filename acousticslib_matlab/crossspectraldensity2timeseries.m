function [time_series, t_range] = crossspectraldensity2timeseries(Sxy, dt)
N = length(Sxy);
shift_amount = 1 - ceil(N/2);
Sxy = circshift(Sxy, shift_amount);

time_series = ifft(Sxy)/dt;
time_series = circshift(time_series, shift_amount);

t_range = (0:(N - 1)).*dt;
t_range = t_range - (ceil(N/2) - 1)*dt;
end