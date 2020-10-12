function Hc = Hc_filter(omega)
omega_1 = 12194.22*2*pi;
omega_2 = 20.598997*2*pi;
Hc = (1.0072*(1j*omega).^2)*(omega_1^2)./(((omega_1 + 1j*omega).^2) .* (omega_2 + 1j*omega).^2);
end