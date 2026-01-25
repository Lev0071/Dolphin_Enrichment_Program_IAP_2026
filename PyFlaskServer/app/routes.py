# PyFlaskServer/app/routes.py
import os
import xml.etree.ElementTree as ET
from .utils.layout_manager import load_layout_devices, LAYOUT_FILE, LAYOUT_DIR
from pathlib import Path
from flask import Blueprint, render_template, redirect, url_for,flash,request,jsonify
from .hardware.i2c_manager import i2c
from config import I2C_ADDRESS_RANGE,I2C_BUS_ID

# Create a blueprint called "main"
bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    """
    Home page route (Current version iv).
    For now, just render a simple template to confirm everything works.
    Later you can point this to homepage_iteration_three.html or another page.
    """
    # Adjust this to whatever template you want as your "home" page:
    devices = load_layout_devices()
    return render_template("homepage_iteration_iv_v2.html", current_devices=devices)

@bp.route("/previous")
def previous():
    """
    Home page route (Old version iii).
    For now, just render a simple template to confirm everything works.
    Later you can point this to homepage_iteration_three.html or another page.
    """
    # Adjust this to whatever template you want as your "home" page:
    return render_template("homepage_iteration_three.html")

@bp.route("/dashboard")
def dashboard():
    # try to read a byte from the known addresses you saw: 0x08, 0x09, 0x0A
    available_addrs = I2C_ADDRESS_RANGE
    devices = []
    for addr in available_addrs:
        ok,value = i2c.try_read(addr)
        devices.append({
            "address":f"0x{addr:02x}",
            "reachable":ok,
            "value":value if value is not None else "-"
        })

    return render_template("dashboard.html", devices=devices,address_range=available_addrs)

@bp.route("/trigger/<int:addr>/<int:value>")
def trigger(addr,value):
    ok = i2c.try_write(addr,value)
    if not ok:
        flash(f"Could not write to 0x{addr:02x}: {value}", "error")
    else:
        flash(f"Wrote {value} to 0x{addr:02x}", "success")
    return redirect(url_for("main.dashboard"))
    
@bp.route("/triggerAll/<addresses>/<int:value>")
def trigger_all(addresses,value):
	ok_addrs = []
	bad_addrs = []
	to_int_list = lambda s: list(map(int, s.split(',')))
	addrs = to_int_list(addresses)
	for ad in addrs:
		ok = i2c.try_write(ad,value)
		if ok:
			ok_addrs.append(ad)
		else:
			bad_addrs.append(ad)

	if ok_addrs:
		hex_list = [f"0x{n:02x}" for n in ok_addrs]
		flash(f"Wrote {value} to {hex_list}", "success")
	if bad_addrs:
		hex_list = [f"0x{n:02x}" for n in bad_addrs]
		flash(f"Could not write to {hex_list}: {value}", "error")
		
	return redirect(url_for("main.dashboard"))

@bp.route("/layout")
def layout():
    # full address list, e.g. [0x08 .. 0x18)
    accessible_addrs = [f"0x{x:02x}" for x in I2C_ADDRESS_RANGE]

    current_devices = load_layout_devices()
    used_addrs = {d["i2c_address"] for d in current_devices if d["i2c_address"]}
    free_addrs = [a for a in accessible_addrs if a not in used_addrs]

    return render_template(
        "layout.html",
        free_addrs=free_addrs,
        current_devices=current_devices,
        bus_id=I2C_BUS_ID
    )

@bp.route("/layout/save", methods=["POST"])
def save_layout():
    data = request.json  or {} # expects a JSON body: { "buttons": [ {...}, ... ] }
    devices = data.get("devices", [])

    # create root <uiLayout>
    #root = ET.SubElement(data, "uiLayout")
    root = ET.Element("uiLayout")
    devices_el = ET.SubElement(root, "devices")

    for dev in devices:
        d = ET.SubElement(devices_el, "device")
        # attributes on the device tag
        d.set("id", dev.get("id","-"))
        d.set("type",dev.get("type","-"))

        #name
        ET.SubElement(d, "name").text = dev.get("name","-")

        # i2c address
        ET.SubElement(d,"i2c_address").text = dev.get("i2c_address", "-")

        # position block (percent-based)
        pos = ET.SubElement(d, "position")
        ET.SubElement(pos, "x_pct").text = str(dev.get("x_pct", 0))
        ET.SubElement(pos, "y_pct").text = str(dev.get("y_pct", 0))

        # style block  – can grow later
        style = ET.SubElement(d, "style")
        ET.SubElement(style, "color").text = dev.get("color", "#0d6efd")
        ET.SubElement(style, "shape").text = dev.get("shape", "rect")
        ET.SubElement(style, "icon").text = dev.get("icon", "none")

    # make sure folder exists
    LAYOUT_DIR.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(root)
    tree.write(LAYOUT_FILE,encoding="utf-8",xml_declaration=True)

    return jsonify({"status":"ok"})



# ---- System A legacy routes (converted to System B stubs) ----

@bp.route('/reset_buttons_pressed')

def reset_buttons_flask_route():

    return "Reset buttons (stub)"



@bp.route('/shutdown_system')

def shutdown_system_flask_route():

    return "Shutdown system (stub)"



@bp.route('/reboot_rasberry_pi')

def reboot_rasberry_pi_flask_route():

    return "Reboot Raspberry Pi (stub)"



@bp.route('/restart_program')

def restart_program_flask_route():

    return "Restart program (stub)"



@bp.route('/change_hose_time', methods=['POST'])

def change_hose_time_flask_route():

    return "Changed hose time (stub)"



@bp.route('/set_new_interval_time/<int:new_interval_time>', methods=['POST'])

def set_new_interval_time(new_interval_time):

    return f"Set new interval time to {new_interval_time} (stub)"



@bp.route('/start_random_game')

def start_random_game_flask_route():

    return "Start random game (stub)"



@bp.route('/stop_random_game')

def stop_random_game_flask_route():

    return "Stop random game (stub)"



@bp.route('/change_coop_button_time', methods=['POST'])

def change_coop_button_time():

    return "Changed coop button time (stub)"



@bp.route('/start_coop_game')

def start_coop_game():

    return "Start coop game (stub)"



@bp.route('/stop_coop_game')

def stop_coop_game():

    return "Stop coop game (stub)"



@bp.route('/scan_button_pressed')

def scan_button_pressed_flask():

    return "Scan buttons (stub)"



@bp.route('/button_click_server/<int:button_id>', methods=['POST'])

def button_click_server(button_id):

    return f"Button {button_id} clicked (stub)"



@bp.route('/toggle_override', methods=['POST'])

def toggle_override():

    return "Toggle override (stub)"



@bp.route('/stream')

def stream_logging_data():

    return "Streaming (stub; SSE disabled)"



@bp.route('/update_button_colour/<button_id>', methods=['POST', 'GET'])

def update_colour(button_id):

    return f"Update button colour for {button_id} (stub)"



@bp.route('/start_simulate_press/<button_id>', methods=['POST'])

def start_stimulating_button(button_id):

    return f"Start simulating press for {button_id} (stub)"



@bp.route('/stop_simulate_press/<button_id>', methods=['POST'])

def stop_simulating_button(button_id):

    return f"Stop simulating press for {button_id} (stub)"

