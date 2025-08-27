import pygame
import random

class SearchingVisualizer:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.array = []
        self.font = pygame.font.Font(None, 40)
        self.pointers = {"low": 0, "high": 0, "mid": -1}
        self.message = ""
        self.colors = {
            "default": (180, 180, 180),
            "found": (100, 255, 100),
            "discarded": (80, 80, 80)
        }

    def generate_sorted_array(self, size=15, min_val=10, max_val=99):
        self.array = [{"value": random.randint(min_val, max_val), "color": self.colors["default"]} for _ in range(size)]
        self.array.sort(key=lambda x: x["value"])
        # Ensure no duplicates for simplicity
        unique_values = []
        seen = set()
        for item in self.array:
            if item["value"] not in seen:
                unique_values.append(item)
                seen.add(item["value"])
        self.array = unique_values
        self.message = ""


    def binary_search(self, target):
        # Reset colors
        for item in self.array:
            item["color"] = self.colors["default"]
        
        self.pointers["low"] = 0
        self.pointers["high"] = len(self.array) - 1
        self.message = f"Searching for {target}"
        yield

        while self.pointers["low"] <= self.pointers["high"]:
            self.pointers["mid"] = (self.pointers["low"] + self.pointers["high"]) // 2
            yield

            mid_val = self.array[self.pointers["mid"]]["value"]

            if mid_val == target:
                self.array[self.pointers["mid"]]["color"] = self.colors["found"]
                self.message = f"Found {target} at index {self.pointers['mid']}"
                yield
                return

            if mid_val < target:
                # Discard left half
                for i in range(self.pointers["low"], self.pointers["mid"] + 1):
                    self.array[i]["color"] = self.colors["discarded"]
                self.pointers["low"] = self.pointers["mid"] + 1
            else:
                # Discard right half
                for i in range(self.pointers["mid"], self.pointers["high"] + 1):
                    self.array[i]["color"] = self.colors["discarded"]
                self.pointers["high"] = self.pointers["mid"] - 1
            yield
        
        self.message = f"{target} not found in the array."
        yield

    def draw(self, screen):
        if not self.array: return

        box_width = self.width / len(self.array)
        
        for i, item in enumerate(self.array):
            box_height = self.height
            box_x = self.x + i * box_width
            box_y = self.y

            rect = pygame.Rect(box_x, box_y, box_width, box_height)
            pygame.draw.rect(screen, item["color"], rect)
            pygame.draw.rect(screen, (20,20,20), rect, 2)

            value_text = self.font.render(str(item["value"]), True, (0,0,0))
            screen.blit(value_text, value_text.get_rect(center=rect.center))

        # Draw pointers
        for name, index in self.pointers.items():
            if 0 <= index < len(self.array):
                box_x = self.x + index * box_width + box_width / 2
                text = self.font.render(name.upper(), True, (255, 255, 100))
                screen.blit(text, text.get_rect(center=(box_x, self.y - 30)))

        # Draw message
        if self.message:
            msg_text = self.font.render(self.message, True, (255,255,255))
            screen.blit(msg_text, msg_text.get_rect(center=(self.x + self.width/2, self.y - 80)))