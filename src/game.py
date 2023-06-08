from LCD_1inch3 import LCD_1inch3
import json
from helper import file_exists
import time


class Pet:

    sit_img_path = ""
    run_img_paths = []
    img_size = (64, 64)
    satiety_drop_per_second = 2/60
    cleanliness_drop_per_second = 1/60

    def __init__(self, LCD: LCD_1inch3) -> None:
        self.LCD = LCD
        self.state = {
            'satiety': 50, # 饱腹
            'cleanliness': 50, # 洁净
            'time': time.time(), 
            'class': self.__class__.__name__,
        }
        if not self.sit_img_path:
            raise ValueError("set pet sit image")
    
    def dump_state(self):
        print("dump_state", self.state)
        return self.state

    def load_state(self, state):
        self.state = state

    def update_state(self):
        """TODO: update state along with time passing by
        """
        new_time = time.time()
        time_passed = new_time - self.state['time']
        new_satiety = self.state['satiety'] - self.satiety_drop_per_second *  time_passed
        new_cleanliness = self.state['cleanliness']- self.cleanliness_drop_per_second *  time_passed
        self.load_state({
            'satiety': new_satiety,
            'cleanliness': new_cleanliness,
            'time': new_time, 
        })

    def render_pet(self, img_data):
        offset = (self.LCD.width//2-self.img_size[1]//2, self.LCD.height//2-self.img_size[0]//2)
        for y in range(0, self.img_size[0]):
            line = img_data[2*y*self.img_size[1]:2*(y+1)*self.img_size[1]]
            for x in range(0, self.img_size[1]):
                pixel = int.from_bytes(line[2*x: 2*x+2], 'big')
                self.LCD.pixel(x+offset[0], y+offset[1], pixel)
        self.LCD.show()

    def _load_img(self, path):
        data = None
        with open(path, "rb") as fp:
            data = fp.read()
        return data

    def render_sit(self):
        self.render_pet(self._load_img(self.sit_img_path))

    def render_run(self, times=20, interval=0.15):
        run_one_way_imgs = [self._load_img(x) for x in self.run_img_paths]
        for i in range(times):
            self.render_pet(run_one_way_imgs[i%len(run_one_way_imgs)])
            time.sleep(interval)


class Pikachu(Pet):
    sit_img_path = "rgb565/pikachu-sit.raw"
    run_img_paths = [
        "rgb565/pikachu-run-right-1.raw",
        "rgb565/pikachu-run-right-2.raw",
        "rgb565/pikachu-run-right-3.raw",
    ]


class Game:
    state_path = "state.json"
    default_pet = Pikachu

    def __init__(self, LCD: LCD_1inch3) -> None:
        self.LCD = LCD
        self.pet = None
        self.load_state()
        assert self.pet
        time.sleep(3)
        self.pet.render_run()
        self.pet.render_sit()

    def load_state(self):
        has_archive = file_exists(Game.state_path)
        if has_archive:
            print("loading pet...")
            with open(Game.state_path, "r") as fp:
                state_loaded = json.load(fp)
                print('state_loaded', state_loaded)
                clazz = eval(state_loaded.get('class', Game.default_pet))
                self.pet = clazz(self.LCD)
                self.pet.load_state(state_loaded)
        else:
            self.spawn_pet(Game.default_pet)
        assert self.pet
        self.pet.render_sit()

    def dump_state(self):
        if not self.pet:
            return
        print("dumping state...")
        with open(Game.state_path, "w") as fp:
            json.dump(self.pet.dump_state(), fp)

    def spawn_pet(self, PetClass):
        print("spawning new pet type", PetClass.__name__)
        self.pet = PetClass(self.LCD)
        self.dump_state()
