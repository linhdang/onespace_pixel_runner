import pygame
from sys import exit
from random import choice

from obstacle import Obstacle
from pixel_runner import PixelRunner
from player import Player

if __name__ == "__main__":
    game = PixelRunner()
    game.run()
