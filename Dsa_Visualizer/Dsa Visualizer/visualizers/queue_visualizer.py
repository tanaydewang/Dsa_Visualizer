import pygame

class QueueVisualizer:
    def __init__(self, x, y, max_size=5):
        self.x = x
        self.y = y
        self.max_size = max_size
        self.queue = [None] * max_size
        self.front = 0
        self.rear = 0
        self.size = 0
        self.box_size = 80
        self.spacing = 10
        self.font = pygame.font.Font(None, 40)
        self.highlight_color = (255, 100, 100)
        self.default_color = (100, 200, 100)
        self.text_color = (255, 255, 255)

    def enqueue(self, value):
        if self.size >= self.max_size:
            print("Queue is full!")
            return

        self.queue[self.rear] = {"value": value, "color": self.highlight_color}
        yield

        self.queue[self.rear]["color"] = self.default_color
        self.rear = (self.rear + 1) % self.max_size
        self.size += 1
        yield

    def dequeue(self):
        if self.size == 0:
            print("Queue is empty!")
            return

        self.queue[self.front]["color"] = self.highlight_color
        yield

        self.queue[self.front] = None
        self.front = (self.front + 1) % self.max_size
        self.size -= 1
        yield

    def draw(self, screen):
        for i in range(self.max_size):
            box_rect = pygame.Rect(self.x + i * (self.box_size + self.spacing), self.y, self.box_size, self.box_size)
            item = self.queue[i]

            color = item["color"] if item else self.default_color
            pygame.draw.rect(screen, color, box_rect, border_radius=5)
            pygame.draw.rect(screen, (200, 200, 200), box_rect, 2, border_radius=5)

            if item:
                text_surf = self.font.render(str(item["value"]), True, (0, 0, 0))
                screen.blit(text_surf, text_surf.get_rect(center=box_rect.center))

        if self.size > 0:
            front_x = self.x + self.front * (self.box_size + self.spacing) + self.box_size / 2
            front_text = self.font.render("Front", True, self.text_color)
            screen.blit(front_text, (front_x - front_text.get_width() / 2, self.y + self.box_size + 10))

        if self.size < self.max_size:
            rear_x = self.x + self.rear * (self.box_size + self.spacing) + self.box_size / 2
            rear_text = self.font.render("Rear", True, self.text_color)
            screen.blit(rear_text, (rear_x - rear_text.get_width() / 2, self.y - 40))