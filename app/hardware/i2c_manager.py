import smbus2
from config import I2C_BUS_ID

class I2CManager:
    def __init__(self,bus_id=I2C_BUS_ID):
        self.bus_id = bus_id
        self.bus = smbus2.SMBus(bus_id)

    def try_write(self,address:int,value:int)->bool:
        try:
            self.bus.write_byte(address,value)
            return True
        except OSError:
            return False

    def try_read(self,address:int)->bool:
        try:
            val = self.bus.read_byte(address)
            return True,val
        except OSError:
            return False,None

# create a singleton for the app to import
i2c=I2CManager(bus_id=I2C_BUS_ID)