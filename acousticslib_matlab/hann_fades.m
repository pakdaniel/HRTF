function x_fade = hann_fades(x, num_samples_per_fade)
window = hann(num_samples_per_fade*2).';
x_fade = x;
x_fade(1:num_samples_per_fade) = x_fade(1:num_samples_per_fade).*window(1:num_samples_per_fade);
x_fade(length(x_fade) - (num_samples_per_fade - 1) : end) = x_fade(length(x_fade) - (num_samples_per_fade - 1) : end).*window(num_samples_per_fade + 1 : end);
end