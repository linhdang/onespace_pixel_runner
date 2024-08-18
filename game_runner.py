import pygame

from pixel_runner import PixelRunner

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Runner')

    game = PixelRunner()
    game.run()
