"""
PuppyLink Metadata System

Creates spacecraft metadata attached to image payloads.
"""

from datetime import datetime, timezone


def create_metadata(
        image_id,
        width,
        height,
        sensor_type="RGB",
        satellite_id="PUPPYSAT-001"
):

    metadata = {

        # =====================
        # Mission Identity
        # =====================

        "mission": {
            "satellite_id": satellite_id,
            "mission_name": "PuppySat-1",
            "mission_type": "Earth Observation",
            "protocol": "PuppyLink",
            "protocol_version": "0.1"
        },


        # =====================
        # Image Information
        # =====================

        "image": {

            "image_id": image_id,

            "sensor": sensor_type,

            "resolution": {
                "width": width,
                "height": height
            },

            "color_mode": "RGB",

            "data_type": "IMAGE",

            "compression": "PENDING"
        },


        # =====================
        # Capture Information
        # =====================

        "capture": {

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "location": {

                "latitude": None,

                "longitude": None,

                "altitude_km": None
            }
        },


        # =====================
        # Orbit Information
        # =====================

        "orbit": {

            "orbit_type": "LEO",

            "altitude_km": 400,

            "velocity_km_s": None,

            "orbit_number": None

        },


        # =====================
        # Spacecraft Health
        # =====================

        "telemetry": {

            "battery": {

                "percentage": None,

                "voltage": None,

                "temperature": None

            },


            "power": {

                "solar_generation": None,

                "power_mode": "NORMAL"

            },


            "thermal": {

                "temperature_internal": None,

                "temperature_external": None

            },


            "storage": {

                "capacity": "1TB",

                "used": None,

                "health": "UNKNOWN"

            }

        },


        # =====================
        # Network Information
        # =====================

        "network": {

            "source_satellite": satellite_id,

            "destination": "GROUND",

            "network_role": "LEO_RELAY",

            "hop_count": 0,

            "relay_enabled": True,

            "relay_path": []

        },


        # =====================
        # Communication Status
        # =====================

        "communications": {

            "fm_repeater": {

                "enabled": True,

                "status": "READY"

            },


            "digital_link": {

                "status": "READY",

                "mode": "PUPPYLINK"

            },


            "apt_ng": {

                "enabled": True,

                "status": "READY"

            }

        },


        # =====================
        # Data Integrity
        # =====================

        "security": {

            "checksum": None,

            "packet_status": "CREATED",

            "error_correction": True

        }

    }


    return metadata