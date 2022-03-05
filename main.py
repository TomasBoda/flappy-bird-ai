# Flappy Bird Neural Network using Genetic Algorithm for learning
# Tomáš Boďa, 1. ročník, kruh 31
# zimný semester 2021/2022
# Programování I NPRG030

import pygame
from game import Game
import config

pygame.display.set_caption("Flappy Bird Neural Network using Genetic Algorithm")
pygame.display.flip()

game = Game()

running = True

# hlavný gameloop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    config.screen.fill((255, 255, 255))

    # hlavná logika renderovania
    game.render()
    # hlavná logika hry
    game.update()

    pygame.display.update()

pygame.quit()