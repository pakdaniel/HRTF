function [time_series, t_range] = linearspectrum2timeseries(X, dt)
N = length(X);
shift_amount = 1 - ceil(N/2);
X = circshift(X, shift_amount);
time_series = ifft(X)/dt;
t_range = (0:(N - 1)).*dt;
end