import numpy as np

def acousticmag2db(signal_wu):
    return (20. * np.log10(signal_wu))/2

def acousticdb2mag(signal_db):
    return 10. ** (signal_db*2 / 20.)

def pressuremag2db(signal_wu):
    return (20. * np.log10(signal_wu))/2