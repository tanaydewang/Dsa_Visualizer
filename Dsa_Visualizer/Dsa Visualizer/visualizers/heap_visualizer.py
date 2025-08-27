import pygame
import math

class HeapNode:
    # ... (HeapNode class remains the same) ...
    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.x = 0
        self.y = 0
        self.color = (255, 165, 0) # Orange


class MinHeapVisualizer:
    # ... (init, _swap, insert, extract_min methods remain the same) ...
    def __init__(self, screen_width):
        self.heap = []
        self.screen_width = screen_width
        self.node_radius = 25
        self.level_gap = 80
        self.font = pygame.font.Font(None, 30)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.heap[i].index = i
        self.heap[j].index = j

    def insert(self, value):
        new_node = HeapNode(value, len(self.heap))
        new_node.color = (255, 0, 0)
        self.heap.append(new_node)
        yield
        current_idx = len(self.heap) - 1
        parent_idx = (current_idx - 1) // 2
        while current_idx > 0 and self.heap[current_idx].value < self.heap[parent_idx].value:
            self.heap[current_idx].color = (0, 255, 0)
            self.heap[parent_idx].color = (0, 255, 0)
            yield
            self._swap(current_idx, parent_idx)
            yield
            self.heap[current_idx].color = (255, 165, 0)
            self.heap[parent_idx].color = (255, 165, 0)
            current_idx = parent_idx
            parent_idx = (current_idx - 1) // 2
        self.heap[current_idx].color = (255, 165, 0)

    def extract_min(self):
        if not self.heap: return
        self.heap[0].color = (255, 0, 0)
        yield
        self._swap(0, len(self.heap) - 1)
        min_node = self.heap.pop()
        yield
        if not self.heap: return
        self.heap[0].color = (0, 255, 0)
        current_idx = 0
        while True:
            left_child_idx = 2 * current_idx + 1; right_child_idx = 2 * current_idx + 2
            smallest_idx = current_idx
            if left_child_idx < len(self.heap) and self.heap[left_child_idx].value < self.heap[smallest_idx].value:
                smallest_idx = left_child_idx
            if right_child_idx < len(self.heap) and self.heap[right_child_idx].value < self.heap[smallest_idx].value:
                smallest_idx = right_child_idx
            if smallest_idx == current_idx: break
            self.heap[current_idx].color = (0, 255, 0)
            self.heap[smallest_idx].color = (0, 255, 0)
            yield
            self._swap(current_idx, smallest_idx)
            yield
            self.heap[current_idx].color = (255, 165, 0)
            self.heap[smallest_idx].color = (255, 165, 0)
            current_idx = smallest_idx
        self.heap[current_idx].color = (255, 165, 0)

    def _update_positions(self):
        padding = 50  # Add some padding to the sides
        drawable_width = self.screen_width - (2 * padding)

        for i, node in enumerate(self.heap):
            if i == 0:
                depth = 0; index_in_level = 0
            else:
                depth = math.floor(math.log2(i + 1))
                index_in_level = i - (2**depth - 1)
            
            node.y = 70 + depth * self.level_gap
            
            total_nodes_in_level = 2**depth
            x_unit = drawable_width / total_nodes_in_level
            node.x = padding + (index_in_level * x_unit) + (x_unit / 2)
            
    def draw(self, screen):
        # ... (draw method remains the same) ...
        self._update_positions()
        
        for i, node in enumerate(self.heap):
            if i > 0:
                parent_idx = (i - 1) // 2
                parent_node = self.heap[parent_idx]
                pygame.draw.line(screen, (255,255,255), (node.x, node.y), (parent_node.x, parent_node.y), 2)

        for node in self.heap:
            pygame.draw.circle(screen, node.color, (node.x, node.y), self.node_radius)
            text_surf = self.font.render(str(node.value), True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=(node.x, node.y))
            screen.blit(text_surf, text_rect)