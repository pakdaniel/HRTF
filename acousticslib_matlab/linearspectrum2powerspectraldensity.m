function [Sxx, Gxx, Gxx_f_range] = linearspectrum2powerspectraldensity(X, dt)
N = length(X);
sampling_frequency = 1/dt;
sample_time = N*dt;

Sxx = (X.*conj(X))/sample_time;

df = 1/(N*dt);
f_range = (0:(N - 1)).*df;
shifted_frequency_range = f_range - (ceil(N/2) - 1)*df;

zero_index = floor((N+1)/2);
Gxx(1) = Sxx(zero_index);
Gxx(2:length(Sxx)-(zero_index-1)) = 2*Sxx(zero_index+1:end);

if shifted_frequency_range(end) == sampling_frequency/2
    Gxx(end) = Gxx(end)/2;
end

Gxx_f_range = shifted_frequency_range(zero_index:end);
end