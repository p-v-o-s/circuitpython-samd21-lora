import time
import board, nativeio
    
import RF95_consts as RF95
from lora_radio import LoRaRadio
LR = LoRaRadio()
while True:
    try:
        LR.reset()
        time.sleep(0.1)
        print("testing REG_01_OP_MODE setting")
        LR._spi_write_reg(RF95.REG_01_OP_MODE, RF95.MODE_SLEEP | RF95.LONG_RANGE_MODE)
        time.sleep(0.1)
        val = LR._spi_read_reg(RF95.REG_01_OP_MODE)
        print("val =",val)
        assert(val == (RF95.MODE_SLEEP | RF95.LONG_RANGE_MODE))
    except AssertionError:
        print("failed!")

print("tests passed")
