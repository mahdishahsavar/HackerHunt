from PIL import Image
from stegano import lsb
import random
import pygame
from loguru import logger

MESSAGES = ['some hacker message', 'another hacker message']


class Steganography:
    def __init__(self):
        pygame.init()
        self.id = "steganography"
        self.tab = '    '
        self.image = Image.open('resources/hacker.gif').convert('RGB')
        self.embedded_message = MESSAGES[random.randint(0, len(MESSAGES)-1)]
        self.embedded_image = self._embed_message(self.embedded_message).convert('RGB')
        self.users_code = f"def steganography(photo):\n{self.tab}"
        self.screen_width = 1000
        self.screen_height = 800
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.screen = self._initialize_screen()
        self.font = self._set_font(None, 20)
        self.instruction_text = self._get_challenge_instructions()
        self.editor_rect = self._render_editor_surface()
        self.running = True
        self.run_button = self._render_run_button()

    def _embed_message(self, message):
        secret_image = lsb.hide("resources/hacker.gif", message)
        secret_image.save("resources/embedded_hacker.gif")
        return secret_image

    def _validate_user_code(self, user_code):
        try:
            local_vars = {}
            exec(user_code, globals(), local_vars)
            return self.embedded_message == local_vars['steganography'](self.embedded_image)
        except Exception as e:
            return False

    def _initialize_screen(self):
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Password Cracker')
        return screen

    def _set_font(self, fontName, fontsize):
        return pygame.font.Font(fontName, fontsize)

    def _get_challenge_instructions(self):
        instruction_text = [
            "Instructions:"
        ]
        return instruction_text

    def _render_editor_surface(self):
        editor_rect = pygame.Rect(self.screen_width // 2, 0, self.screen_width // 2, self.screen_height)
        return editor_rect

    def _render_text_to_surface(self, surface, text, position, font, color):
        lines = text.split('\n')
        y_offset = 0
        for line in lines:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (position[0], position[1] + y_offset))
            y_offset += text_surface.get_height() + 5

    def _is_run_code_button_pressed(self, run_button):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            if run_button.collidepoint(mouse_pos):
                return True
        return False

    def _render_run_button(self):
        button = pygame.Rect(30, self.screen_height - 60, 75, 30)
        pygame.draw.rect(self.screen, self.BLACK, button)
        self._render_text_to_surface(self.screen, "RUN", [button.x + 25, button.y + 10], self.font, self.GRAY)
        return button

    def _display_photo(self):
        photo = pygame.image.load("resources/hacker.gif")
        photo_rect = photo.get_rect()
        img_rect = pygame.Rect(self.screen_width//2 - photo_rect.width, self.screen_height - photo_rect.height - 100, self.screen_width//2, photo_rect.height)
        self.screen.blit(photo, img_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self._is_run_code_button_pressed(self.run_button):
                    if self._validate_user_code(self.users_code):
                        logger.info(f"Passed!")
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
            self._render_text_to_surface(self.screen, '\n'.join(self.instruction_text), (20, 20), self.font, self.BLACK)
            self._render_run_button()
            pygame.draw.rect(self.screen, self.GRAY, self.editor_rect)
            self._render_text_to_surface(self.screen, self.users_code, (self.editor_rect.x + 10, 20), self.font, self.BLACK)
            self._display_photo()
            pygame.display.flip()


if __name__ == '__main__':
    chall = Steganography()
    chall.run()
