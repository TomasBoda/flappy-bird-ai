import pygame
from config import screen, gravity
from pipe import pipe_width
from rectangle import Rectangle
from neuralnetwork import NeuralNetwork

class Bird:
    def __init__(self, y, type, brain = None):
        self.x = 100
        self.y = y
        self.width = 51
        self.height = 36
        
        # type = RANDOM / COPY OF WINNER / CROSSOVER
        self.type = type
        self.velocity = 0

        self.image = pygame.image.load("assets/bird.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height)) 

        self.brain = NeuralNetwork([ 2, 6, 1 ]) if not brain else brain
        self.score = 0

    def render(self):
        screen.blit(self.image, (self.x, self.y))

    def update(self, closest_pipe):
        self.apply_physics()
        self.y += self.velocity

        self.predict(closest_pipe)

    # funkcia, ktorá pošle nové dáta do neurálnej siete
    # na základe výsledkov neurálnej siete rozhodne,
    # či má vták skočiť alebo nič nespraviť
    def predict(self, closest_pipe):
        closest_pipe_horizontal_distance = closest_pipe.x + pipe_width - self.x
        closest_pipe_vertical_distance = self.y - closest_pipe.y

        # do neurálnej siete pošleme dva parametre:
        # vertikálnu a horizontálnu vzdialenosť od najbližšieho potrubia
        self.brain.feed_forward([ closest_pipe_horizontal_distance, closest_pipe_vertical_distance ])
        
        output = self.brain.get_output_values()[0]

        # návratová hodnota je interval [0, 1]:
        # vták skočí, pokiaľ je hodnota >= 0.5
        if output >= 0.5:
            self.jump()

    def jump(self):
        self.velocity = -7

    # funckia, ktorá rieši gravitáciu a zrýchlenie padajúceho vtáka
    def apply_physics(self):
        self.velocity += gravity

        if self.velocity > 9:
            self.velocity = 9

    def set_image(self, color):
        self.image = pygame.image.load("assets/bird-" + color + ".png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height)) 

    # funkcia používaná na výpočet kolízie
    def get_bounds(self):
        return Rectangle(self.x, self.y, self.width, self.height)