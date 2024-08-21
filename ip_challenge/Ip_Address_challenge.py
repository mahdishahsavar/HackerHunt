import pygame
from loguru import logger
import random
import socket
import sys

class IPChallenge:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen settings
        self.screen_width = 1000
        self.screen_height = 800
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.screen = self.initialize_screen()
        self.font = self.set_font(None, 20)
        self.instruction_text = self.get_challenge_instructions()
        self.editor_rect = self.render_editor_surface()
        self.running = True
        self.tab = ' ' * 5
        self.users_code = "def scan_ports(target_ip): \n" + self.tab
        self.run_button = self.render_run_button()
        self.target_ip = "10.0.0.1"  # Target IP for the challenge
        self.expected_result = self.get_expected_result()
        self.id = "ip_challenge"  # Added id attribute
        self.completed=True

    def initialize_screen(self):
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('IP Address Challenge')
        return screen

    def set_font(self, font_name, fontsize):
        return pygame.font.Font(font_name, fontsize)
    
    def is_completed(self):
        return self.completed

    def get_challenge_instructions(self):
        instruction_text = [
            "Instructions:",
            "1. You need to create a function to scan ports on the IP address.",
            "2. The target IP address is 10.0.0.1.",
            "3. Your function should scan common ports and return a list of open ports.",
            "4. Click 'RUN' when you are done to test your changes."
        ]
        return instruction_text

    def render_editor_surface(self):
        editor_rect = pygame.Rect(self.screen_width // 2, 0, self.screen_width // 2, self.screen_height)
        return editor_rect

    def render_text_to_surface(self, surface, text, position, font, color):
        lines = text.split('\n')
        y_offset = 0
        for line in lines:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (position[0], position[1] + y_offset))
            y_offset += text_surface.get_height() + 5

    def validate_user_code(self, user_input):
        try:
            logger.info(f"Validating user code: {user_input}")
            local_vars = {}
            exec(user_input, globals(), local_vars)
            result = local_vars["scan_ports"](self.target_ip)
            if result == self.expected_result:
                logger.info("User code passed!")
                return True
            else:
                logger.info(f"User code failed. Expected result: {self.expected_result}, Got: {result}")
                return False
        except Exception as e:
            logger.error(f"An error occurred with your code: {e}")
            return False

    def is_run_code_button_pressed(self, run_button):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            if run_button.collidepoint(mouse_pos):
                return True
        return False

    def render_run_button(self):
        button = pygame.Rect(30, self.screen_height - 60, 75, 30)
        pygame.draw.rect(self.screen, self.BLACK, button)
        self.render_text_to_surface(self.screen, "RUN", [button.x + 25, button.y + 10], self.font, self.GRAY)
        return button

    def get_expected_result(self):
        # Example expected result, adjust as needed
        return "\n".join([f"Port {port}: Open" for port in [22, 80, 443]])

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.completed=True
                elif self.is_run_code_button_pressed(self.run_button):
                    if self.validate_user_code(self.users_code):
                        logger.info("Challenge Passed!")
                        self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.users_code += '\n' + self.tab
                    elif event.key == pygame.K_TAB:
                        self.users_code += self.tab
                    elif event.key == pygame.K_BACKSPACE:
                        self.users_code = self.users_code[:-1]
                    else:
                        self.users_code += event.unicode
            self.screen.fill(self.WHITE)
            self.render_text_to_surface(self.screen, '\n'.join(self.instruction_text), (20, 20), self.font, self.BLACK)
            self.render_run_button()
            pygame.draw.rect(self.screen, self.GRAY, self.editor_rect)
            self.render_text_to_surface(self.screen, self.users_code, (self.editor_rect.x + 10, 20), self.font, self.BLACK)
            pygame.display.flip()

if __name__ == '__main__':
    # Configure Loguru to output logs to a file and the console
    logger.add("ip_challenge.log", rotation="1 MB", level="INFO")
    logger.add(sys.stdout, level="INFO")

    challenge = IPChallenge()
    challenge.run()
