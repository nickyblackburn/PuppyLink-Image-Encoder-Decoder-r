"""
PuppyLink Packet Builder
"""

import json
import struct

from checksum import generate_checksum



MAGIC = b"PUPPYLINK"


def create_packet(metadata, image_data):
    """
    Create PuppyLink binary packet.
    """


    # Convert metadata into bytes

    metadata_bytes = json.dumps(
        metadata
    ).encode("utf-8")


    # Combine payload

    payload = (
        MAGIC
        +
        struct.pack(
            ">I",
            len(metadata_bytes)
        )
        +
        metadata_bytes
        +
        image_data
    )


    # Generate checksum

    checksum = generate_checksum(
        payload
    )


    # Add checksum to end

    packet = (
        payload
        +
        struct.pack(
            ">I",
            checksum
        )
    )


    return packet