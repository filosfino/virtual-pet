from machine import Pin

class LCDJoystickPin(Pin):

    def pressed(self):
        return self.value() == 0

class JoyStick:

    keyA = LCDJoystickPin(15, Pin.IN, Pin.PULL_UP)
    keyB = LCDJoystickPin(17, Pin.IN, Pin.PULL_UP)
    keyX = LCDJoystickPin(19, Pin.IN, Pin.PULL_UP)
    keyY = LCDJoystickPin(21, Pin.IN, Pin.PULL_UP)
    buttons = [keyA, keyB, keyX, keyY]

    up = LCDJoystickPin(2, Pin.IN, Pin.PULL_UP)
    down = LCDJoystickPin(18, Pin.IN, Pin.PULL_UP)
    left = LCDJoystickPin(16, Pin.IN, Pin.PULL_UP)
    right =LCDJoystickPin(20, Pin.IN, Pin.PULL_UP)
    ctrl = LCDJoystickPin(3, Pin.IN, Pin.PULL_UP)
    moves = [up, down, left, right, ctrl]

# if keyA.value() == 0:
#     LCD.fill_rect(208,15,30,30,RGB565.red)
# else :
#     LCD.fill_rect(208,15,30,30,RGB565.white)
#     LCD.rect(208,15,30,30,RGB565.red)

# if(keyB.value() == 0):
#     LCD.fill_rect(208,75,30,30,RGB565.red)
# else :
#     LCD.fill_rect(208,75,30,30,RGB565.white)
#     LCD.rect(208,75,30,30,RGB565.red)

# if(keyX.value() == 0):
#     LCD.fill_rect(208,135,30,30,RGB565.red)
# else :
#     LCD.fill_rect(208,135,30,30,RGB565.white)
#     LCD.rect(208,135,30,30,RGB565.red)

# if(keyY.value() == 0):
#     LCD.fill_rect(208,195,30,30,RGB565.red)
# else :
#     LCD.fill_rect(208,195,30,30,RGB565.white)
#     LCD.rect(208,195,30,30,RGB565.red)

# if(up.value() == 0):
#     LCD.fill_rect(60,60,30,30,RGB565.red)
# else :
#     LCD.fill_rect(60,60,30,30,RGB565.white)
#     LCD.rect(60,60,30,30,RGB565.red)

# if(dowm.value() == 0):
#     LCD.fill_rect(60,150,30,30,RGB565.red)
# else :
#     LCD.fill_rect(60,150,30,30,RGB565.white)
#     LCD.rect(60,150,30,30,RGB565.red)

# if(left.value() == 0):
#     LCD.fill_rect(15,105,30,30,RGB565.red)
# else :
#     LCD.fill_rect(15,105,30,30,RGB565.white)
#     LCD.rect(15,105,30,30,RGB565.red)

# if(right.value() == 0):
#     LCD.fill_rect(105,105,30,30,RGB565.red)
# else :
#     LCD.fill_rect(105,105,30,30,RGB565.white)
#     LCD.rect(105,105,30,30,RGB565.red)

# if(ctrl.value() == 0):
#     LCD.fill_rect(60,105,30,30,RGB565.red)
# else :
#     LCD.fill_rect(60,105,30,30,RGB565.white)
#     LCD.rect(60,105,30,30,RGB565.red)
