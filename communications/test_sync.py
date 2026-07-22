import numpy as np
from scipy.io import wavfile
from apt_sync import create_sync_tone

SAMPLE_RATE = 44100

sync = create_sync_tone()

wavfile.write(
    "PUPPYSAT_SYNC.wav",
    SAMPLE_RATE,
    sync
)

print("Created PUPPYSAT_SYNC.wav")
print("Samples:", len(sync))