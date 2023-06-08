from machine import ADC, Pin, PWM
import time

adc = ADC(Pin(26)) # need to use ADC pin

# while True:
#     print(adc.read_u16())
#     time.sleep(1)

pwm = PWM(Pin(0))

pwm.freq(1000)

while True:
	duty = adc.read_u16()
	pwm.duty_u16(duty)
