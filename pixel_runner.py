import pygame


class PixelRunner:

    def __init__(self, mode=pygame.display.set_mode((800, 400))) -> None:
        self.score = None
        self.start_time = None
        self.game_active = None
        self.ground_surface = None
        self.sky_surface = None
        self.font = None
        self.clock = None
        self.screen = None
        self.initialize_game_screen(mode)

    def initialize_game_screen(self, mode):
        self.screen = mode
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.sky_surface = pygame.image.load('graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('graphics/ground.png').convert()
        bg_music = pygame.mixer.Sound('audio/music.wav')
        bg_music.play(loops=-1)
        self.game_active = False
        self.start_time = 0
        self.score = 0


    def draw_background(self):
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.ground_surface, (0, 300))

    def run(self):
        while True:
            self.draw_background()

            pygame.display.update()
            self.clock.tick(60)
