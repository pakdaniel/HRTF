import numpy as np
from math import isclose
def parseval_sum_check(x, dt, X, df):
    '''
    Parseval's theorem says that the sum of the square of the function
    is equal to the sum of the square of its transform.
    This theorem returns a boolean specifying if the two sums are in fact equal.
    '''
    time_series_sum = sum(np.square(x))*dt
    frequency_domain_sum = sum(np.square(np.abs(X)))*df

    # Floating point equality tends to report false negatives due to imprecise binary representations, so use a
    # tolerance value that accounts for this

    return isclose(time_series_sum, frequency_domain_sum)
    