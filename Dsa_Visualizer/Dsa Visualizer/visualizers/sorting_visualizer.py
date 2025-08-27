import pygame
import random

class SortingVisualizer:
    # We store pseudocode for each algorithm in a dictionary
    PSEUDOCODE = {
        "selection_sort": [
            "1  procedure selectionSort( A )",
            "2     n = length(A)",
            "3     for i = 0 to n-1 do",
            "4        minIndex = i",
            "5        for j = i+1 to n do",
            "6           if A[j] < A[minIndex] then",
            "7              minIndex = j",
            "8           end if",
            "9        end for",
            "10       swap( A[i], A[minIndex] )",
            "11    end for",
            "12 end procedure"
        ],
        "bubble_sort": [
            "1  procedure bubbleSort( A )",
            "2     n = length(A)",
            "3     for i = 0 to n-1 do",
            "4        for j = 0 to n-i-2 do",
            "5           if A[j] > A[j+1] then",
            "6              swap( A[j], A[j+1] )",
            "7           end if",
            "8        end for",
            "9     end for",
            "10 end procedure"
        ],
        "insertion_sort": [
            "1  procedure insertionSort( A )",
            "2     n = length(A)",
            "3     for i = 1 to n-1 do",
            "4        key = A[i]",
            "5        j = i - 1",
            "6        while j >= 0 and key < A[j] do",
            "7           A[j+1] = A[j]",
            "8           j = j - 1",
            "9        end while",
            "10       A[j+1] = key",
            "11    end for",
            "12 end procedure"
        ]
    }

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.array = []
        self.font = pygame.font.Font(None, 30)
        self.colors = {"default": (180, 180, 180), "comparing": (255, 255, 100), "key": (255, 165, 0), "sorted": (100, 255, 100), "swapping": (255, 100, 100)}

    def generate_array(self, size=20, min_val=10, max_val=100):
        self.array = []
        bar_width = self.width / size
        for i in range(size):
            value = random.randint(min_val, max_val)
            self.array.append({"value": value, "color": self.colors["default"], "x": self.x + i * bar_width, "width": bar_width})

    def _animate_swap(self, idx1, idx2, line_num, steps=15):
        if idx1 == idx2: return
        pos1_start, pos2_start = self.array[idx1]['x'], self.array[idx2]['x']
        for i in range(steps + 1):
            t = i / steps
            self.array[idx1]['x'] = pos1_start + (pos2_start - pos1_start) * t
            self.array[idx2]['x'] = pos2_start + (pos1_start - pos2_start) * t
            yield {'line': line_num, 'msg': f"Swapping {self.array[idx1]['value']} and {self.array[idx2]['value']}"}
        self.array[idx1], self.array[idx2] = self.array[idx2], self.array[idx1]
        self.array[idx1]['x'], self.array[idx2]['x'] = pos1_start, pos2_start

    def selection_sort(self):
        yield {'line': 1, 'msg': "Starting Selection Sort"}
        n = len(self.array)
        yield {'line': 2, 'msg': f"n = {n}"}
        for i in range(n):
            yield {'line': 3, 'msg': f"Outer loop, i = {i}"}
            min_idx = i
            self.array[i]["color"] = self.colors["key"]
            yield {'line': 4, 'msg': f"minIndex = {i}"}
            for j in range(i + 1, n):
                yield {'line': 5, 'msg': f"Inner loop, j = {j}"}
                self.array[j]["color"] = self.colors["comparing"]
                yield {'line': 6, 'msg': f"Comparing {self.array[j]['value']} < {self.array[min_idx]['value']}"}
                if self.array[j]["value"] < self.array[min_idx]["value"]:
                    self.array[min_idx]["color"] = self.colors["default"] if min_idx != i else self.colors["key"]
                    min_idx = j
                    self.array[min_idx]["color"] = self.colors["key"]
                    yield {'line': 7, 'msg': f"New minIndex = {j}"}
                else: self.array[j]["color"] = self.colors["default"]
            self.array[i]["color"] = self.colors["swapping"]; self.array[min_idx]["color"] = self.colors["swapping"]
            yield from self._animate_swap(i, min_idx, 10)
            self.array[i]["color"] = self.colors["sorted"]
            if i != min_idx: self.array[min_idx]["color"] = self.colors["default"]
        yield {'line': 12, 'msg': "Array is sorted!"}

    def bubble_sort(self):
        yield {'line': 1, 'msg': "Starting Bubble Sort"}
        n = len(self.array)
        yield {'line': 2, 'msg': f"n = {n}"}
        for i in range(n - 1):
            yield {'line': 3, 'msg': f"Pass {i + 1}"}
            for j in range(0, n - i - 1):
                yield {'line': 4, 'msg': f"Comparing index {j} and {j+1}"}
                self.array[j]["color"] = self.colors["comparing"]; self.array[j + 1]["color"] = self.colors["comparing"]
                yield {'line': 5, 'msg': f"Is {self.array[j]['value']} > {self.array[j+1]['value']}?"}
                if self.array[j]["value"] > self.array[j + 1]["value"]:
                    self.array[j]["color"] = self.colors["swapping"]; self.array[j + 1]["color"] = self.colors["swapping"]
                    yield from self._animate_swap(j, j + 1, 6)
                self.array[j]["color"] = self.colors["default"]; self.array[j + 1]["color"] = self.colors["default"]
            self.array[n - i - 1]["color"] = self.colors["sorted"]
        self.array[0]["color"] = self.colors["sorted"]
        yield {'line': 10, 'msg': "Array is sorted!"}

    def insertion_sort(self):
        yield {'line': 1, 'msg': "Starting Insertion Sort"}
        n = len(self.array)
        yield {'line': 2, 'msg': f"n = {n}"}
        for i in range(1, n):
            yield {'line': 3, 'msg': f"Outer loop, i = {i}"}
            key_item = self.array[i]; key_item_val = key_item['value']
            key_item["color"] = self.colors["key"]
            yield {'line': 4, 'msg': f"Key = {key_item_val}"}
            j = i - 1
            yield {'line': 5, 'msg': f"j = {j}"}
            while j >= 0 and key_item_val < self.array[j]["value"]:
                yield {'line': 6, 'msg': f"Comparing key {key_item_val} with {self.array[j]['value']}"}
                self.array[j]["color"] = self.colors["comparing"]
                yield {'line': 7, 'msg': f"Shifting {self.array[j]['value']} to the right"}
                self.array[j+1], self.array[j+1]['x'] = self.array[j], self.array[j]['x']
                self.array[j+1]["color"] = self.colors["default"]
                j -= 1
                yield {'line': 8, 'msg': f"j = {j}"}
            self.array[j + 1], self.array[j+1]['x'] = key_item, self.x + (j+1) * key_item['width']
            yield {'line': 10, 'msg': f"Inserting key {key_item_val} at index {j+1}"}
            for k in range(i + 1): self.array[k]["color"] = self.colors["sorted"]
            yield
        yield {'line': 12, 'msg': "Array is sorted!"}

    def draw(self, screen):
        if not self.array: return
        max_val = max(item["value"] for item in self.array) if self.array else 1
        for item in self.array:
            bar_height = (item["value"] / max_val) * self.height
            bar_x = item['x']
            bar_y = self.y + self.height - bar_height
            rect = pygame.Rect(bar_x, bar_y, item['width'], bar_height)
            pygame.draw.rect(screen, item["color"], rect)
            pygame.draw.rect(screen, (20,20,20), rect, 2)
            if item['width'] > 30:
                value_text = self.font.render(str(item["value"]), True, (0,0,0))
                screen.blit(value_text, value_text.get_rect(center=rect.center))