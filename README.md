# Dolphin Enrichment Project (Raspberry Pi 4 / 5 / etc.)

## Setup

### Windows 11 / PC Setup

1. Install **Python 3.13** (or newer) and make sure it’s on your PATH.

2. Open PowerShell and navigate to your project directory:

   ```powershell
   cd "C:\Users\User\Documents\6002ENG\Button_arrainge Project\dolphin_enrichment"
   ```

3. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Run the Flask app:

   ```powershell
   python run.py
   ```

---

### Raspberry Pi 4 / 5 Setup (Recommended Deployment)

1. Update your system and install dependencies:

   ```bash
   sudo apt update
   sudo apt install python3 python3-venv python3-pip i2c-tools git -y
   ```

2. Enable I²C (only once):

   ```bash
   sudo raspi-config
   ```

   * Navigate → **Interface Options → I2C → Enable**
   * Reboot when prompted.

3. Verify I²C bus:

   ```bash
   sudo i2cdetect -y 1      # Default hardware I²C bus
   ```

4. Clone or copy the project to `/home/dep/dolphin_enrichment`, then:

   ```bash
   cd /home/dep/dolphin_enrichment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. Configure your I²C bus in `config.py`:

   ```python
   # config.py
   I2C_BUS_ID = 1  # Use 1 for new Pi boards, 5 if your pins are remapped
   ```

6. Also make sure the Pi has the system-level I²C packages installed:

   ```bash
   sudo apt install python3-smbus python3-gpiozero -y
   ```

7. Run it on the Pi:

   ```bash
   cd /home/dep/dolphin_enrichment
   source venv/bin/activate
   python run.py --host=0.0.0.0
   ```

8. **Accessing the Flask App on Your Network:**

   * From the Pi terminal, find your hostname:

     ```bash
     hostname
     ```

     Example output:

     ```bash
     raspberrypiDEP
     ```

   * Once Flask is running, open a browser on your laptop, desktop, or phone (connected to the same Wi-Fi) and go to:

     ```
     http://raspberrypiDEP.local:5000
     ```

   * Alternatively, you can also use the Pi’s IP address:

     ```
     http://<PI-IP>:5000/dashboard
     ```

   > 💡 Tip: If `.local` addresses don’t work, install Avahi on the Pi:
   >
   > ```bash
   > sudo apt install avahi-daemon -y
   > sudo systemctl enable avahi-daemon
   > sudo systemctl start avahi-daemon
   > ```

---

## Project Structure

```
/home/dep/dolphin_enrichment/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── hardware/
│   │   ├── i2c_manager.py
│   │   ├── led_control.py
│   │   ├── solenoid_driver.py
│   │   └── button_monitor.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── logs.html
│   └── static/
│       ├── css/
│       └── js/
│
├── config.py
├── run.py
└── requirements.txt
```

---

## Notes

* Run `sudo i2cdetect -y <bus>` to check device connectivity.
* To start automatically on boot, add this to `/etc/rc.local` before `exit 0`:

  ```bash
  su - dep -c "cd /home/dep/dolphin_enrichment && /home/dep/dolphin_enrichment/venv/bin/python run.py &"
  ```
* Use `Ctrl+C` to stop the Flask server.
* Change `I2C_BUS_ID` in `config.py` if switching hardware buses.
* Works on **Raspberry Pi 4**, **Raspberry Pi 5**, and future models using the same GPIO/I²C configuration.

---

© 2025 Dolphin Enrichment Project — for academic and educational use.
