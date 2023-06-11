import json
import time
from LCD_1inch3 import LCD_1inch3
from helper import file_exists
from LCD_joystick import JoyStick
from LCD_color import RGB565
from pet import Pet, PetJob
from pet_pikachu import Pikachu
from ui import button_ui_map


RenderIntervalInMs = 20
TextUIOffsetY = 10


class Game:
    state_path = "state.json"
    default_pet = Pikachu

    def __init__(self, LCD: LCD_1inch3, allow_dump=False) -> None:
        self.LCD = LCD
        self.allow_persist = allow_dump
        self.pet: Pet
        self.load_state()
        if not getattr(self, "pet", None):
            print("spawning new pet type", Game.default_pet.__name__)
            self.pet = Game.default_pet(self.LCD)
        self.persist_state()

    def start(self):
        self.loop()

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

    def persist_state(self):
        if not self.allow_persist:
            print("persist state skipped")
            return
        if not self.pet:
            return
        print("persiting state...")
        with open(Game.state_path, "w") as fp:
            json.dump(self.pet.dump_state(), fp)

    def get_triggered_btn(self, btn_status):
        for key_to_check in JoyStick.buttons:
            if self.pet.job_to_render and self.pet.job_to_render.is_user_action:
                # hide ui & wait for action complete
                continue
            elif btn_status[key_to_check]:
                # save action for state change
                print("triggered_btn", key_to_check)
                return key_to_check

    def loop(self):
        prev_time = None

        while 1:
            curr_time = time.ticks_ms()
            time_elapsed_in_ms = None
            if prev_time:
                time_elapsed_in_ms = time.ticks_diff(curr_time, prev_time)

            self.LCD.fill(RGB565.black)

            key_pressed = self.detect_key_pressed()
            triggered_btn = self.get_triggered_btn(key_pressed)

            self.render_ui(key_pressed, triggered_btn)
            self.render_pet()

            if triggered_btn and not self.pet.is_busy:
                print(time.time(), "pet assigned new jobs", button_ui_map[triggered_btn].assignment)
                self.pet.set_status(list(button_ui_map[triggered_btn].assignment))
            self.pet.update_state(time_elapsed_in_ms)

            if (time.time() - self.pet.state["birth_time"]) % 30 == 0:
                self.persist_state()

            prev_time = curr_time
            time.sleep_ms(RenderIntervalInMs)

    def detect_key_pressed(self):
        """get key pressed status"""
        ret = {}
        for key_to_check in JoyStick.buttons:
            ret[key_to_check] = key_to_check.pressed()
        for key_to_check in JoyStick.ctrl_btns:
            ret[key_to_check] = key_to_check.pressed()
        return ret

    def render_ui(self, key_pressed, triggered_btn):
        print(time.time(), "rendering ui")
        for key_to_check in JoyStick.buttons:
            button_ui = button_ui_map[key_to_check]
            if self.pet.is_busy:
                # hide ui & wait for action complete
                ...
            elif key_pressed[key_to_check] and triggered_btn == key_to_check:
                self.LCD.fill_rect(*button_ui.coordinates, *button_ui.size, RGB565.white)
                self.LCD.text(
                    button_ui.text, button_ui.coordinates[0], button_ui.coordinates[1] + TextUIOffsetY, RGB565.black
                )
            else:
                # self.LCD.fill_rect(*button_ui.coordinates, *button_ui.size, RGB565.black)
                self.LCD.text(
                    button_ui.text, button_ui.coordinates[0], button_ui.coordinates[1] + TextUIOffsetY, RGB565.white
                )

    def render_pet(self):
        print(time.time(), "rendering pet", self.pet.status)
        job_to_render = self.pet.job_to_render
        if not job_to_render:
            if self.pet.state["satiety"] < 0:
                self.pet.render_hungry()
            elif self.pet.state["cleanliness"] < 0:
                self.pet.render_dirty()
            elif self.pet.state["fatigue"] > 100:
                self.pet.render_sleepy()
            elif self.pet.state["happiness"] < 0:
                self.pet.render_lonely()
        else:
            if job_to_render.job == PetJob.Sit:
                self.pet.render_sit()
            elif job_to_render.job == PetJob.Run:
                self.pet.render_run()
            elif job_to_render.job == PetJob.Eat:
                self.pet.render_eat()
            elif job_to_render.job == PetJob.Shower:
                self.pet.render_shower()
            elif job_to_render.job == PetJob.Play:
                self.pet.render_play()
            elif job_to_render.job == PetJob.Sleep:
                self.pet.render_sleep()
            else:
                raise NotImplementedError()
