from PIL import Image

from overlay import add_map_overlay
from metadata import create_metadata
from compression import compress_image
from packet import create_packet


INPUT_IMAGE = "input/earth.png"
OUTPUT_PACKET = "output/PUPPYSAT_IMAGE.bin"


# ==========================
# Load Image
# ==========================

image = Image.open(INPUT_IMAGE)


# ==========================
# Add Mission Overlay
# ==========================

image = add_map_overlay(
    image,
    satellite_id="PUPPYSAT-001",
    latitude=42.3,
    longitude=-83.0,
    timestamp="2026-07-22"
)


# ==========================
# Generate Metadata
# ==========================

metadata = create_metadata(
    image_id="IMG-00001",
    width=image.width,
    height=image.height,
    sensor_type="RGB"
)


# ==========================
# Compress Image
# ==========================

image_data = compress_image(
    image
)


# ==========================
# Build PuppyLink Packet
# ==========================

packet = create_packet(
    metadata,
    image_data
)


# ==========================
# Save Satellite Data File
# ==========================

with open(
    OUTPUT_PACKET,
    "wb"
) as file:

    file.write(packet)


print("PuppySat Image Packet Created!")
print(f"Size: {len(packet)} bytes")