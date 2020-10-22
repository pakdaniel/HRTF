from numpy import pi, log, square, power
def lin_sine_sweep(t, T_p, f1, f2):
    return 2*pi*( (((f2 - f1)/(2*T_p)) * square(t)) + f1*t)

def log_sine_sweep(t, T_p, f1, f2):
    return 2*pi*(( f1*T_p* power((f2/f1)^(t/T_p)))/(log(f2/f1)) - (f1*T_p)/(log(f2/f1)))