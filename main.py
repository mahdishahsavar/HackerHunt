# main.py
import pygame
import sys
from firewall import ask_question_firewall, detect_collision
import random
import tkinter as tk
from tkinter import simpledialog

def init_pygame():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("HackerHunt")
    return screen, width, height

def draw_player(screen, color, position, size, path_orientation):
    if path_orientation == 'horizontal':
        adjusted_position = (position[0], position[1] - size // 2)
    elif path_orientation == 'vertical':
        adjusted_position = (position[0] - size // 2, position[1])
    pygame.draw.rect(screen, color, (*adjusted_position, size, size))

def draw_nodes(screen, color, nodes, size):
    for node_pos in nodes:
        pygame.draw.circle(screen, color, node_pos, size)

def draw_paths(screen, color, paths):
    for start, end in paths:
        pygame.draw.line(screen, color, start, end, 5)

def detect_node_collision(player_pos, node_pos, player_size, node_size):
    p_x, p_y = player_pos
    n_x, n_y = node_pos
    distance = ((p_x - n_x) ** 2 + (p_y - n_y) ** 2) ** 0.5
    if distance < player_size / 2 + node_size:
        return True
    return False

def is_on_path(old_pos, new_pos, paths):
    for start, end in paths:
        if start[0] == end[0]:
            if start[0] == new_pos[0] and start[1] <= new_pos[1] <= end[1]:
                return True
        elif start[1] == end[1]:
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
    root.withdraw()
    user_input = simpledialog.askinteger("Node Challenge", "Enter the correct number to delete the node:")
    root.destroy()
    correct_number = 42
    if user_input is not None and user_input == correct_number:
        return True
    return False

def generate_random_firewall_positions(paths, num_firewalls, start_pos):
    possible_positions = []
    for start, end in paths:
        if start[0] == end[0]:  # Vertical path
            for y in range(start[1], end[1] + 1, 50):
                possible_positions.append((start[0], y))
        elif start[1] == end[1]:  # Horizontal path
            for x in range(start[0], end[0] + 1, 50):
                possible_positions.append((x, start[1]))

    # Exclude the starting position
    if start_pos in possible_positions:
        possible_positions.remove(start_pos)
    
    return random.sample(possible_positions, num_firewalls)

def main():
    screen, width, height = init_pygame()
    clock = pygame.time.Clock()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 128, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    player_size = 30
    player_color = WHITE
    player_pos = [100, 100]
    player_speed = 5
    path_orientation = 'horizontal'

    problems = ["P1", "P2", "P3", "P4", "P5"]

    paths = [
        ((100, 100), (700, 100)),
        ((100, 100), (100, 500)),
        ((700, 100), (700, 500)),
        ((100, 500), (700, 500)),
        ((400, 100), (400, 500)),
        ((200, 100), (200, 200)),
        ((600, 100), (600, 200)),
        ((300, 500), (500, 500)),
        ((100, 300), (300, 300)),
        ((500, 300), (700, 300)),
        ((650, 100), (650, 150)),
        ((100, 450), (350, 450)),
    ]

    nodes = [end for _, end in paths]
    node_size = 10
    node_color = GREEN
    node_problems = {tuple(node): random.choice(problems) for node in nodes}

    # Randomly generate firewall positions
    num_firewalls = 5
    firewall_positions = generate_random_firewall_positions(paths, num_firewalls, tuple(player_pos))
    firewall_size = 15
    firewall_color = RED

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
        
        for firewall_pos in firewall_positions:
            pygame.draw.circle(screen, firewall_color, firewall_pos, firewall_size)

        for node_pos in nodes[:]:
            if detect_node_collision(player_pos, node_pos, player_size, node_size):
                if ask_question_node():
                    nodes.remove(node_pos)
                    print(f"Problem solved at node: {node_problems[tuple(node_pos)]}")
                else:
                    print("You Need To Come Back")
        
        for firewall_pos in firewall_positions[:]:
            if detect_node_collision(player_pos, firewall_pos, player_size, firewall_size):
                difficulty = 'medium'  # Example difficulty level
                if ask_question_firewall(difficulty):
                    firewall_positions.remove(firewall_pos)
                    print(f"Firewall at {firewall_pos} cleared")
                else:
                    print("Firewall challenge failed. You need to try again.")
                    
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
