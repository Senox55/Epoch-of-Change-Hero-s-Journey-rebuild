import pygame, sys
from src.utils.settings import *
from src.game.level import Level
from src.utils.menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Menu')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.menu = Menu()
        self.in_screen = 'menu'

    def run(self):
        while True:
            dt = self.clock.tick() / SECOND_TO_MILLISECOND

            if self.in_screen == 'menu':
                self.menu.draw(self.screen)

            elif self.in_screen == 'level':
                self.level.run(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if self.menu.check_clicked_button() == 'start':
                    self.in_screen = 'level'

                if self.menu.check_clicked_button() == 'exit':
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
