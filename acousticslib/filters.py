from numpy import pi, square, multiply, divide
def Ha_filter(omega):
    omega_3 = 107.65265*2*pi
    omega_4 = 737.86223*2*pi
    return divide(multiply(Hc_filter(omega),( 1.25*square(1j*omega)) ), multiply( (omega_3 + 1j*omega),(omega_4 + 1j*omega) ))
    
def Hc_filter(omega):
    omega_1 = 12194.22*2*pi
    omega_2 = 20.598997*2*pi
    return divide((1.0072*square(1j*omega))*(omega_1^2), multiply((square(omega_1 + 1j*omega)) , square(omega_2 + 1j*omega)))