import pygame
from config import screen, screen_width, screen_height, bird_colors, pipe_count, pipe_gap, pipe_init_offset, pipe_width, closest_pipe_index
from genetics import spawn_new_generation
from pipe import Pipe
from bird import Bird
from dashboard import Dashboard

class Game:
    def __init__(self):
        # vtáky, ktoré sú živé a hrajú
        self.birds: list = self.init_birds()
        # vtáky, ktoré zomreli
        self.dead: list = []
        # potrubia
        self.pipes: list = self.init_pipes()

        # počítadlo generácie
        self.generation = 1

        self.background = pygame.image.load("assets/background.png").convert_alpha()
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height)) 

        self.dashboard = Dashboard()

    def render(self):
        screen.blit(self.background, (0, 0))

        for pipe in self.pipes:
            pipe.render()

        for bird in self.birds:
            bird.render()

        self.dashboard.render(self.birds, self.dead, self.generation)

    def update(self):
        global closest_pipe_index

        # keď sú všetky vtáky mŕtve, resetuje sa hra
        if len(self.birds) == 0:
            self.reset_game()
            return
        
        for pipe in self.pipes:
            pipe.update()
            self.loop_pipes(pipe)

        self.calculate_closest_pipe()

        for bird in self.birds:
            # kolízia vtáka so zemou alebo najbližším potrubím
            # vták zomrie
            if bird.y <= 0 or bird.y + bird.height >= screen_height or bird.get_bounds().intersects(self.pipes[closest_pipe_index].get_top_bounds()) or bird.get_bounds().intersects(self.pipes[closest_pipe_index].get_bottom_bounds()):
                self.dead.append(bird)
                self.birds.remove(bird)
                break

            bird.update(self.pipes[closest_pipe_index])

    # funkcia, ktorá vypočítava, ktoré potrubie je najbližšie ku vtákom,
    # takže pri kolíziach stačí pozerať iba toto potrubie, nie všetky
    def calculate_closest_pipe(self):
        global closest_pipe_index

        if self.pipes[closest_pipe_index].x + pipe_width < self.birds[0].x:
            closest_pipe_index = (closest_pipe_index + 1) % len(self.pipes)

            # počítadlo skóre
            for bird in self.birds:
                bird.score += 1

    # funkcia, ktorá sa stará o nekonečný cyklus potrubí
    # keď je potrubie mimo okna (naľavo), posunie ho čo najviac
    # napravo za všetky ostatné potrubia
    def loop_pipes(self, pipe):
        if pipe.x + pipe_width >= 0:
            return

        # získame x súradnicu posledného potrubia
        max_x = max(list(map(lambda p: p.x, self.pipes)))

        pipe.x = max_x + pipe_gap
        pipe.y = pipe.generate_gap_position()
        pipe.repaint_images()

    # prvotná inicializácia vtákov
    def init_birds(self) -> list:
        birds = []

        for i in range(10):
            bird = Bird(50 + (i * 60), "Random")
            bird.set_image(bird_colors[i])
            birds.append(bird)

        return birds

    # prvotná inicializácia potrubí
    def init_pipes(self) -> list:
        global pipe_count, pipe_init_offset, pipe_gap

        return [ Pipe(pipe_init_offset + (i * pipe_gap)) for i in range(pipe_count) ]

    # resetovanie hry
    # vytvorí sa nová generácia vtákov
    # vygenerujú sa nanovo potrubia
    # počítadlo generácie sa nastaví na 1
    def reset_game(self):
        global closest_pipe_index, spawn_new_generation

        self.birds = spawn_new_generation(self.dead)
        self.dead = []
        self.pipes = self.init_pipes()
        closest_pipe_index = 0

        self.generation += 1