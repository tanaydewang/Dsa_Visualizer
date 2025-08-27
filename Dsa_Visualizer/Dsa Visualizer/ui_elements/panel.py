import pygame

class CodePanel:
    def __init__(self, x, y, width, height, code_lines, font, theme):
        self.rect = pygame.Rect(x, y, width, height)
        self.code_lines = code_lines
        self.font = font
        self.theme = theme
        self.padding = 10

    def draw(self, screen, highlighted_line):
        # Draw background panel
        pygame.draw.rect(screen, self.theme['primary'], self.rect, border_radius=10)
        
        for i, line in enumerate(self.code_lines):
            # Highlight the current line
            if i + 1 == highlighted_line:
                highlight_rect = pygame.Rect(self.rect.x, self.rect.y + self.padding + i * self.font.get_height(), self.rect.width, self.font.get_height())
                pygame.draw.rect(screen, self.theme['hover2'], highlight_rect)

            text_surface = self.font.render(line, True, self.theme['text'])
            screen.blit(text_surface, (self.rect.x + self.padding, self.rect.y + self.padding + i * self.font.get_height()))