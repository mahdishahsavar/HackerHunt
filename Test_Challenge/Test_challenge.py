import pygame

class SyntaxChallenge:
    def __init__(self):
        self.id = "syntax_challenge"
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.screen = self.initialize_screen()
        self.font = pygame.font.Font(None, 20)
        self.instruction_text = self.get_challenge_instructions()
        self.editor_rect = pygame.Rect(self.screen_width // 2, 0, self.screen_width // 2, self.screen_height)
        self.running = True
        self.users_code = ""
        self.run_button = self.render_run_button()

    def initialize_screen(self):
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Syntax Challenge')
        return screen

    def get_challenge_instructions(self):
        instruction_text = [
            "Challenge Instructions:",
            "Identify the correct syntax for a for-loop in Python.",
            "Write your answer below and click RUN to submit."
        ]
        return instruction_text

    def render_text_to_surface(self, surface, text, position, font, color):
        lines = text.split('\n')
        y_offset = 0
        for line in lines:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (position[0], position[1] + y_offset))
            y_offset += text_surface.get_height() + 5

    def validate_user_code(self):
        # Here, you can define correct answers or use a simpler validation
        correct_answers = ["for i in range(x):", "for element in iterable:"]
        return self.users_code.strip() in correct_answers

    def is_run_code_button_pressed(self, run_button):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] and run_button.collidepoint(mouse_pos):
            return True
        return False

    def render_run_button(self):
        button = pygame.Rect(30, self.screen_height - 60, 75, 30)
        pygame.draw.rect(self.screen, self.BLACK, button)
        self.render_text_to_surface(self.screen, "RUN", [button.x + 25, button.y + 5], self.font, self.WHITE)
        return button

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.is_run_code_button_pressed(self.run_button):
                    if self.validate_user_code():
                        print("Correct syntax!")
                        self.running = False
                    else:
                        print("Incorrect syntax, please try again.")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.users_code += '\n'
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
    challenge = SyntaxChallenge()
    challenge.run()
