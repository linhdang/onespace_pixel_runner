from random import choice

import pygame

from obstacle import Obstacle
from player import Player


class PixelRunner:

    def __init__(self) -> None:

        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption('Runner')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.sky_surface = pygame.image.load('graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('graphics/ground.png').convert()
        self.game_active = False
        self.start_time = 0
        self.score = 0
        bg_music = pygame.mixer.Sound('audio/music.wav')
        bg_music.play(loops=-1)

        self.snail_surf = None
        self.current_snail_frame_index = None
        self.snail_frames = None

        # Groups
        self.player = pygame.sprite.GroupSingle()
        self.obstacle_group = pygame.sprite.Group()
        self.player.add(Player())

        self.initialize_snail_frames()

        # Fly
        fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
        fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
        self.fly_frames = [fly_frame1, fly_frame2]
        self.current_fly_frame_index = 0
        self.fly_surf = self.fly_frames[self.current_fly_frame_index]

        self.obstacle_rect_list = []

        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        player_walk = [player_walk_1, player_walk_2]
        player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        player_surf = player_walk[player_index]
        self.player_rect = player_surf.get_rect(midbottom=(80, 300))
        self.player_gravity = 0

        # Intro screen
        player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
        self.player_stand_rect = player_stand.get_rect(center=(400, 200))

        self.game_name = self.font.render('Pixel Runner', False, (111, 196, 169))
        self.game_name_rect = self.game_name.get_rect(center=(400, 80))

        self.game_message = self.font.render('Press space to run', False, (111, 196, 169))
        self.game_message_rect = self.game_message.get_rect(center=(400, 330))

        # Timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

        self.snail_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.snail_animation_timer, 500)

        self.fly_animation_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.fly_animation_timer, 200)

    def initialize_snail_frames(self):
        # Snail
        snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
        self.snail_frames = [snail_frame_1, snail_frame_2]
        self.current_snail_frame_index = 0
        self.snail_surf = self.snail_frames[self.current_snail_frame_index]

    def display_score(self):
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        score_surf = self.font.render(f'Score: {current_time}', False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(400, 50))
        self.screen.blit(score_surf, score_rect)
        return current_time

    def obstacle_movement(self, obstacle_list):
        if obstacle_list:
            for obstacle_rect in obstacle_list:
                obstacle_rect.x -= 5

                if obstacle_rect.bottom == 300:
                    self.screen.blit(self.snail_surf, obstacle_rect)
                else:
                    self.screen.blit(self.fly_surf, obstacle_rect)

            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

            return obstacle_list
        else:
            return []

    def collisions(self, player, obstacles):
        if obstacles:
            for obstacle_rect in obstacles:
                if player.colliderect(obstacle_rect):
                    return False
        return True

    def collision_sprite(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False):
            self.obstacle_group.empty()
            return False
        else:
            return True

    def animate_fly(self):
        if self.current_fly_frame_index == 0:
            self.current_fly_frame_index = 1
        else:
            self.current_fly_frame_index = 0
        self.fly_surf = self.fly_frames[self.current_fly_frame_index]

    def animate_snail(self):
        if self.current_snail_frame_index == 0:
            self.current_snail_frame_index = 1
        else:
            self.current_snail_frame_index = 0
        self.snail_surf = self.snail_frames[self.current_snail_frame_index]

    def handle_player_jump(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.player_rect.collidepoint(event.pos) and self.player_rect.bottom >= 300:
                self.player_gravity = -20
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.player_rect.bottom >= 300:
                self.player_gravity = -20

    def get_random_obstacle(self):
        self.obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

    def start_game(self):
        self.game_active = True
        self.start_time = int(pygame.time.get_ticks() / 1000)

    def draw_player_and_obstacles(self):
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.ground_surface, (0, 300))
        self.score = self.display_score()
        self.player.draw(self.screen)
        self.player.update()
        self.obstacle_group.draw(self.screen)
        self.obstacle_group.update()
        self.obstacle_rect_list = self.obstacle_movement(self.obstacle_rect_list)
        # collision
        self.game_active = self.collision_sprite()

    def display_summary_screen(self):
        self.screen.fill((94, 129, 162))
        self.screen.blit(self.player_stand, self.player_stand_rect)
        self.obstacle_rect_list.clear()
        self.player_rect.midbottom = (80, 300)
        self.player_gravity = 0
        score_message = self.font.render(f'Your score: {self.score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        self.screen.blit(self.game_name, self.game_name_rect)
        if self.score == 0:
            self.screen.blit(self.game_message, self.game_message_rect)
        else:
            self.screen.blit(score_message, score_message_rect)

    def run(self):

        while True:
            for event in pygame.event.get():
                # event handler
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active:
                    self.handle_player_jump(event)
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.start_game()

                if self.game_active:
                    if event.type == self.obstacle_timer:
                        self.get_random_obstacle()

            if self.game_active:
                self.draw_player_and_obstacles()

            else:
                self.display_summary_screen()

            pygame.display.update()
            self.clock.tick(60)
