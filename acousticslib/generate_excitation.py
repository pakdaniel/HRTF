import numpy as np
from acousticslib.sweeps import lin_sine_sweep, log_sine_sweep
from math import ceil
from acousticslib.domain_conversions import linearspectrum2timeseries

def generate_excitation(record_length, pulse_time, num_records, excitation_type, sampling_frequency,
    SineFrequency = 0,
    SweepFrequencyHigh = 0,
    SweepFrequencyLow = 0):

    # Set random seed for reproducibility and debugging
    np.random.seed(31415)

    f2 = SweepFrequencyHigh
    f1 = SweepFrequencyLow

    dt = 1/sampling_frequency

    t_range = np.arange((record_length*num_records))*dt
    pulse_length = sampling_frequency * pulse_time

    if excitation_type =='impulse':
        
        pulse_length = 1
        pulse = 1

    elif excitation_type == 'cw_pulse':
        # if no explicitly given sine frequency, use one full pulse.
        sine_freq = SineFrequency
        if not sine_freq:
            sine_freq = 1/pulse_time 
        
        pulse_t_range = np.linspace(0, pulse_time, pulse_length)
        pulse = np.sin(2*np.pi*sine_freq * pulse_t_range)

    elif excitation_type == 'lin_sine_sweep':
        pulse_t_range = np.arange(0, pulse_length)*dt
        pulse = np.sin(lin_sine_sweep(pulse_t_range, pulse_time, f1, f2))
        
    elif excitation_type == 'log_sine_sweep':
        
        pulse_t_range = np.arange(pulse_length)*dt
        pulse = np.sin(log_sine_sweep(pulse_t_range, pulse_time, f1, f2))

    elif excitation_type== 'white_noise':
        X = np.ones((1, pulse_length))

        phase_noise = (2*np.pi)*np.uniform((1,ceil(pulse_length/2 - 1)))

        X[:len(phase_noise)] = np.exp(1j*phase_noise)
        X[ ceil(pulse_length/2 + 1) - 1 : pulse_length - ((pulse_length % 2) == 0)] = np.conj(np.exp(1j*np.flip(phase_noise)))
        pulse, _ = linearspectrum2timeseries(X, dt)    

    elif excitation_type== 'pink_noise':
        df = 1/(pulse_length*dt)
        f_range = np.arange(pulse_length)*df
        shifted_frequency_range = f_range - (ceil(pulse_length/2) - 1)*df
        X = np.sqrt(np.divide(1, np.abs(shifted_frequency_range)))
        inf_index = ceil(pulse_length/2) - 1
        X[inf_index] = 1
        phase_noise = (2*np.pi)*np.uniform((1,ceil(pulse_length/2 - 1)))
        X[:len(phase_noise)] = X[:len(phase_noise)]*np.exp(1j*phase_noise)
        X[ceil(pulse_length/2 + 1) - 1: pulse_length - ((pulse_length % 2) == 0)] = np.multiply(X[ ceil(pulse_length/2 + 1) - 1 : pulse_length - ((pulse_length % 2) == 0)], np.conj(np.exp(1j*np.flip(phase_noise))))

        pulse, _ = linearspectrum2timeseries(X, dt)    
       
    single_record = np.concatenate((pulse, np.zeros(1, record_length - pulse_length)), axis=1)
    excitation = np.matlib.repmat(single_record, 1, num_records)
    return excitation, t_range