import pygame

screen_width = 1200
screen_height = 700

gravity = 0.6

bird_colors = [ "black", "white", "green", "red", "blue", "yellow", "orange", "turquoise", "pink", "violet" ]

pipe_count = 5
pipe_init_offset = 500
pipe_gap = 300
pipe_width = 58
pipe_hole_height = 160
pipe_velocity = 4

closest_pipe_index = 0

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)

large_font = pygame.font.SysFont(None, 35)
medium_font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 23)