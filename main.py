import time
import board, nativeio

LED = nativeio.DigitalInOut(board.D13)
LED.switch_to_output()

def blink_LED():
    print("On")
    LED.value = True
    time.sleep(0.5)
    print("Off")
    LED.value = False
    time.sleep(0.5)
    
blink_LED()

import test_lora
