# app/utils/layout_manager.py
import xml.etree.ElementTree as ET
from pathlib import Path
from uuid import uuid4

BASE_DIR = Path(__file__).resolve().parent.parent.parent   # dolphin_enrichment/
LAYOUT_DIR = BASE_DIR / "ui_layout"
LAYOUT_FILE = LAYOUT_DIR / "devices_layout.xml"

def generate_id()->str:
    return uuid4().hex

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
        uid = dev.get("uid") or generate_id()

        devices.append({
            "uid": uid,
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
