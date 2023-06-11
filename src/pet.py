import time
from random import choice
from LCD_1inch3 import LCD_1inch3
from LCD_color import RGB565
from pet_ui import PetUIStatus


class PetJob:
    Sit = "Sit"
    Run = "Run"
    Eat = "Eat"
    Shower = "Shower"
    Play = "Play"
    Sleep = "Sleep"


class Pet:
    sit_img_path = ""
    run_img_paths = []
    eat_img_paths = []
    img_size = (72, 72)

    satiety_drop_per_second = 2 / 60
    cleanliness_drop_per_second = 1 / 60
    fatigue_drop_per_second = 1 / 60

    def __init__(self, LCD: LCD_1inch3) -> None:
        self.LCD = LCD
        self.i = 0
        self.state = {
            "status": [],  # ui status list for rendering
            "satiety": 50,
            "cleanliness": 50,
            "fatigue": 50,
            "happiness": 50,
            "time": time.time(),
            "birth_time": time.time(),
            "class": self.__class__.__name__,
        }
        if not self.sit_img_path:
            raise ValueError("set pet sit image")

    @property
    def status(self) -> list[PetUIStatus]:
        return self.state["status"]

    def set_status(self, value):
        self.state["status"] = value

    @property
    def is_busy(self):
        return bool(self.status) and self.status[0].is_user_action

    @property
    def job_to_render(self):
        if not self.status:
            return None
        return self.status[0]

    def dump_state(self):
        print("dump_state", self.state)
        return self.state

    def update_state(self, ui_time_elapsed_in_ms):
        """
        update ui status
        update pet numbers
        """
        if not self.job_to_render:
            random_action = choice(
                (
                    PetUIStatus(PetJob.Sit, 5, 5, False),
                    PetUIStatus(PetJob.Sleep, 5, 5, False),
                    PetUIStatus(PetJob.Play, 5, 5, False),
                )
            )
            print(time.time(), "pet start doing", random_action)
            self.status.append(random_action)
        else:
            # update ui status
            if self.job_to_render.remaining_seconds > 0:
                self.status[0] = PetUIStatus(
                    self.job_to_render.job,
                    self.job_to_render.total_secoends,
                    self.job_to_render.remaining_seconds - ui_time_elapsed_in_ms / 1000,
                    self.job_to_render.is_user_action,
                )
            if self.job_to_render.remaining_seconds < 0:
                self.reward(self.job_to_render.job, self.job_to_render.total_secoends)
                self.set_status(self.status[1:])

        # update time & satiety & cleanliness & fatigue every 10 seconds
        new_time = time.time()
        time_passed = new_time - self.state["time"]
        if time_passed > 10:
            new_satiety = self.state["satiety"] - self.satiety_drop_per_second * time_passed
            new_cleanliness = self.state["cleanliness"] - self.cleanliness_drop_per_second * time_passed
            new_fatigue = self.state["fatigue"] + self.fatigue_drop_per_second * time_passed
            self.state.update(
                {
                    "satiety": new_satiety,
                    "cleanliness": new_cleanliness,
                    "fatigue": new_fatigue,
                    "time": new_time,
                }
            )
            print(new_time, "updating pet state\n", self.state)

    def render_pet(self, img_data):
        start = time.ticks_ms()
        offset_x, offset_y = (self.LCD.width // 2 - self.img_size[1] // 2, self.LCD.height // 2 - self.img_size[0] // 2)

        # self.LCD.fill_rect(*offset, *self.img_size, RGB565.black)
        for y, line in enumerate(img_data):
            line_y = y + offset_y
            line_x = offset_x
            for x in range(0, self.img_size[1]):
                xx = x << 1
                # TODO: 使用 x,y,int 来表达有效像素，尝试降低渲染时间
                self.LCD.pixel(line_x, line_y, int.from_bytes(line[xx : xx + 2], "big"))
                line_x += 1

        # self.LCD.fill_rect(*offset, *self.img_size, RGB565.black)
        # for y in range(0, self.img_size[0]):
        #     line = img_data[2 * y * self.img_size[1] : 2 * (y + 1) * self.img_size[1]]
        #     for x in range(0, self.img_size[1]):
        #         pixel = int.from_bytes(line[2 * x : 2 * x + 2], "big")
        #         self.LCD.pixel(x + offset[0], y + offset[1], pixel)
        end = time.ticks_ms()
        print("render pet took", time.ticks_diff(end, start), "ms")
        self.LCD.show()

    def _load_img(self, path):
        read_line_count = 32
        line_length = self.img_size[1]
        with open(path, "rb") as fp:
            while 1:
                data = fp.read(2 * read_line_count * line_length)
                if data:
                    for i in range(read_line_count):
                        yield data[2 * i * line_length : 2 * (i + 1) * line_length]
                else:
                    break

    def render_sit(self):
        self.render_pet(self._load_img(self.sit_img_path))

    def render_run(self):
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def render_eat(self):
        self.render_pet(self._load_img(self.eat_img_paths[self.i % len(self.eat_img_paths)]))
        self.i += 1

    def render_shower(self):
        # TODO: img
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def render_play(self):
        # TODO: img
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def render_sleep(self):
        # TODO: img
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def render_hungry(self):
        # TODO: img
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def render_dirty(self):
        # TODO: img
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def render_sleepy(self):
        # TODO: img
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def render_lonely(self):
        # TODO: img
        self.render_pet(self._load_img(self.run_img_paths[self.i % len(self.run_img_paths)]))
        self.i += 1

    def reward(self, job: PetJob, duration_in_s):
        # TODO: use duration_in_s as coefficient
        if job == PetJob.Eat:
            self.state["satiety"] += 10
        elif job == PetJob.Play:
            self.state["happiness"] += 10
            self.state["satiety"] -= 3
            self.state["fatigue"] += 5
        elif job == PetJob.Shower:
            self.state["cleanliness"] += 10
        elif job == PetJob.Sleep:
            self.state["fatigue"] = max(0, self.state["fatigue"] - 20)
        else:
            print("nothing awarded")
