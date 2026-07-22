from packet_reader import read_packet


packet = read_packet(
    "../output/PUPPYSAT_IMAGE.bin"
)


print(packet["metadata"])

print(
    "Image bytes:",
    len(packet["image_data"])
)

print(
    "Checksum:",
    packet["checksum"]
)