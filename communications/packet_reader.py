"""
PuppyLink Packet Reader

Extracts metadata and image data
from PUPPYSAT_IMAGE.bin
"""

import json
import struct


MAGIC = b"PUPPYLINK"



def read_packet(filename):

    with open(
        filename,
        "rb"
    ) as file:

        data = file.read()


    # Check packet identity

    if not data.startswith(MAGIC):

        raise ValueError(
            "Not a PuppyLink packet"
        )


    index = len(MAGIC)


    # Read metadata length

    metadata_length = struct.unpack(
        ">I",
        data[index:index+4]
    )[0]


    index += 4


    # Extract metadata

    metadata_bytes = data[
        index:
        index + metadata_length
    ]


    metadata = json.loads(
        metadata_bytes.decode("utf-8")
    )


    index += metadata_length


    # Extract image payload

    image_data = data[index:-4]


    # Last 4 bytes are checksum

    checksum = struct.unpack(
        ">I",
        data[-4:]
    )[0]


    return {
        "metadata": metadata,
        "image_data": image_data,
        "checksum": checksum
    }