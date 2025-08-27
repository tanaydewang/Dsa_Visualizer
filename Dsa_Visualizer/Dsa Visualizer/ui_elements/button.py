import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, color_theme, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color_theme = color_theme # e.g., ('primary', 'hover')
        self.text_color = text_color
        self.is_hovered = False
        self.colors = {} # This will be updated by the theme

    def update_theme(self, theme_colors):
        """Updates the button's colors from the global theme."""
        self.colors['default'] = theme_colors[self.color_theme[0]]
        self.colors['hover'] = theme_colors[self.color_theme[1]]

    def draw(self, screen):
        current_color = self.colors['hover'] if self.is_hovered else self.colors['default']
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                return True
        return False