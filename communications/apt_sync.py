import numpy as np

SAMPLE_RATE = 44100


def create_sync_tone():

    pattern = [
        2400,
        2400,
        1500,
        2400
    ]

    waveform = []


    for frequency in pattern:

        samples = np.arange(
            int(SAMPLE_RATE * 0.05)
        )

        tone = np.sin(
            2 *
            np.pi *
            frequency *
            samples /
            SAMPLE_RATE
        )

        waveform.extend(
            tone
        )


    return np.array(
        waveform,
        dtype=np.float32
    )