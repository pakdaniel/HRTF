function parseval_check_succeeded = parseval_sum_check(x, dt, X, df)
%% Parseval's theorem says that the sum of the square of the function is equal to the sum of the square of its transform. This theorem returns a boolean specifying if the two sums are in fact equal.
time_series_sum = sum(x.^2)*dt;
frequency_domain_sum = sum(abs(X).^2)*df;

% Floating point equality tends to report false negatives due to imprecise binary representations, so use a
% tolerance value that accounts for this
tol = eps('single');

parseval_check_succeeded = abs(time_series_sum-frequency_domain_sum) < tol;
end