import pygame

class StackVisualizer:
    def __init__(self, x, y, max_size=7):
        self.x = x
        self.y = y
        self.max_size = max_size
        self.stack = []  # A simple list to act as our stack
        self.box_width = 120
        self.box_height = 50
        self.spacing = 10
        self.font = pygame.font.Font(None, 40)
        self.highlight_color = (255, 100, 100)
        self.default_color = (135, 206, 235)  # Sky blue
        self.text_color = (255, 255, 255)

    def push(self, value):
        if len(self.stack) >= self.max_size:
            print("Stack is full!")
            return

        # Add a new item with a highlight color
        self.stack.append({"value": value, "color": self.highlight_color})
        yield

        # Reset its color to default
        self.stack[-1]["color"] = self.default_color
        yield

    def pop(self):
        if not self.stack:
            print("Stack is empty!")
            return

        # Highlight the top item
        self.stack[-1]["color"] = self.highlight_color
        yield

        # Remove the item
        self.stack.pop()
        yield

    def draw(self, screen):
        # Draw from bottom to top
        for i, item in enumerate(self.stack):
            # The y-position depends on the index, with index 0 at the bottom
            box_y = self.y - i * (self.box_height + self.spacing)
            box_rect = pygame.Rect(self.x, box_y, self.box_width, self.box_height)

            # Draw the box
            pygame.draw.rect(screen, item["color"], box_rect, border_radius=5)
            pygame.draw.rect(screen, (200, 200, 200), box_rect, 2, border_radius=5)

            # Draw the value inside the box
            text_surf = self.font.render(str(item["value"]), True, (0, 0, 0))
            screen.blit(text_surf, text_surf.get_rect(center=box_rect.center))

        # Draw a "Top" pointer
        if self.stack:
            top_y = self.y - (len(self.stack) - 1) * (self.box_height + self.spacing) + (self.box_height / 2)
            top_x = self.x + self.box_width + 20
            top_text = self.font.render("<- Top", True, self.text_color)
            screen.blit(top_text, top_text.get_rect(midleft=(top_x, top_y)))