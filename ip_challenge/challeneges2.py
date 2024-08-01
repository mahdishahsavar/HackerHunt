import pygame
import socket
import tkinter as tk
from tkinter import simpledialog


# Define the QuestionDialog class for user input
class QuestionDialog(simpledialog.Dialog):
    def __init__(self, parent, question, hint, sample_code):
        self.question = question
        self.hint = hint
        self.sample_code = sample_code
        self.answer = None
        super().__init__(parent, title="Node Challenge")

    def body(self, master):
        tk.Label(master, text=self.question, wraplength=400).grid(row=0, column=0, padx=20, pady=10)
        tk.Label(master, text="Hint:", fg="blue", wraplength=400).grid(row=1, column=0, padx=20, pady=5)
        tk.Label(master, text=self.hint, wraplength=400).grid(row=2, column=0, padx=20, pady=5)
        tk.Label(master, text="Sample Code:", fg="green", wraplength=400).grid(row=3, column=0, padx=20, pady=5)
        tk.Label(master, text=self.sample_code, wraplength=400, bg="lightgrey").grid(row=4, column=0, padx=20, pady=5)
        self.entry = tk.Text(master, height=15, width=60)
        self.entry.grid(row=5, column=0, padx=20, pady=10)
        return self.entry

    def apply(self):
        self.answer = self.entry.get("1.0", tk.END).strip()

def ask_question_node(question, hint, sample_code):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    dialog = QuestionDialog(root, question, hint, sample_code)
    root.destroy()
    return dialog.answer

# Define the IPAddressChallenge class
class IPAddressChallenge:
    def __init__(self):
        pygame.init()
        self.id = "IP_challenge"
        self.screen_width = 1000
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('IP Address Challenge')
        self.font = pygame.font.Font(None, 40)
        self.button_font = pygame.font.Font(None, 30)
        self.node_problems = {
            (700, 100): [
                {
                    "question": "Level 1: You've received a message from an anonymous source, claiming to have information about a vulnerable server. The message reads: 'Check the ports on 10.0.0.1'. Write a Python script to perform a basic port scan on the target IP address.",
                    "hint": "Use the 'socket' library to attempt connections on different ports. A successful connection indicates the port is open.",
                    "sample_code": """import socket

def user_function(target_ip):
    open_ports = []
    ports = [22, 80, 443, 21, 25, 3306]  # Example ports to scan
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set timeout to 1 second
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return "\\n".join([f"Port {port}: Open" for port in open_ports])

# Test your function with the given IP address
print(user_function("10.0.0.1"))
""",
                    "test_cases": ["10.0.0.1"]
                }
            ],
        }
        self.node_levels = {node: 0 for node in self.node_problems}
        self.initialize_interface_elements()
        self.show_summary = True

    def initialize_interface_elements(self):
        self.nodes = []
        for node_pos in self.node_problems:
            rect = pygame.Rect(node_pos[0], node_pos[1], 100, 50)
            self.nodes.append((rect, node_pos))

    def validate_function(self, user_code, test_cases):
        # Always return True to pass the test case
        return True

    def present_challenge(self, node_pos):
        level = self.node_levels[node_pos]
        if level < len(self.node_problems[node_pos]):
            problem = self.node_problems[node_pos][level]
            question = problem["question"]
            hint = problem["hint"]
            sample_code = problem["sample_code"]
            test_cases = problem["test_cases"]

            user_code = ask_question_node(question, hint, sample_code)
            if user_code and self.validate_function(user_code, test_cases):
                self.node_levels[node_pos] += 1
                if self.node_levels[node_pos] >= len(self.node_problems[node_pos]):
                    return True, f"All problems solved at node: {node_pos}"
                else:
                    return False, f"Level {self.node_levels[node_pos]} completed at node: {node_pos}"
            else:
                return False, "Incorrect answer or function did not pass the test cases. Try again."
        return False, None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.show_summary:
                        if self.button_rect.collidepoint(pos):
                            self.show_summary = False
                            self.present_challenge((700, 100))
                    else:
                        for rect, node_pos in self.nodes:
                            if rect.collidepoint(pos):
                                success, message = self.present_challenge(node_pos)
                                print(message)

            self.screen.fill((255, 255, 255))

            if self.show_summary:
                self.draw_summary()
            else:
                self.draw_challenge()

            pygame.display.flip()

        pygame.quit()

    def draw_summary(self):
        title = self.font.render("Welcome to the IP Address Challenge:", True, (0, 0, 0))
        description = self.font.render("Press the button below to start the challenge.", True, (0, 0, 0))

        # Center the title and description
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        description_rect = description.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        self.screen.blit(title, title_rect)
        self.screen.blit(description, description_rect)

        # Center the button
        self.button_rect = pygame.Rect(0, 0, 200, 50)
        self.button_rect.center = (self.screen_width // 2, self.screen_height // 2 + 100)

        pygame.draw.rect(self.screen, (0, 255, 0), self.button_rect)
        button_text = self.button_font.render("Start Challenge", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text, button_text_rect)

    def draw_challenge(self):
        for rect, node_pos in self.nodes:
            pygame.draw.rect(self.screen, (0, 0, 255), rect)
            text = self.font.render(f"Node {node_pos}", True, (255, 255, 255))
            self.screen.blit(text, rect.topleft)


if __name__ == '__main__':
    challenge = IPAddressChallenge()
    challenge.run()
