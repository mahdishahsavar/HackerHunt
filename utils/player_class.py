import pygame

class Player:
    def __init__(self, position, color, size, speed):
        self.position = list(position)  # Convert tuple to list if needed for mutability
        self.color = color
        self.size = size
        self.speed = speed
        self.path_orientation = 'horizontal'  # Initial orientation
        #self.image = pygame.transform.scale(pygame.image.load('utils/resources/Hacker.png'), (size, size))
        self.image = pygame.image.load('utils/resources/Hacker.png').convert_alpha()
        # Scale the image to the desired size
        self.image = pygame.transform.scale(self.image, (size, size))
        self.score = 0
    def move(self, keys, paths):
        # Handle movement, check path constraints
        if keys[pygame.K_LEFT]:
            new_pos = (self.position[0] - self.speed, self.position[1])
            if self.is_on_path(self.position, new_pos, paths):
                self.position[0] -= self.speed
                self.path_orientation = 'horizontal'
        if keys[pygame.K_RIGHT]:
            new_pos = (self.position[0] + self.speed, self.position[1])
            if self.is_on_path(self.position, new_pos, paths):
                self.position[0] += self.speed
                self.path_orientation = 'horizontal'
        if keys[pygame.K_UP]:
            new_pos = (self.position[0], self.position[1] - self.speed)
            if self.is_on_path(self.position, new_pos, paths):
                self.position[1] -= self.speed
                self.path_orientation = 'vertical'
        if keys[pygame.K_DOWN]:
            new_pos = (self.position[0], self.position[1] + self.speed)
            if self.is_on_path(self.position, new_pos, paths):
                self.position[1] += self.speed
                self.path_orientation = 'vertical'

    def draw(self, screen):
        # Draw the player on the screen based on the current orientation
        if self.path_orientation == 'horizontal':
            adjusted_position = (self.position[0], self.position[1] - self.size // 2)
        elif self.path_orientation == 'vertical':
            adjusted_position = (self.position[0] - self.size // 2, self.position[1])
        screen.blit(self.image, adjusted_position)

    def is_on_path(self, old_pos, new_pos, paths):
        for path in paths:
            if path.start[0] == path.end[0]:  # Vertical path
                if path.start[0] == new_pos[0] and path.start[1] <= new_pos[1] <= path.end[1]:
                    return True
            elif path.start[1] == path.end[1]:  # Horizontal path
                if path.start[1] == new_pos[1] and path.start[0] <= new_pos[0] <= path.end[0]:
                    return True
        return False