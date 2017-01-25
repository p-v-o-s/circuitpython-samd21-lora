import time
import nativeio
from board import *
import microcontroller
from adafruit_bus_device.spi_device import SPIDevice
import RF95_consts as RF95


class LoRaRadio(object):
    # This is the bit in the SPI address that marks it as a write
    SPI_WRITE_MASK  = 0x80
    def __init__(self):
        # see http://learn.adafruit.com/assets/30921 for Feather M0 pinout
        self.pin_CS  = nativeio.DigitalInOut(microcontroller.pin.PB09) # pin #8
        self.pin_RST = nativeio.DigitalInOut(microcontroller.pin.PA03) # pin #4
        self.pin_INT = nativeio.DigitalInOut(microcontroller.pin.PA02) # pin #3
        self.pin_CS.switch_to_output()
        self.pin_CS.value = True
        self.pin_RST.switch_to_output()
        self.pin_RST.value = True
        self.pin_INT.switch_to_input()
        self._buff = bytearray(1)
        
    def _spi_read_reg(self, reg):
        with nativeio.SPI(SCK, MOSI, MISO) as spi_bus:
            device = SPIDevice(spi_bus, self.pin_CS)
            with device as spi:
                spi.write(bytes([reg & ~self.SPI_WRITE_MASK])) # Send the address with the write mask off
                spi.readinto(self._buff)
        return self._buff
        
    def _spi_write_reg(self, reg, val):
        with nativeio.SPI(SCK, MOSI, MISO) as spi_bus:
            device = SPIDevice(spi_bus, self.pin_CS)
            with device as spi:
                spi.write(bytes([reg | self.SPI_WRITE_MASK, val])) # Send the address with the write mask on
                #spi.write(bytes([val]))
                
    def reset(self):
        self.pin_RST.value = False
        time.sleep(10e-6)
        self.pin_RST.value = True
        time.sleep(10e-6)
        
    def begin(self):
        # No way to check the device type :-(
        # Set sleep mode, so we can also set LORA mode:
        self._spi_write_reg(RF95.REG_01_OP_MODE, RF95.MODE_SLEEP | RF95.LONG_RANGE_MODE)
        time.sleep(10e-6) # Wait for sleep mode to take over from say, CAD


#import RF95_consts as RF95
#from lora_radio import LoRaRadio
#LR = LoRaRadio()
#LR._spi_write_reg(RF95.REG_01_OP_MODE, RF95.MODE_SLEEP | RF95.LONG_RANGE_MODE)

