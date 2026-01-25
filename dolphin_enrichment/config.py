# config.py
# Global configuration for Dolphin Enrichment Project

# I²C bus ID (5 = current Raspberry Pi board, 1 = default on new board)
I2C_BUS_ID = 5

# Future global settings can live here too, e.g.:
# LOG_FILE_PATH = "/home/dep/dolphin_enrichment/logs/events.log"
DEBUG_MODE = True

# Available adresses for all I2C devices
I2C_ADDRESS_RANGE = [x for x in range(0x08, 0x08 + 17)]