function Ha = Ha_filter(omega)
omega_3 = 107.65265*2*pi;
omega_4 = 737.86223*2*pi;
Ha = Hc_filter(omega).*( 1.25*(1j*omega).^2 )/( (omega_3 + 1j*omega).*(omega_4 + 1j*omega) );
end