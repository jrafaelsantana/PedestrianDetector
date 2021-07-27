import pygame
import numpy as np


class Viewer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.rgb_data = np.zeros(shape=(480, 640, 3), dtype=np.uint8)

    def update_rgb(self, data):
        self.rgb_data = data

    def update(self):
        return self.rgb_data

    def start(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            Z = self.update()
            surf = pygame.surfarray.make_surface(Z)
            self.screen.blit(surf, (0, 0))

            pygame.display.update()

        pygame.quit()
