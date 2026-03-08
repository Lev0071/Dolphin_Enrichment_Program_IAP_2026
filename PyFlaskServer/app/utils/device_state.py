# PyFlaskServer/app/utils/device_state.py

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
import time

# We will reuse your existing XML loader (layout_manager.py)
# It already returns devices like:
# {id,type,name,i2c_address,x_pct,y_pct,color,shape,icon}
from utils.layout_manager import load_layout_devices


@dataclass
class DeviceRuntimeState:
    # identity / config
    uid: str                 # primary key
    id: str                  # user label
    type: str
    name: str
    i2c_address: str  # keep as string e.g. "0x08" for now

    # layout/style (config)
    x_pct: float
    y_pct: float
    color: str
    shape: str
    icon: str

    # classification flags
    configured: bool = True
    detected: bool = False

    # professor scope: two actions / two states
    enabled: bool = False   # toggle
    pressed: bool = False   # momentary

    # optional helpful metadata
    last_updated_ts: float = 0.0
    last_action: str = ""   # e.g. "toggle_on", "press", "release"

    def to_dict(self) -> dict:
        return asdict(self)


class DeviceStateStore:
    """
    In-memory source of truth for runtime device states.
    XML is configuration. This store merges XML + detection + UI actions.
    """

    def __init__(self) -> None:
        self._devices: Dict[str, DeviceRuntimeState] = {}
        self.reload_from_xml()

    # -----------------------------
    # Loading / merging configuration
    # -----------------------------
    def reload_from_xml(self) -> None:
        """
        Rebuild store based on XML config, but keep existing runtime flags if possible.
        """
        configured_devices = load_layout_devices()  # list[dict]
        new_map: Dict[str, DeviceRuntimeState] = {}

        for d in configured_devices:
            dev_id = d.get("id", "").strip()
            if not dev_id:                                 # is it falsy ie (None,"" (empty string),0,0.0,,False,[],{} )
                continue

            dev_uid = d.get("uid", "").strip()
            if not dev_uid:                                 # is it falsy ie (None,"" (empty string),0,0.0,,False,[],{} )
                continue

            prev = self._devices.get(dev_uid)

            # preserve runtime state if already existed
            enabled = prev.enabled if prev else False
            pressed = prev.pressed if prev else False
            detected = prev.detected if prev else False

            new_map[dev_uid] = DeviceRuntimeState(
                uid=dev_uid,
                id=dev_id,
                type=d.get("type", "button"),
                name=d.get("name", dev_id),
                i2c_address=d.get("i2c_address", "-"),
                x_pct=float(d.get("x_pct", 0.5)),
                y_pct=float(d.get("y_pct", 0.5)),
                color=d.get("color", "#0d6efd"),
                shape=d.get("shape", "rect"),
                icon=d.get("icon", "none"),
                configured=True,
                detected=detected,
                enabled=enabled,
                pressed=pressed,
                last_updated_ts=time.time() if prev else 0.0,
                last_action=prev.last_action if prev else "",
            )

        self._devices = new_map

    def merge_detected_addresses(self, detected_addrs: List[str]) -> None:
        """
        Mark devices as detected based on I2C address list.
        For now detected_addrs can come from a MOCK scan.
        """
        detected_set = set(detected_addrs)

        # update configured devices detection flag
        for dev in self._devices.values():
            dev.detected = (dev.i2c_address in detected_set)

    # -----------------------------
    # Queries
    # -----------------------------
    def all_devices(self) -> List[DeviceRuntimeState]:
        return list(self._devices.values())

    def get(self, device_uid: str) -> Optional[DeviceRuntimeState]:
        return self._devices.get(device_uid)

    def snapshot_for_ui(self) -> List[dict]:
        """
        Return JSON-friendly list for canvas/table rendering.
        """
        return [d.to_dict() for d in self.all_devices()]

    # -----------------------------
    # Actions (professor requirement)
    # -----------------------------
    def toggle(self, device_uid: str,device_id: str) -> Tuple[bool, str]:
        dev = self.get(device_uid)
        if not dev:
            return False, f"Unknown device_uid='{device_uid}' (label='{device_id}')"

        dev.enabled = not dev.enabled
        dev.last_updated_ts = time.time()
        dev.last_action = "toggle_on" if dev.enabled else "toggle_off"
        return True, dev.last_action

    def press(self, device_uid: str,device_id: str) -> Tuple[bool, str]:
        dev = self.get(device_uid)
        if not dev:
            return False, f"Unknown device_uid='{device_uid}' (label='{device_id}')"

        dev.pressed = True
        dev.last_updated_ts = time.time()
        dev.last_action = "press"
        return True, dev.last_action

    def release(self, device_uid: str,device_id: str) -> Tuple[bool, str]:
        dev = self.get(device_uid)
        if not dev:
            return False, f"Unknown device_uid='{device_uid}' (label='{device_id}')"

        dev.pressed = False
        dev.last_updated_ts = time.time()
        dev.last_action = "release"
        return True, dev.last_action

        # https://chatgpt.com/c/699fa926-1f64-839f-9858-a4380e483238