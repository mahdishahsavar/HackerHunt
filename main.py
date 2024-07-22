import pygame
import sys
import tkinter as tk
from tkinter import simpledialog

# Initialize Pygame
def init_pygame():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("HackerHunt")
    return screen, width, height

# Draw the player on the screen
def draw_player(screen, color, position, size, path_orientation):
    if path_orientation == 'horizontal':
        adjusted_position = (position[0], position[1] - size // 2)
    elif path_orientation == 'vertical':
        adjusted_position = (position[0] - size // 2, position[1])
    pygame.draw.rect(screen, color, (*adjusted_position, size, size))

# Draw the nodes on the screen
def draw_nodes(screen, color, nodes, size):
    for node_pos in nodes:
        pygame.draw.circle(screen, color, node_pos, size)

# Draw the paths on the screen
def draw_paths(screen, color, paths):
    for start, end in paths:
        pygame.draw.line(screen, color, start, end, 5)  # Draw line with thickness of 5

# Detect collision between player and node
def detect_collision(player_pos, node_pos, player_size, node_size):
    p_x, p_y = player_pos
    n_x, n_y = node_pos
    distance = ((p_x - n_x) ** 2 + (p_y - n_y) ** 2) ** 0.5
    if distance < player_size / 2 + node_size:
        return True
    return False

# Check if the player is on a path
def is_on_path(old_pos, new_pos, paths):
    for start, end in paths:
        if start[0] == end[0]:  # Vertical path
            if start[0] == new_pos[0] and start[1] <= new_pos[1] <= end[1]:
                return True
        elif start[1] == end[1]:  # Horizontal path
            if start[1] == new_pos[1] and start[0] <= new_pos[0] <= end[0]:
                return True
    return False

# Move the player based on key inputs
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

# Custom dialog box for asking questions
class QuestionDialog(simpledialog.Dialog):
    def __init__(self, parent, question, test_cases):
        self.question = question
        self.test_cases = test_cases
        self.answer = None
        super().__init__(parent, title="Node Challenge")

    def body(self, master):
        tk.Label(master, text=self.question, wraplength=400).grid(row=0, column=0, padx=20, pady=20)
        self.entry = tk.Text(master, height=10, width=50)
        self.entry.grid(row=1, column=0, padx=20, pady=20)
        return self.entry

    def apply(self):
        self.answer = self.entry.get("1.0", tk.END).strip()

def ask_question_node(question, test_cases):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    dialog = QuestionDialog(root, question, test_cases)
    root.destroy()
    return dialog.answer
def validate_function(user_code, test_cases):
    try:
        # Define a local dictionary to store the user's function
        local_dict = {}
        exec(user_code, {}, local_dict)

        # Extract the function from the local dictionary
        user_function = local_dict.get("user_function")

        if not user_function:
            print("Function 'user_function' not defined.")
            return False

        # Run the test cases
        for test_input, expected_output in test_cases:
            if isinstance(test_input, tuple):
                result = user_function(*test_input)
            else:
                result = user_function(test_input)
            assert result == expected_output, f"Test failed: {test_input} => {result} != {expected_output}"

        return True

    except Exception as e:
        print(f"Exception during function validation: {e}")
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

    # Define coding problems for each node with multiple levels
    node_problems = {
        (700, 100): [
            {
                "question": "Level 1: Write a function `user_function` that takes two integers and returns their sum.",
                "test_cases": [((1, 2), 3), ((-1, 1), 0), ((10, 5), 15)]
            },
            {
                "question": "Level 2: Write a function `user_function` that takes three integers and returns their sum.",
                "test_cases": [((1, 2, 3), 6), ((-1, 1, -1), -1), ((10, 5, 1), 16)]
            },
            {
                "question": "Level 3: Write a function `user_function` that takes an integer and returns its factorial.",
                "test_cases": [(3, 6), (5, 120), (0, 1)]
            },
            {
                "question": "Level 4: Write a function `user_function` that takes a list of integers and returns their sum.",
                "test_cases": [([1, 2, 3], 6), ([0, 0, 0], 0), ([10, -10, 20], 20)]
            },
        ],
        
    }

    # Track current level for each node
    node_levels = {node: 0 for node in node_problems}

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
                if node_pos in node_problems:
                    level = node_levels[node_pos]
                    if level < len(node_problems[node_pos]):
                        question = node_problems[node_pos][level]["question"]
                        test_cases = node_problems[node_pos][level]["test_cases"]
                        user_code = ask_question_node(question, test_cases)
                        if user_code and validate_function(user_code, test_cases):
                            node_levels[node_pos] += 1
                            if node_levels[node_pos] >= len(node_problems[node_pos]):
                                nodes.remove(node_pos)
                                print(f"All problems solved at node: {node_pos}")
                            else:
                                print(f"Level {node_levels[node_pos]} completed at node: {node_pos}")
                        else:
                            print("Incorrect answer or function did not pass the test cases. Try again.")

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
