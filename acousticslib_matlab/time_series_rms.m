function rms = time_series_rms(x)
rms = sqrt(sum(x.^2)/length(x));
end