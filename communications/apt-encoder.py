from pathlib import Path
import numpy as np
from scipy.io import wavfile


SAMPLE_RATE = 44100


# Project paths
PROJECT_DIR = Path(__file__).parent
OUTPUT_DIR = PROJECT_DIR / "output"

BIN_FILE = OUTPUT_DIR / "PUPPYSAT.bin"
WAV_FILE = OUTPUT_DIR / "PUPPYSAT_APT.wav"



def create_tone(frequency, duration):

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

    print("🔊 Creating APT sync")

    pattern = [
        2400,
        2400,
        1500,
        2400
    ]

    audio = []

    for frequency in pattern:

        audio.extend(
            create_tone(
                frequency,
                0.05
            )
        )

    return np.array(
        audio,
        dtype=np.float32
    )



def create_calibration():

    print("📏 Creating calibration")

    tones = [
        1500,
        1700,
        1900,
        2100
    ]

    audio = []

    for frequency in tones:

        audio.extend(
            create_tone(
                frequency,
                0.1
            )
        )

    return np.array(
        audio,
        dtype=np.float32
    )



def load_packet(filename):

    print(
        "📡 Reading:",
        filename
    )


    with open(filename, "rb") as file:

        packet = file.read()


    print(
        "📦 Packet size:",
        len(packet),
        "bytes"
    )

    print(
        "🔎 First bytes:",
        packet[:32]
    )


    #
    # PuppySAT packet format:
    #
    # PUPSAT01
    # width uint16
    # height uint16
    # pixels
    #

    if packet[:8] == b"PUPSAT01":

        print(
            "🛰️ PuppySAT packet detected"
        )


        width = int.from_bytes(
            packet[8:10],
            "little"
        )

        height = int.from_bytes(
            packet[10:12],
            "little"
        )


        pixels = np.frombuffer(
            packet[12:],
            dtype=np.uint8
        )


        image = pixels.reshape(
            height,
            width
        )


        return image



    #
    # Fallback:
    # assume raw grayscale image
    #

    print(
        "⚠️ No packet header found"
    )

    print(
        "Using raw grayscale mode"
    )


    pixels = np.frombuffer(
        packet,
        dtype=np.uint8
    )


    # Guess square image

    size = int(
        np.sqrt(
            len(pixels)
        )
    )


    image = pixels[:size*size].reshape(
        size,
        size
    )


    return image



def brightness_to_frequency(pixel):

    return (
        1500 +
        (pixel / 255.0) * 800
    )



def encode_image(image):

    print(
        "🖼️ Encoding image:",
        image.shape
    )


    audio = []


    height, width = image.shape


    pixel_time = 1 / width


    for row_number, row in enumerate(image):

        if row_number % 50 == 0:

            print(
                "Line:",
                row_number,
                "/",
                height
            )


        for pixel in row:

            audio.extend(
                create_tone(
                    brightness_to_frequency(pixel),
                    pixel_time
                )
            )


    return np.array(
        audio,
        dtype=np.float32
    )



def create_apt_signal(bin_file):

    image = load_packet(
        bin_file
    )


    sync = create_sync_tone()

    calibration = create_calibration()

    image_audio = encode_image(
        image
    )


    print(
        "🔗 Combining signal"
    )


    return np.concatenate(
        [
            sync,
            calibration,
            image_audio
        ]
    )



def save_wav(filename, signal):

    print(
        "💾 Saving WAV"
    )


    signal = signal / np.max(
        np.abs(signal)
    )


    wavfile.write(
        filename,
        SAMPLE_RATE,
        signal.astype(
            np.float32
        )
    )



if __name__ == "__main__":

    print(
        "🐾 PuppySAT APT Encoder"
    )


    if not BIN_FILE.exists():

        raise FileNotFoundError(
            f"Missing {BIN_FILE}"
        )


    signal = create_apt_signal(
        BIN_FILE
    )


    save_wav(
        WAV_FILE,
        signal
    )


    print()
    print(
        "✅ COMPLETE"
    )

    print(
        "Created:",
        WAV_FILE
    )

    print(
        "Duration:",
        round(
            len(signal) / SAMPLE_RATE,
            2
        ),
        "seconds"
    )