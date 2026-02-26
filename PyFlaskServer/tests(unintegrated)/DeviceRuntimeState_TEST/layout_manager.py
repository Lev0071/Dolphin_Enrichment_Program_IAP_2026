import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).parent
LAYOUT_FILE = BASE_DIR / "devices_layout.xml"

def load_layout_devices():
    """
    Try to load existing layout.
    If file/folder doesn't exist or is empty/bad, return empty list.
    """
    if not LAYOUT_FILE.exists():
        return []

    try:
        tree = ET.parse(LAYOUT_FILE)
        root = tree.getroot()
    except ET.ParseError:
        return []  # file exists but empty or corrupted

    devices_el = root.find("devices")
    if devices_el is None:
        return []

    devices = []
    for dev in devices_el.findall("device"):
        devices.append({
            "id": dev.get("id"),
            "type": dev.get("type"),
            "name": dev.findtext("name", ""),
            "i2c_address": dev.findtext("i2c_address", ""),  # ← fixed key name
            "x_pct": float(dev.findtext("position/x_pct", "0") or 0),
            "y_pct": float(dev.findtext("position/y_pct", "0") or 0),
            "color": dev.findtext("style/color", "#0d6efd"),
            "shape": dev.findtext("style/shape", "rect"),
            "icon": dev.findtext("style/icon", "none"),
        })
    return devices