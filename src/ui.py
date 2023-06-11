from collections import namedtuple

from LCD_joystick import JoyStick
from pet import PetJob
from pet_ui import PetUIStatus


ButtonUI = namedtuple("ButtonUI", "assignment coordinates size text")

button_ui_map = {
    JoyStick.keyA: ButtonUI((PetUIStatus(PetJob.Eat, 5, 5, True),), (208, 15), (30, 30), "feed"),
    JoyStick.keyB: ButtonUI((PetUIStatus(PetJob.Shower, 5, 5, True),), (208, 75), (30, 30), "bath"),
    JoyStick.keyX: ButtonUI((PetUIStatus(PetJob.Play, 10, 10, True),), (208, 135), (30, 30), "play"),
    JoyStick.keyY: ButtonUI((PetUIStatus(PetJob.Sit, 5, 5, True),), (208, 195), (30, 30), "Sit"),
}
