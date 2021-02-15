from numpy import multiply, hanning
def hann_fades(x, num_samples_per_fade):
    window = hanning(num_samples_per_fade*2).T
    x_fade = x.copy()
    x_fade[:num_samples_per_fade] = multiply(x_fade[:num_samples_per_fade], window[:num_samples_per_fade])
    x_fade[len(x_fade) - (num_samples_per_fade) :] = multiply(x_fade[len(x_fade) - (num_samples_per_fade):], window[num_samples_per_fade:])
    return x_fade