function [linear_spectrum, shifted_frequency_range] = timeseries2linearspectrum(x, dt)
N = length(x);
X = fft(x)*dt;

shift_amount = ceil(N/2) - 1;
linear_spectrum = circshift(X, shift_amount);

df = 1/(N*dt);
f_range = (0:(N - 1)).*df;
shifted_frequency_range = f_range - (ceil(N/2) - 1)*df;
end