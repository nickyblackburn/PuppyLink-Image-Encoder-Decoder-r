import numpy as np
from PIL import Image
from scipy.io import wavfile


SAMPLE_RATE = 44100


# How long each APT section lasts
SYNC_DURATION = 0.05
CALIBRATION_DURATION = 0.5


def create_tone(frequency, duration):
    """
    Create a sine wave tone
    """

    samples = np.arange(
        int(SAMPLE_RATE * duration)
    )

    return np.sin(
        2 *
        np.pi *
        frequency *
        samples /
        SAMPLE_RATE
    )



def create_sync_tone():
    """
    APT frame sync pattern
    """

    pattern = [
        2400,
        2400,
        1500,
        2400
    ]

    waveform = []

    for frequency in pattern:

        tone = create_tone(
            frequency,
            SYNC_DURATION
        )

        waveform.extend(tone)


    return np.array(
        waveform,
        dtype=np.float32
    )



def create_calibration():

    """
    Calibration tones.
    Real APT uses calibration bars.
    """

    tones = [
        1500,
        1700,
        1900,
        2100
    ]

    waveform = []

    for freq in tones:

        waveform.extend(
            create_tone(
                freq,
                CALIBRATION_DURATION / len(tones)
            )
        )


    return np.array(
        waveform,
        dtype=np.float32
    )



def load_image(path):

    """
    Convert image into grayscale
    """

    img = Image.open(path)

    img = img.convert(
        "L"
    )

    return np.array(img)



def pixel_to_frequency(pixel):

    """
    Convert brightness to APT audio frequency

    dark  = low tone
    bright = high tone
    """

    return (
        1500 +
        (pixel / 255) * 600
    )



def encode_image(image):

    """
    Convert image pixels into audio
    """

    waveform = []


    height, width = image.shape


    for row in image:

        for pixel in row:

            freq = pixel_to_frequency(
                pixel
            )

            waveform.extend(
                create_tone(
                    freq,
                    1 / width
                )
            )


    return np.array(
        waveform,
        dtype=np.float32
    )



def create_frame(image_path):

    image = load_image(
        image_path
    )


    sync = create_sync_tone()

    calibration = create_calibration()

    image_audio = encode_image(
        image
    )


    return np.concatenate(
        [
            sync,
            calibration,
            image_audio
        ]
    )



def save_wav(filename, audio):

    """
    Save final satellite signal
    """

    # prevent clipping

    audio = audio / np.max(
        np.abs(audio)
    )


    wavfile.write(
        filename,
        SAMPLE_RATE,
        audio.astype(
            np.float32
        )
    )



if __name__ == "__main__":

    print(
        "🐾 PuppySAT APT Encoder"
    )


    signal = create_frame(
        "image.png"
    )


    save_wav(
        "PUPPYSAT_APT.wav",
        signal
    )


    print(
        "🛰️ Created PUPPYSAT_APT.wav"
    )

    print(
        "Samples:",
        len(signal)
    )

    print(
        "Duration:",
        len(signal) / SAMPLE_RATE,
        "seconds"
    )