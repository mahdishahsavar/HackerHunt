import pygame
class Node:
    def __init__(self, id, position, size, color):
        self.id = id
        self.position = position
        self.size = size
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.size)

    def detect_collision(self, player_pos, player_size):
        p_x, p_y = player_pos
        n_x, n_y = self.position
        distance = ((p_x - n_x) ** 2 + (p_y - n_y) ** 2) ** 0.5
        return distance < player_size / 2 + self.size
