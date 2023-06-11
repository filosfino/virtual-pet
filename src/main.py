from LCD_1inch3 import LCD_1inch3
from LCD_color import RGB565
from game import Game


if __name__ == "__main__":
    LCD = LCD_1inch3()
    LCD.fill(RGB565.black)
    LCD.show()
    game = Game(LCD)
    game.start()
