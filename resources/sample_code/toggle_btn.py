from machine import Pin
import time

led = Pin(0, Pin.OUT)
button = Pin(1, Pin.IN, Pin.PULL_DOWN)

while True:
    if button.value():
        led.toggle()
        time.sleep(0.5)
