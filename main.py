import pygame, sys
from src.utils.settings import *
from src.game.level import Level
from src.utils.button import Button


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.import_assets()
        pygame.display.set_caption('Menu')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.buttons = {'start': Button(MENU_POSITIONS['start'], self.buttons_images['start']),
                        'exit': Button(MENU_POSITIONS['exit'], self.buttons_images['exit']),
                        'restart': Button(MENU_POSITIONS['restart'], self.buttons_images['restart'])}
        self.current_screen = 'start_menu'

        #sound
        main_sound_1 = pygame.mixer.Sound(r'..\Epoch-of-Change-Hero-s-Journey-rebuild\audio\background\menu.wav')
        main_sound_2 = pygame.mixer.Sound(r'..\Epoch-of-Change-Hero-s-Journey-rebuild\audio\background\level1.wav')
        main_sound_1.play(loops=-1)
        main_sound_2.play(loops=-1)

    def import_assets(self):
        self.buttons_images = {'start': None, 'exit': None, 'restart': None}

        for button_image in self.buttons_images.keys():
            full_path = r'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\menu\buttons/' + button_image + '.png'
            self.buttons_images[button_image] = pygame.image.load(full_path).convert_alpha()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            for name, button in self.buttons.items():
                if button.clicked:
                    if name == 'start' or name == 'restart':
                        self.level = Level()
                        self.current_screen = 'level'
                    elif name == 'exit':
                        pygame.quit()
                        sys.exit()
                button.enable()

            pygame.display.update()

    def run_start_menu(self):
        self.screen.fill(GREY_GREEN)
        self.buttons['start'].draw(self.screen)
        self.buttons['exit'].draw(self.screen)

    def run_level(self, dt):
        self.level.run(dt)

    def run_death_screen(self):
        self.buttons['restart'].draw(self.screen)

    def run_win_screen(self):
        self.screen.fill(GREY_GREEN)
        font = pygame.font.Font(None, 128)
        text = font.render("You Win!", True, WHITE)
        text_rect = text.get_rect(center=MENU_POSITIONS['win'])
        self.screen.blit(text, text_rect)
        self.buttons['start'].draw(self.screen)
        self.buttons['exit'].draw(self.screen)

    def run(self):
        while True:
            dt = self.clock.tick() / SECOND_TO_MILLISECOND

            if self.level.finish_player_death():
                self.current_screen = 'death'

            if self.level.finish_win():
                self.current_screen = 'win'

            if self.current_screen == 'start_menu':
                self.run_start_menu()
            elif self.current_screen == 'level':
                self.run_level(dt)
            elif self.current_screen == 'death':
                self.run_death_screen()
            elif self.current_screen == 'win':
                self.run_win_screen()

            self.handle_events()

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
