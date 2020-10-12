function phi = lin_sine_sweep(t, T_p, f1, f2)
phi = 2*pi*( (((f2 - f1)/(2*T_p)) * t^2) + f1*t);
end