"""
PuppyAPT Waveform Generator

Responsible only for creating audio samples.
"""

import numpy as np


SAMPLE_RATE = 44100


def create_tone(
    frequency,
    duration,
    amplitude=1.0
):
    """
    Generate a sine wave.
    """

    samples = int(
        SAMPLE_RATE * duration
    )

    time = np.arange(samples)

    waveform = amplitude * np.sin(
        2 *
        np.pi *
        frequency *
        time /
        SAMPLE_RATE
    )

    return waveform



def combine_waveforms(parts):
    """
    Join multiple audio sections.
    """

    if not parts:
        return np.array([])

    return np.concatenate(parts)