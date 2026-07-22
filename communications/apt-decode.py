from pathlib import Path
import numpy as np

from scipy.io import wavfile
from PIL import Image


SAMPLE_RATE = 44100

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256

PIXEL_DURATION = 0.02

MIN_FREQ = 2000
MAX_FREQ = 6000


PROJECT_DIR = Path(__file__).parent

OUTPUT_DIR = PROJECT_DIR / "output"

WAV_FILE = OUTPUT_DIR / "PUPPYSAT_APT.wav"

IMAGE_FILE = OUTPUT_DIR / "RECOVERED_IMAGE.png"



def find_sync_end(audio):

    """
    Skip our known sync + calibration area

    Sync:
    4 tones x .05 seconds

    Calibration:
    5 tones x .1 seconds
    """


    sync_samples = int(
        SAMPLE_RATE *
        (4 * 0.05)
    )


    calibration_samples = int(
        SAMPLE_RATE *
        (5 * 0.1)
    )


    return (
        sync_samples +
        calibration_samples
    )



def frequency_to_brightness(freq):

    """
    Reverse of encoder mapping

    2000 Hz = black
    6000 Hz = white
    """


    pixel = (
        (freq - MIN_FREQ)
        /
        (MAX_FREQ - MIN_FREQ)
        *
        255
    )


    return int(
        np.clip(
            pixel,
            0,
            255
        )
    )



def detect_frequency(samples):

    """
    Measure dominant frequency
    """


    fft = np.fft.rfft(
        samples
    )


    frequencies = np.fft.rfftfreq(
        len(samples),
        1 / SAMPLE_RATE
    )


    index = np.argmax(
        np.abs(fft)
    )


    return frequencies[index]



def decode_image(audio):

    print(
        "🔊 Decoding audio..."
    )


    pixels = []


    pixel_samples = int(
        SAMPLE_RATE *
        PIXEL_DURATION
    )


    total_pixels = (
        IMAGE_WIDTH *
        IMAGE_HEIGHT
    )


    for i in range(
        0,
        len(audio) - pixel_samples + 1,
        pixel_samples
    ):

        if len(pixels) >= total_pixels:

            break


        chunk = audio[
            i:i+pixel_samples
        ]


        freq = detect_frequency(
            chunk
        )


        pixel = frequency_to_brightness(
            freq
        )


        pixels.append(
            pixel
        )


    return pixels



def save_image(pixels):

    expected_pixels = (
        IMAGE_WIDTH *
        IMAGE_HEIGHT
    )


    if len(pixels) < expected_pixels:

        print(
            "⚠️ Missing pixels:",
            expected_pixels - len(pixels)
        )


        pixels.extend(
            [0] *
            (
                expected_pixels -
                len(pixels)
            )
        )


    pixels = pixels[
        :expected_pixels
    ]


    image = np.array(
        pixels,
        dtype=np.uint8
    )


    image = image.reshape(
        IMAGE_HEIGHT,
        IMAGE_WIDTH
    )


    img = Image.fromarray(
        image,
        "L"
    )


    img.save(
        IMAGE_FILE
    )


    print(
        "🖼️ Saved:",
        IMAGE_FILE
    )



if __name__ == "__main__":

    print(
        "🐾 PuppySAT APT Decoder"
    )


    rate, audio = wavfile.read(
        WAV_FILE
    )


    audio = audio.astype(
        np.float32
    )


    start = find_sync_end(
        audio
    )


    image_audio = audio[
        start:
    ]


    pixels = decode_image(
        image_audio
    )


    save_image(
        pixels
    )


    print(
        "✅ Decode complete"
    )