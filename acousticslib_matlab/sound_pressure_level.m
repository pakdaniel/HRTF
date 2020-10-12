function spl = sound_pressure_level(x)
p_ref = 20*10^(-6);
spl = 20*log10(time_series_rms(x)/p_ref) ;
end