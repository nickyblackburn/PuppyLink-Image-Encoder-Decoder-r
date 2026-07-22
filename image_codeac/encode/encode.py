from PIL import Image

from overlay import add_map_overlay
from metadata import create_metadata


image = Image.open(
    "input/earth.png"
)


image = add_map_overlay(
    image,
    satellite_id="PUPPYSAT-001",
    latitude=42.3,
    longitude=-83.0,
    timestamp="2026-07-22"
)


metadata = create_metadata(
    image_id="IMG-00001",
    width=image.width,
    height=image.height,
    sensor_type="RGB"
)


image.save(
    "output/processed_image.png"
)

print(metadata)
print("Encoder stage complete!")