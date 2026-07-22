"""
PuppyLink Image Compression

Handles conversion of images into compressed binary payloads.
"""

import io
import zlib
from PIL import Image


COMPRESSION_LEVEL = 9


def compress_image(image: Image.Image) -> bytes:
    """
    Compress a PIL image into binary data.
    """

    # Store image temporarily in memory

    buffer = io.BytesIO()


    # Save as PNG

    image.save(
        buffer,
        format="PNG"
    )


    # Get raw image bytes

    image_bytes = buffer.getvalue()


    # Compress bytes

    compressed = zlib.compress(
        image_bytes,
        level=COMPRESSION_LEVEL
    )


    return compressed