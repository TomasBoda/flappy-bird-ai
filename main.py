# by Tomáš Boďa

import pygame
from game import Game
import config

pygame.display.set_caption("Flappy Bird Neural Network using Genetic Algorithm")
pygame.display.flip()

game = Game()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    config.screen.fill((255, 255, 255))

    game.render()
    game.update()

    pygame.display.update()

pygame.quit()