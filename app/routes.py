from flask import Blueprint, render_template, redirect, url_for,flash
from .hardware.i2c_manager import i2c

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/dashboard")
def dashboard():
    # try to read a byte from the known addresses you saw: 0x08, 0x09, 0x0A
    known_addrs = [x for x in range(0x08, 0x08 + 17)]
    devices = []
    for addr in known_addrs:
        ok,value = i2c.try_read(addr)
        devices.append({
            "address":f"0x{addr:02x}",
            "reachable":ok,
            "value":value if value is not None else "-"
        })

    return render_template("dashboard.html", devices=devices,address_range=known_addrs)

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
