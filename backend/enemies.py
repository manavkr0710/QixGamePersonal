import pygame


class Sparx:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path_index = 0  # Initialize the path index to 0

    def draw(self, screen):
        pygame.draw.circle(screen, "orange", (self.x, self.y), 7)
class Qix:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 3
        self.dy = 3

    def reset(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, "purple", (int(self.x), int(self.y)), 14)