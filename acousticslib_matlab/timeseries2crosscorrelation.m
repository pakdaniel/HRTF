function [Rxy, Rxy_t_range] = timeseries2crosscorrelation(x1, x2, dt)
[X1, ~] = timeseries2linearspectrum(x1, dt);
[X2, ~] = timeseries2linearspectrum(x2, dt);
[Sxy, ~, ~] = linearspectrum2crossspectraldensity(X1, X2, dt);
[Rxy, Rxy_t_range] = crossspectraldensity2timeseries(Sxy, dt);
end