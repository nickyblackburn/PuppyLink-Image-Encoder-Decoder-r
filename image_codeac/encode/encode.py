from PIL import Image
import os

from overlay import add_map_overlay
from metadata import create_metadata
from compress import compress_image
from packet import create_packet


INPUT_IMAGE = "test.png"
OUTPUT_PACKET = "output/PUPPYSAT_IMAGE.bin"


# ==========================
# Create Output Folder
# ==========================

output_folder = os.path.dirname(OUTPUT_PACKET)

if output_folder:
    os.makedirs(
        output_folder,
        exist_ok=True
    )


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
print(f"Output: {OUTPUT_PACKET}")
print(f"Size: {len(packet)} bytes")