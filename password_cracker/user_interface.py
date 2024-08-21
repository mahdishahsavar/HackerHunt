import pygame
from loguru import logger
import random

class PasswordCracker:
    def __init__(self):
        self.id = "password_cracker"
        self.completed = False
        pygame.init()
        self.screen_width = 1000
        self.screen_height = 800
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.PASSWORDS = ["password", "for", "game", "team-24", "techwise"]
        self.screen = self.initialize_screen()
        self.font = self.set_font(None, 20)
        self.instruction_text = self.get_challenge_instructions(self.PASSWORDS)
        self.editor_rect = self.render_editor_surface()
        self.running = True
        self.tab = ' ' * 5
        self.users_code = "def crack_password(passwords): \n" + self.tab
        self.run_button = self.render_run_button()
        self.master_password = self.create_password()


    def initialize_screen(self):
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Password Cracker')
        return screen

    def set_font(self, fontName, fontsize):
        return pygame.font.Font(fontName, fontsize)

    def get_challenge_instructions(self, possible_passwords):
        instruction_text = [
            "Instructions:",
            "1. Our passwords have been compromised and we need you to help us \ncrack the password. From our records, it shows that the password \nwas mashed up.",
            f"2. The password can only be made from a single word, combination of \nwords from this list {possible_passwords}",
            "3.CLick run when you are done to test your changes"
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
            return self.master_password == local_vars["crack_password"](self.PASSWORDS)
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

    def create_password(self):
        master_password = ""
        context = ''.join(word for word in self.PASSWORDS)
        accessed_indices = []
        while len(master_password) < 8:
            index = random.randint(0, 9)
            if index not in accessed_indices:
                accessed_indices.append(index)
                master_password += context[index]
        return master_password

    def is_completed(self):
        return self.completed
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.is_run_code_button_pressed(self.run_button):
                    if self.validate_user_code(self.users_code):
                        logger.info(f"Passed!")
                        self.completed = True
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
    cracker = PasswordCracker()
    cracker.run()