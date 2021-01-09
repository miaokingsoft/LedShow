from ledshow import LedShow
from webled import WebLed
from machine import Pin
import time

#KEY1=Pin(13,Pin.IN,Pin.PULL_UP)
#KEY2=Pin(14,Pin.IN,Pin.PULL_UP)
#KEY3=Pin(27,Pin.IN,Pin.PULL_UP)

led = LedShow()
wl = WebLed()

while True:
    led.micphone()
    wl.Webhttp()
    
            
    

