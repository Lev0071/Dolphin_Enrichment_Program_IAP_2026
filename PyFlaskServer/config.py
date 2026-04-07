# PyFlaskServer/config.py
# Global configuration for Dolphin Enrichment Project

from enum import Enum

class InteractionMode(str, Enum):
    MOMENTARY = "momentary"
    LATCHING = "latching"

class SystemMode(str,Enum):
    SOFTWARE = "software"
    HARDWARE = "hardware"
    HYBRID = "hybrid"

# -----------------------------
# Runtime mode selection
# -----------------------------
# Windows development machine:
#   use SOFTWARE
#
# Raspberry Pi:
#   use SOFTWARE, HARDWARE, or HYBRID depending on test/deployment need
SYSTEM_MODE = SystemMode.SOFTWARE

# Default interaction behavior for the UI / runtime logic
INTERACTION_MODE = InteractionMode.MOMENTARY

# -----------------------------
# I2C configuration
# -----------------------------
# I²C bus ID (5 = current Raspberry Pi board, 1 = default on new board)
I2C_BUS_ID = 5


# Available adresses for all I2C devices
I2C_ADDRESS_RANGE = [x for x in range(0x08, 0x08 + 17)]

# -----------------------------
# General app config
# -----------------------------
DEBUG_MODE = True


# LOG_FILE_PATH = "/home/dep/dolphin_enrichment/logs/events.log"