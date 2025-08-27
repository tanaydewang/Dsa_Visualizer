import pygame

class ArrayVisualizer:
    def __init__(self, x, y, max_size=10):
        self.x = x
        self.y = y
        self.max_size = max_size
        self.array = []
        self.box_size = 70
        self.spacing = 10
        self.font = pygame.font.Font(None, 40)
        self.index_font = pygame.font.Font(None, 30)
        self.colors = {
            "default": (180, 180, 180),
            "highlight": (100, 200, 255),
            "found": (100, 255, 100),
            "delete": (255, 100, 100),
            "checking": (255, 255, 100)
        }
    
    def populate_random(self, count):
        import random
        self.array = [{"value": random.randint(10, 99), "color": self.colors["default"]} for _ in range(count)]

    def insert(self, value, index):
        if len(self.array) >= self.max_size or not (0 <= index <= len(self.array)):
            print("Invalid index or array full.")
            return

        # Make space for the new element
        self.array.append(None) 
        
        # Shift elements to the right
        for i in range(len(self.array) - 1, index, -1):
            self.array[i-1]["color"] = self.colors["highlight"]
            yield
            self.array[i] = self.array[i-1]
            self.array[i-1] = None
            self.array[i]["color"] = self.colors["default"]
            yield

        # Insert the new element
        self.array[index] = {"value": value, "color": self.colors["found"]}
        yield
        self.array[index]["color"] = self.colors["default"]
        yield

    def delete(self, index):
        if not (0 <= index < len(self.array)):
            print("Invalid index.")
            return

        self.array[index]["color"] = self.colors["delete"]
        yield
        self.array.pop(index)
        yield
    
    def search(self, value):
        found_idx = -1
        for i in range(len(self.array)):
            self.array[i]["color"] = self.colors["checking"]
            yield
            if self.array[i]["value"] == value:
                found_idx = i
                break
            self.array[i]["color"] = self.colors["default"]

        if found_idx != -1:
            self.array[found_idx]["color"] = self.colors["found"]
        yield


    def draw(self, screen):
        for i, item in enumerate(self.array):
            if item is None:
                continue
            
            box_rect = pygame.Rect(self.x + i * (self.box_size + self.spacing), self.y, self.box_size, self.box_size)
            
            # Draw box and value
            pygame.draw.rect(screen, item["color"], box_rect, border_radius=5)
            pygame.draw.rect(screen, (255,255,255), box_rect, 2, border_radius=5)
            text_surf = self.font.render(str(item["value"]), True, (0, 0, 0))
            screen.blit(text_surf, text_surf.get_rect(center=box_rect.center))

            # Draw index
            index_surf = self.index_font.render(str(i), True, (200, 200, 200))
            screen.blit(index_surf, index_surf.get_rect(center=(box_rect.centerx, box_rect.bottom + 20)))