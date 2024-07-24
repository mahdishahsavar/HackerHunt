import pygame

class Path:
    def __init__(self, start, end, color, thickness=5):
        self.start = start
        self.end = end
        self.color = color
        self.thickness = thickness

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.start, self.end, self.thickness)