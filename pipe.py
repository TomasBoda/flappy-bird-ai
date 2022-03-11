import pygame
import random
from rectangle import Rectangle
from config import pipe_width, pipe_velocity, pipe_hole_height, screen_width, screen_height, screen

class Pipe:
    def __init__(self, x):
        self.x = x
        self.y = self.generate_gap_position()

        self.top_body = pygame.transform.smoothscale(pygame.image.load("assets/pipe-body.png").convert_alpha(), (pipe_width, self.y - 24)) 
        self.top_head = pygame.transform.smoothscale(pygame.image.load("assets/pipe-head.png").convert_alpha(), (pipe_width, 24)) 
        self.bottom_body = pygame.transform.smoothscale(pygame.image.load("assets/pipe-body.png").convert_alpha(), (pipe_width, screen_height - self.y - pipe_hole_height - 24)) 
        self.bottom_head = pygame.transform.smoothscale(pygame.image.load("assets/pipe-head.png").convert_alpha(), (pipe_width, 24)) 

    def render(self):
        screen.blit(self.top_body, (self.x, 0))
        screen.blit(self.top_head, (self.x, self.y - 24))
        screen.blit(self.bottom_body, (self.x, self.y + pipe_hole_height + 24))
        screen.blit(self.bottom_head, (self.x, self.y + pipe_hole_height))

    def update(self):
        self.x -= pipe_velocity

    def generate_gap_position(self):
        return random.randint(50, screen_height - 50 - pipe_hole_height)

    def repaint_images(self):
        self.top_body = pygame.transform.smoothscale(pygame.image.load("assets/pipe-body.png").convert_alpha(), (pipe_width, self.y - 24)) 
        self.top_head = pygame.transform.smoothscale(pygame.image.load("assets/pipe-head.png").convert_alpha(), (pipe_width, 24)) 
        self.bottom_body = pygame.transform.smoothscale(pygame.image.load("assets/pipe-body.png").convert_alpha(), (pipe_width, screen_height - self.y - pipe_hole_height - 24)) 
        self.bottom_head = pygame.transform.smoothscale(pygame.image.load("assets/pipe-head.png").convert_alpha(), (pipe_width, 24))

    def get_top_bounds(self):
        return Rectangle(self.x, 0, pipe_width, self.y)

    def get_bottom_bounds(self):
        return Rectangle(self.x, self.y + pipe_hole_height, pipe_width, screen_height - self.y - pipe_hole_height)