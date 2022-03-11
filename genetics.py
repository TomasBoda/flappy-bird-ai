import random
import copy
from neuralnetwork import NeuralNetwork
from config import bird_colors
from bird import Bird

def crossover(brain_1, brain_2) -> Bird:
    new_weights = copy.deepcopy(brain_1.weights)

    for i in range(len(brain_1.weights)):
        for j in range(len(brain_1.weights[i])):
            for k in range(len(brain_1.weights[i][j])):
                chosen_weights = random.choice([ brain_1.weights, brain_2.weights ])

                new_weights[i][j][k] = copy.deepcopy(chosen_weights[i][j][k])

    return Bird(0, "Crossover", NeuralNetwork([ 2, 6, 1 ], new_weights))

def spawn_new_generation(dead) -> list:
    brains = [ bird.brain for bird in dead ]
    next_gen = []

    for i in range(4):
        next_gen.append(Bird(0, "Copy of winner",  brains[-i]))

    next_gen.append(crossover(brains[-1], brains[-2]))

    for i in range(3):
        winners = [ brains[-1], brains[-2], brains[-3], brains[-4] ]
        winner_1 = random.choice(winners)
        winner_2 = random.choice(winners)

        next_gen.append(crossover(winner_1, winner_2))

    next_gen.append(Bird(0, "Random"))
    next_gen.append(Bird(0, "Random"))

    for i in range(10):
        next_gen[i].y = 25 + (50 * i)
        next_gen[i].set_image(bird_colors[i])

    return next_gen
