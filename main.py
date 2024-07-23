import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

def init_pygame():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("HackerHunt")
    return screen, width, height

def draw_player(screen, color, position, size, path_orientation):
    # Offset player position to center on the path
    if path_orientation == 'horizontal':
        # Adjust y-position to center vertically on a horizontal path
        adjusted_position = (position[0], position[1] - size // 2)
    elif path_orientation == 'vertical':
        # Adjust x-position to center horizontally on a vertical path
        adjusted_position = (position[0] - size // 2, position[1])
    pygame.draw.rect(screen, color, (*adjusted_position, size, size))

def draw_nodes(screen, color, nodes, size):
    for node_pos in nodes:
        pygame.draw.circle(screen, color, node_pos, size)

def draw_paths(screen, color, paths):
    for start, end in paths:
        pygame.draw.line(screen, color, start, end, 5)  # Draw line with thickness of 5

def detect_collision(player_pos, node_pos, player_size, node_size):
    p_x, p_y = player_pos
    n_x, n_y = node_pos
    distance = ((p_x - n_x) ** 2 + (p_y - n_y) ** 2) ** 0.5
    if distance < player_size / 2 + node_size:
        return True
    return False

def is_on_path(old_pos, new_pos, paths):
    # Simplistic collision detection that checks if a move stays on a path
    for start, end in paths:
        if start[0] == end[0]:  # Vertical path
            if start[0] == new_pos[0] and start[1] <= new_pos[1] <= end[1]:
                return True
        elif start[1] == end[1]:  # Horizontal path
            if start[1] == new_pos[1] and start[0] <= new_pos[0] <= end[0]:
                return True
    return False

def move_player(player_pos, keys, paths, speed):
    current_orientation = ""
    if keys[pygame.K_LEFT]:
        new_pos = (player_pos[0] - speed, player_pos[1])
        if is_on_path(player_pos, new_pos, paths):
            player_pos[0] -= speed
            current_orientation = 'horizontal'
    if keys[pygame.K_RIGHT]:
        new_pos = (player_pos[0] + speed, player_pos[1])
        if is_on_path(player_pos, new_pos, paths):
            player_pos[0] += speed
            current_orientation = 'horizontal'
    if keys[pygame.K_UP]:
        new_pos = (player_pos[0], player_pos[1] - speed)
        if is_on_path(player_pos, new_pos, paths):
            player_pos[1] -= speed
            current_orientation = 'vertical'
    if keys[pygame.K_DOWN]:
        new_pos = (player_pos[0], player_pos[1] + speed)
        if is_on_path(player_pos, new_pos, paths):
            player_pos[1] += speed
            current_orientation = 'vertical'
    return current_orientation

def ask_question_node():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # Prompt the user for a number
    user_input = simpledialog.askinteger("Node Challenge", "Enter the correct number to delete the node:")
    root.destroy()
    # Here you can implement any validation logic
    correct_number = 42  # This is just an example
    if user_input is not None and user_input == correct_number:
        return True
    return False

def main():
    screen, width, height = init_pygame()
    clock = pygame.time.Clock()

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 128, 255)
    GREEN = (0, 255, 0)

    # Define player properties
    player_size = 30
    player_color = WHITE
    player_pos = [100, 100]  # Starting position on the first path
    player_speed = 5
    path_orientation = 'horizontal'
    # Define problems
    problems = ["P1", "P2", "P3", "P4", "P5"]

    # Define paths
    paths = [
        ((100, 100), (700, 100)),  # Main horizontal path
        ((100, 100), (100, 500)),  # Main vertical path from the start
        ((700, 100), (700, 500)),  # Another vertical path
        ((100, 500), (700, 500)),  # Bottom horizontal path
        ((400, 100), (400, 500)),  # Central vertical path
        ((200, 100), (200, 200)),  # Dead-end vertical path
        ((600, 100), (600, 200)),  # Dead-end vertical path
        ((300, 500), (500, 500)),  # Short horizontal path at the bottom
        ((100, 300), (300, 300)),  # Short horizontal path in the middle left
        ((500, 300), (700, 300)),  # Short horizontal path in the middle right
        ((650, 100), (650, 150)),  # Dead-end vertical path
        ((100, 450), (350, 450)),  # Dead-end horizontal path
    ]
    # Define node properties
    nodes = [end for _, end in paths]
    node_size = 10
    node_color = GREEN
    node_problems = {tuple(node): random.choice(problems) for node in nodes}

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        path_orientation_flag = move_player(player_pos, keys, paths, player_speed)
        if path_orientation_flag == "horizontal" or path_orientation_flag == "vertical":
            path_orientation = path_orientation_flag
        screen.fill(BLACK)
        draw_paths(screen, BLUE, paths)
        draw_player(screen, player_color, player_pos, player_size, path_orientation)
        draw_nodes(screen, node_color, nodes, node_size)

        for node_pos in nodes[:]:
            if detect_collision(player_pos, node_pos, player_size, node_size):
                if ask_question_node():
                    nodes.remove(node_pos)
                    print(f"Problem solved at node: {node_problems[tuple(node_pos)]}")
                else:
                    print("You Need To Come Back")
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
