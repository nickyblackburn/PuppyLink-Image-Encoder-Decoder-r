from scipy.io import wavfile
import numpy as np

rate, audio = wavfile.read(
    "output/PUPPYSAT_APT.wav"
)

print("Sample rate:", rate)
print("Samples:", len(audio))
print("Duration:", len(audio)/rate)

# Look at first tone after start
chunk = audio[:2205]

fft = np.fft.rfft(chunk)

freqs = np.fft.rfftfreq(
    len(chunk),
    1/rate
)

peak = freqs[np.argmax(abs(fft))]

print("First frequency:", peak)