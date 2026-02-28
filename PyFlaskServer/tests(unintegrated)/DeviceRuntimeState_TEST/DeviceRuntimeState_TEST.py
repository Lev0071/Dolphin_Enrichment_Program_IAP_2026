from dataclasses import dataclass, asdict
# from app.utils.layout_manager import load_layout_devices
from layout_manager import load_layout_devices
from pprint import pprint
from typing import Dict, List, Optional, Tuple,Any
import os
# print(os.path.abspath(__file__));exit(1)

devices = load_layout_devices()
# pprint(devices)

def display_dict_contents(devices):
    for i, dev in enumerate(devices, 1):
        print(f"\nDevice {i}")
        print("-" * 30)
        for key, value in dev.items():
            print(f"{key:12}: {value}")
            
display_dict_contents(devices) 

@dataclass
class DeviceRuntimeState:
    # identity / config
    uid: str
    id: str
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
        
#-------------------------------------------------------------
runtime_states = []

for dev in devices:
    device_state = DeviceRuntimeState(
        # identity / config
        uid=dev["uid"],
        id=dev["id"],
        type=dev["type"],
        name=dev["name"],
        i2c_address=dev["i2c_address"],
    
        # layout/style (config)
        x_pct=dev["x_pct"],
        y_pct=dev["y_pct"],
        color=dev["color"],
        shape=dev["shape"],
        icon=dev["icon"],
    )
    runtime_states.append(device_state.to_dict())

print("===================") 
print("Show runtime states")   
print("===================") 
display_dict_contents(runtime_states) 