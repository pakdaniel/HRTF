function [Sxy, Gxy, Gxy_f_range] = linearspectrum2crossspectraldensity(X1, X2, dt)
assert(length(X1) == length(X2));
N = length(X1);
sampling_frequency = 1/dt;
sample_time = N*dt;

Sxy = (X1.*conj(X2))/sample_time;

df = 1/(N*dt);
f_range = (0:(N - 1)).*df;
shifted_frequency_range = f_range - (ceil(N/2) - 1)*df;

zero_index = floor((N+1)/2);
Gxy(1) = Sxy(zero_index);
Gxy(2:length(Sxy)-(zero_index-1)) = 2*Sxy(zero_index+1:end);

if shifted_frequency_range(end) == sampling_frequency/2
    Gxy(end) = Gxy(end)/2;
end

Gxy_f_range = shifted_frequency_range(zero_index:end);
end