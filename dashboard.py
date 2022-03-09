import pygame
from config import screen, screen_width, screen_height, large_font, medium_font, small_font

# komponent na renderovanie statusu vtákov, ich skóre, generácie atď.
class Dashboard:
    def __init__(self):
        self.width = 350
        self.height = screen_height - 40
        self.x = screen_width - self.width - 20
        self.y = 20

        self.bird_image = pygame.image.load("assets/bird.png").convert_alpha()

    def render(self, birds, dead, generation):
        # dashboard background
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x, self.y, self.width, self.height), 0, 5)

        numbers = [ 1, 2, 3 ]
        number_endings = [ "st", "nd", "rd", "th" ]
        gen_number = int(str(generation)[-1]) - 1
        generation_number = str(generation) + number_endings[gen_number] if generation in numbers else str(generation) + "th"

        # číslo generácie
        gen_text = large_font.render(generation_number + " generation", True, (0, 0, 0))
        screen.blit(gen_text, (self.x + 20, self.y + 20, gen_text.get_rect().width, gen_text.get_rect().height))

        all_birds = birds + list(reversed(dead))

        for i in range(len(all_birds)):
            bird = all_birds[i]

            width = self.width - 40
            height = int((self.height - 40 - gen_text.get_rect().height - 20) / 10)
            x = self.x + 20
            y = self.y + 20 + gen_text.get_rect().height + 20 + (i * height)

            # obrázkov vtáka
            screen.blit(pygame.transform.smoothscale(bird.image, (int((height - 26) * 1.5), height - 26)), (x + 13, y + 13))

            # typ vtáka (RANDOM / COPY OF WINNER / CROSSOVER)
            type_text = small_font.render(str(bird.type), True, (0, 0, 0))
            screen.blit(type_text, (x + 85, int(y + (height / 2) - (type_text.get_rect().height / 2)), type_text.get_rect().width, type_text.get_rect().height))

            # skóre vtáka
            score_text = medium_font.render(str(bird.score), True, (0, 0, 0))
            screen.blit(score_text, (x + width - score_text.get_rect().width, int(y + (height / 2) - (score_text.get_rect().height / 2)), score_text.get_rect().width, score_text.get_rect().height))

            # na mŕtve vtáky nastaviť tmavý overlay,
            # aby sa dali rozlíšiť od živých vtákov
            if i >= len(birds):
                s = pygame.Surface((width, height))
                s.set_alpha(128)
                s.fill((255, 255, 255))
                screen.blit(s, (x, y))
            