function [excitation, t_range] = generate_excitation(record_length, pulse_time, num_records, excitation_type, sampling_frequency, varargin) 

% Set random seed for reproducibility and debugging
rng(31415);

p = inputParser;
addRequired(p, 'record_length')
addRequired(p, 'pulse_time')
addRequired(p, 'num_records')
addRequired(p, 'excitation_type')
addRequired(p, 'sampling_frequency')
addOptional(p, 'SineFrequency', 0)
addOptional(p, 'SweepFrequencyHigh', 0)
addOptional(p, 'SweepFrequencyLow', 0)
parse(p, record_length, pulse_time, num_records, excitation_type, sampling_frequency, varargin{:});

f2 = p.Results.SweepFrequencyHigh;
f1 = p.Results.SweepFrequencyLow;

dt = 1/sampling_frequency;

t_range = (0:(record_length*num_records-1))*dt;
pulse_length = sampling_frequency * pulse_time;

if strcmp(excitation_type, 'impulse')
    
    pulse_length = 1;
    pulse = 1;

elseif strcmp(excitation_type, 'cw_pulse')
    % if no explicitly given sine frequency, use one full pulse.
    sine_freq = p.Results.SineFrequency;
    if ~sine_freq
       sine_freq = 1/pulse_time; 
    end
    
    pulse_t_range = linspace(0, pulse_time, pulse_length);
    pulse = sin(2*pi*sine_freq * pulse_t_range);

elseif strcmp(excitation_type, 'lin_sine_sweep')
    
    pulse_t_range = (0:pulse_length-1)*dt;
    phi = @(t) lin_sine_sweep(t, pulse_time, f1, f2);
    pulse = sin(arrayfun(phi, pulse_t_range));
    
elseif strcmp(excitation_type, 'log_sine_sweep')
    
    pulse_t_range = (0:pulse_length-1)*dt;
    phi = @(t) log_sine_sweep(t, pulse_time, f1, f2);
    pulse = sin(arrayfun(phi, pulse_t_range));

elseif strcmp(excitation_type, 'white_noise')
    X = ones(1, pulse_length);
    phase_noise = (2*pi)*rand(1,ceil(pulse_length/2 - 1));
    X(1:length(phase_noise)) = exp(1j*phase_noise);
    X( ceil(pulse_length/2 + 1) : pulse_length - (mod(pulse_length, 2) == 0)) = conj(exp(1j*flip(phase_noise)));
    [pulse, ~] = linearspectrum2timeseries(X, dt);    

elseif strcmp(excitation_type, 'pink_noise')
    df = 1/(pulse_length*dt);
    f_range = (0:(pulse_length - 1)).*df;
    shifted_frequency_range = f_range - (ceil(pulse_length/2) - 1)*df;
    X = sqrt(1./abs(shifted_frequency_range));
    inf_index = ceil(pulse_length/2);
    X(inf_index) = 1;
    phase_noise = (2*pi)*rand(1,ceil(pulse_length/2 - 1));
    X(1:length(phase_noise)) = X(1:length(phase_noise)).*exp(1j*phase_noise);
    X( ceil(pulse_length/2 + 1) : pulse_length - (mod(pulse_length, 2) == 0)) = ...
        X( ceil(pulse_length/2 + 1) : pulse_length - (mod(pulse_length, 2) == 0)).*conj(exp(1j*flip(phase_noise)));

    [pulse, ~] = linearspectrum2timeseries(X, dt);    
    
end
single_record = [pulse zeros(1, record_length - pulse_length)];
excitation = repmat(single_record, 1, num_records);
end
