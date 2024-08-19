import random
import pygame
import tkinter as tk
from utils.node_class import Node
from utils.player_class import Player  # Import the Player class
from utils.path_class import Path
from password_cracker.user_interface import PasswordCracker
from network_sniffer.user_interface import NetworkSniffer
from ip_challenge.Ip_Address_challenge import IPAddressChallenge

pygame.font.init()
# Fonts
pygame.init()
font = pygame.font.Font(None, 36)

PROBLEMS = [PasswordCracker(), NetworkSniffer(), IPAddressChallenge()]# Steganography()]

PROBLEM_IDS_WITH_NODE = []
# Define game states
MENU, GAME, HIGH_SCORES = 0, 1, 2
game_state = MENU

menu_items = ['Start Game', 'High Scores', 'Options', 'Quit']

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def init_pygame():
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("HackerHunt")
    return screen, width, height

def read_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            scores = [line.strip().split(",") for line in file]
        return sorted(scores, key=lambda x: -int(x[1]))[:5]  # Get top 5 scores
    except FileNotFoundError:
        return []

def write_high_score(name, score):
    with open("high_scores.txt", "a") as file:
        file.write(f"{name},{score}\n")

def draw_high_scores(screen):
    high_scores = read_high_scores()
    screen.fill(BLACK)
    title = font.render("High Scores", True, WHITE)
    screen.blit(title, (350, 100))
    for index, score in enumerate(high_scores):
        text = font.render(f"{index + 1}. {score[0]}: {score[1]}", True, WHITE)
        screen.blit(text, (350, 150 + 40 * index))

def ask_question_with_node_class(node):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    challenge_id = node.id
    challenge = None
    for problem in PROBLEMS:
        if problem.id == challenge_id:
            challenge = problem
    if challenge is not None:
        challenge.run()
    else:
        print("No valid challenge found for ID:", challenge_id)
    
def get_challenge_id():
    for problem in PROBLEMS:
        if not problem.id in PROBLEM_IDS_WITH_NODE:
            PROBLEM_IDS_WITH_NODE.append(problem.id)
            return problem.id
        elif len(PROBLEM_IDS_WITH_NODE) == len(PROBLEMS):
            return "all_current_problems_exhausted_id"

def choose_background():
    key = random.randint(1,2)
    choices = {
        1 : "binary.jpg",
        2 : "circuit_board.jpg",
    }
    path = f"utils/resources/{choices[key]}"
    return pygame.image.load(path)

BACKGROUND = choose_background()

def add_background(screen, background):
    screen.blit(background, (0, 0))

def draw_menu(screen, selected_item):
    background_image = pygame.image.load('Menu_BG.jpg').convert()
    screen.blit(background_image, (0, 0))
    for index, item in enumerate(menu_items):
        if index == selected_item:
            label = font.render(item, True, BLUE)  # Highlight the selected item
        else:
            label = font.render(item, True, WHITE)
        # Calculate position of text
        width = label.get_width()
        height = label.get_height()
        posX = (800 - width) / 2  # Center align text
        posY = (150 + index * 50)  # Start at y = 150 and space items by 50 pixels
        screen.blit(label, (posX, posY))

def main_game(screen, width, height, player, nodes, paths):
    node_size = 10
    node_color = GREEN
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()
    player.move(keys, paths)  # Update player's position
    #        screen.blit(background, (0,0))  #MB(7/22/24)
    for path in paths:
        path.draw(screen)
    for node in nodes:
        node.draw(screen)

    player.draw(screen)  # Draw the player
    for node in nodes:
        if node.detect_collision(player.position,player.size):
            if ask_question_with_node_class(node):
                nodes.remove(node)
                player.score += 100
                print(f"Problem solved at node: {node.id}")
            else:
                print("You Need To Come Back")

def main():
    screen, width, height = init_pygame()

    # Define paths
    paths = [
        Path((100, 100), (700, 100), BLUE),
        Path((100, 100), (100, 500), BLUE),
        Path((700, 100), (700, 500), BLUE),
        Path((100, 500), (700, 500), BLUE),
        Path((400, 100), (400, 500), BLUE),
        Path((200, 100), (200, 200), BLUE),
        Path((600, 100), (600, 200), BLUE),
        Path((300, 500), (500, 500), BLUE),
        Path((100, 300), (300, 300), BLUE),
        Path((500, 300), (700, 300), BLUE),
        Path((650, 100), (650, 150), BLUE),
        Path((100, 450), (350, 450), BLUE),
    ]

    # Define node properties
    nodes = [Node(get_challenge_id(), path.end, 10, GREEN) for path in paths]

    clock = pygame.time.Clock()
    global game_state
    player = Player((100, 100), BLACK, 60, 5)

   

    selected_item = 0
    running = True
    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == MENU:
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        if menu_items[selected_item] == 'Quit':
                            running = False
                        elif menu_items[selected_item] == 'Start Game':
                            game_state = GAME
                elif game_state == GAME:
                    if event.key == pygame.K_ESCAPE:
                        game_state = MENU

        if game_state == MENU:
            draw_menu(screen, selected_item)
        elif game_state == GAME:
            main_game(screen, width, height, player, nodes, paths)
        elif game_state == HIGH_SCORES:
            draw_high_scores(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

