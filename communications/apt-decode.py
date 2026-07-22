from pathlib import Path
import numpy as np

from scipy.io import wavfile
from PIL import Image


SAMPLE_RATE = 44100


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
    4 tones x .1 seconds
    """

    sync_samples = int(
        SAMPLE_RATE *
        (4 * 0.05)
    )

    calibration_samples = int(
        SAMPLE_RATE *
        (4 * 0.1)
    )


    return (
        sync_samples +
        calibration_samples
    )



def frequency_to_brightness(freq):

    """
    Reverse of encoder mapping

    1500 Hz = black
    2300 Hz = white
    """

    pixel = (
        (freq - 1500)
        /
        800
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


    # Encoder used 1/width seconds
    # This matches the current test encoder

    pixel_samples = int(
        SAMPLE_RATE *
        (1 / 1309)
    )


    for i in range(
        0,
        len(audio)-pixel_samples,
        pixel_samples
    ):

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

    size = int(
        np.sqrt(
            len(pixels)
        )
    )


    pixels = pixels[
        :size*size
    ]


    image = np.array(
        pixels,
        dtype=np.uint8
    )


    image = image.reshape(
        size,
        size
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