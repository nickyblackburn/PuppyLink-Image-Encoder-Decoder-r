from PIL import Image, ImageDraw, ImageFont


def add_map_overlay(
        image,
        satellite_id="PUPPYSAT-001",
        latitude=None,
        longitude=None,
        timestamp=None
):

    draw = ImageDraw.Draw(image)

    width, height = image.size


    # Draw latitude/longitude grid

    for x in range(0, width, width // 6):

        draw.line(
            [(x,0),(x,height)],
            fill="white",
            width=2
        )


    for y in range(0, height, height // 6):

        draw.line(
            [(0,y),(width,y)],
            fill="white",
            width=2
        )


    # Add mission information

    text = f"""
PuppySat-1
SAT: {satellite_id}
LAT: {latitude}
LON: {longitude}
TIME: {timestamp}
"""


    draw.rectangle(
        (10,10,350,120),
        fill="black"
    )


    draw.text(
        (20,20),
        text,
        fill="white"
    )


    return image