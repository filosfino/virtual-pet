def render_img(LCD, img: list[list[int]]):
    for i, line in enumerate(img):
        for j, pixel in enumerate(line):
            LCD.pixel(i, j, pixel)
