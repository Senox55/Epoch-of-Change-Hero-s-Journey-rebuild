import pygame


class Button:
    def __init__(self, pos, image):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.clicked = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

    def enable(self):
        self.clicked = False
