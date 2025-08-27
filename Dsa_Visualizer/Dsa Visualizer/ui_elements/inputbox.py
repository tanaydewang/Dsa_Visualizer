import pygame

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = ''
        self.font = font
        self.txt_surface = self.font.render('', True, (255, 255, 255))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    value = self.text
                    # self.text = '' # Optional: clear after enter
                    return value
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (255, 255, 255))
        return None

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)