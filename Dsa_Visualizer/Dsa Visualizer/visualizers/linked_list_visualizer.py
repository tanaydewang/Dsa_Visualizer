import pygame

class LLNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.x = 0
        self.y = 0
        self.color = (137, 207, 240)  # Light Blue

class LinkedListVisualizer:
    def __init__(self, x, y):
        self.head = None
        self.start_x = x
        self.y = y
        self.node_width = 100
        self.node_height = 50
        self.spacing = 50
        self.font = pygame.font.Font(None, 35)

    def _update_positions(self):
        current = self.head
        x_pos = self.start_x
        while current:
            current.x = x_pos
            current.y = self.y
            x_pos += self.node_width + self.spacing
            current = current.next

    def insert_at_beginning(self, value):
        new_node = LLNode(value)
        new_node.color = (255, 100, 100) # Highlight
        new_node.next = self.head
        self.head = new_node
        yield

        new_node.color = (137, 207, 240) # Reset color
        yield

    def delete_value(self, value):
        if not self.head:
            return

        # Traverse and highlight
        current = self.head
        prev = None
        while current and current.value != value:
            current.color = (255, 255, 0) # Yellow for traversal
            yield
            current.color = (137, 207, 240)
            prev = current
            current = current.next

        # If found, highlight for deletion and update pointers
        if current:
            current.color = (255, 0, 0) # Red for delete
            yield

            if prev:
                prev.next = current.next
            else:
                self.head = current.next
            yield
        else: # Reset colors if not found
            temp = self.head
            while temp:
                temp.color = (137, 207, 240)
                temp = temp.next


    def draw(self, screen):
        self._update_positions()
        current = self.head
        
        # Draw Head pointer
        if current:
            head_text = self.font.render("Head", True, (255,255,255))
            screen.blit(head_text, (current.x + self.node_width/2 - head_text.get_width()/2, current.y - 40))

        while current:
            # Draw node rectangle
            rect = pygame.Rect(current.x, current.y, self.node_width, self.node_height)
            pygame.draw.rect(screen, current.color, rect, border_radius=10)
            pygame.draw.rect(screen, (255,255,255), rect, 2, border_radius=10)

            # Draw value
            value_text = self.font.render(str(current.value), True, (0,0,0))
            screen.blit(value_text, value_text.get_rect(center=(current.x + self.node_width/2, current.y + self.node_height/2)))

            # Draw pointer to next node
            if current.next:
                start_pos = (current.x + self.node_width, current.y + self.node_height / 2)
                end_pos = (current.next.x, current.next.y + self.node_height / 2)
                pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 2)
                # Arrowhead
                pygame.draw.polygon(screen, (255, 255, 255), [end_pos, (end_pos[0] - 10, end_pos[1] - 5), (end_pos[0] - 10, end_pos[1] + 5)])

            current = current.next