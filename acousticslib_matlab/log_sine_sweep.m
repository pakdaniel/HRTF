function phi = log_sine_sweep(t, T_p, f1, f2)
phi = 2*pi*(( f1*T_p* (f2/f1)^(t/T_p))/(log(f2/f1)) - (f1*T_p)/(log(f2/f1)));
end