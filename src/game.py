import json
import time
from collections import namedtuple

from LCD_1inch3 import LCD_1inch3
from helper import file_exists
from LCD_joystick import JoyStick
from LCD_color import RGB565


class PetJob:
    Sit = "Sit"
    Run = "Run"
    Eat = "Eat"
    Shower = "Shower"
    Play = "Play"

PetUIStatus = namedtuple("PetUIStatus", "job remaining_seconds")

class PetState:
    # TODO:
    ...

class Pet:
    sit_img_path = ""
    run_img_paths = []
    img_size = (64, 64)
    satiety_drop_per_second = 2 / 60
    cleanliness_drop_per_second = 1 / 60

    def __init__(self, LCD: LCD_1inch3) -> None:
        self.LCD = LCD
        self.i = 0
        self.state = {
            "status": PetUIStatus(PetJob.Sit, -1), # for ui rendering
            "satiety": 50,
            "cleanliness": 50,
            "time": time.time(),
            "birth_time": time.time(),
            "class": self.__class__.__name__,
        }
        if not self.sit_img_path:
            raise ValueError("set pet sit image")

    @property
    def status(self) -> PetUIStatus:
        return self.state['status']
    
    def set_status(self, value):
        self.state['status'] = value

    def dump_state(self):
        print("dump_state", self.state)
        return self.state

    def load_state(self, state):
        self.state = state

    def update_state(self):
        """TODO: update state along with time passing by"""
        new_time = time.time()
        time_passed = new_time - self.state["time"]
        new_satiety = self.state["satiety"] - self.satiety_drop_per_second * time_passed
        new_cleanliness = self.state["cleanliness"] - self.cleanliness_drop_per_second * time_passed
        self.load_state(
            {
                "satiety": new_satiety,
                "cleanliness": new_cleanliness,
                "time": new_time,
            }
        )

    def render_pet(self, img_data):
        offset = (self.LCD.width // 2 - self.img_size[1] // 2, self.LCD.height // 2 - self.img_size[0] // 2)
        self.LCD.fill_rect(*offset, *self.img_size, RGB565.black)
        for y in range(0, self.img_size[0]):
            line = img_data[2 * y * self.img_size[1] : 2 * (y + 1) * self.img_size[1]]
            for x in range(0, self.img_size[1]):
                pixel = int.from_bytes(line[2 * x : 2 * x + 2], "big")
                self.LCD.pixel(x + offset[0], y + offset[1], pixel)
        self.LCD.show()

    def _load_img(self, path):
        data = None
        with open(path, "rb") as fp:
            data = fp.read()
        return data

    def render_sit(self):
        self.render_pet(self._load_img(self.sit_img_path))

    def render_run(self):
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def render_eat(self):
        # TODO: img
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def render_shower(self):
        # TODO: img
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def render_play(self):
        # TODO: img
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1


class Pikachu(Pet):
    sit_img_path = "rgb565/pikachu-sit.raw"
    run_img_paths = [
        "rgb565/pikachu-run-right-1.raw",
        "rgb565/pikachu-run-right-2.raw",
        "rgb565/pikachu-run-right-3.raw",
    ]


ButtonUI = namedtuple("ButtonUI", "assignment coordinates size text")

def reward(pet: Pet, job: PetJob):
    if job == PetJob.Eat:
        pet.state['']


class Game:
    state_path = "state.json"
    default_pet = Pikachu
    button_ui_map = {
        JoyStick.keyA: ButtonUI(PetUIStatus(PetJob.Eat, 5), (208, 15), (30, 30), "feed"),
        JoyStick.keyB: ButtonUI(PetUIStatus(PetJob.Shower, 5), (208, 75), (30, 30), "bath"),
        JoyStick.keyX: ButtonUI(PetUIStatus(PetJob.Play, 10), (208, 135), (30, 30), "play"),
        JoyStick.keyY: ButtonUI(PetUIStatus(PetJob.Sit, -1), (208, 195), (30, 30), "??"),
    }

    def __init__(self, LCD: LCD_1inch3, allow_dump=False) -> None:
        self.LCD = LCD
        self.allow_dump = allow_dump
        self.triggered_button = None
        self.pet: Pet
        self.load_state()
        if not getattr(self, 'pet', None):
            print("spawning new pet type", Game.default_pet.__name__)
            self.pet = Game.default_pet(self.LCD)
        self.dump_state()
        self.render()

    def load_state(self):
        has_archive = file_exists(Game.state_path)
        if has_archive:
            print("loading pet...")
            with open(Game.state_path, "r") as fp:
                state_loaded = json.load(fp)
                print("state_loaded", state_loaded)
                clazz = eval(state_loaded.get("class", Game.default_pet))
                self.pet = clazz(self.LCD)
                self.pet.load_state(state_loaded)

    def dump_state(self):
        if not self.allow_dump:
            print("dump skipped")
            return
        if not self.pet:
            return
        print("dumping state...")
        with open(Game.state_path, "w") as fp:
            json.dump(self.pet.dump_state(), fp)

    def render(self):
        prev_time = None

        while 1:

            curr_time = time.ticks_ms()
            time_elapsed = None
            if prev_time:
                time_elapsed = time.ticks_diff(curr_time, prev_time)

            self.render_ui()
            self.render_pet()

            if self.pet.status.remaining_seconds > 0 and time_elapsed:
                self.pet.state['status'] = PetUIStatus(self.pet.status.job, self.pet.status.remaining_seconds - time_elapsed / 1000)
                if self.pet.status.remaining_seconds < 0:
                    self.pet.state['status'] = PetUIStatus(PetJob.Sit, -1)

            if self.triggered_button:
                if self.pet.status.job == PetJob.Sit:
                    # change state
                    triggered = Game.button_ui_map[self.triggered_button]
                    self.pet.state['status'] = triggered.assignment
                self.triggered_button = None

            prev_time = curr_time
            time.sleep_ms(10)

    def render_ui(self):
        print(time.time(), 'rendering ui')
        for key_to_check in JoyStick.buttons:
            button_ui = Game.button_ui_map[key_to_check]
            if self.pet.status.job != PetJob.Sit:
                # waiting for ui animation complete
                self.LCD.fill_rect(*button_ui.coordinates, *button_ui.size, RGB565.black)
            elif key_to_check.pressed() and self.triggered_button is None:
                self.LCD.fill_rect(*button_ui.coordinates, *button_ui.size, RGB565.white)
                # save action for state change
                self.triggered_button = key_to_check
            else:
                self.LCD.fill_rect(*button_ui.coordinates, *button_ui.size, RGB565.black)
                self.LCD.rect(*button_ui.coordinates, *button_ui.size, RGB565.white)
                self.LCD.text(button_ui.text, *button_ui.coordinates, RGB565.white)

    def render_pet(self):
        print(time.time(), 'rendering pet', self.pet.status)
        if self.pet.status.job == PetJob.Sit:
            self.pet.render_sit()
        elif self.pet.status.job == PetJob.Run:
            self.pet.render_run()
        elif self.pet.status.job == PetJob.Eat:
            self.pet.render_eat()
        elif self.pet.status.job == PetJob.Shower:
            self.pet.render_shower()
        elif self.pet.status.job == PetJob.Play:
            self.pet.render_play()
        else:
            raise NotImplementedError()
