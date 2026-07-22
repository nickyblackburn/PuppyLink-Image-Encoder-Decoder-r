"""
PuppyLink Checksum System
"""

import zlib


def generate_checksum(data: bytes):
    """
    Generate CRC32 checksum.
    """

    checksum = zlib.crc32(data)

    return checksum


def verify_checksum(data: bytes, checksum):
    """
    Verify data integrity.
    """

    return zlib.crc32(data) == checksum