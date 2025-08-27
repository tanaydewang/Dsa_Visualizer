import pygame

class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = {}  # Pointers to child nodes
        self.is_end_of_word = False
        self.x = 0
        self.y = 0
        self.color = (200, 200, 200) # Default node color

class TrieVisualizer:
    def __init__(self, screen_width):
        self.root = TrieNode("*") # Root node doesn't hold a character
        self.screen_width = screen_width
        self.node_radius = 25
        self.level_gap = 90
        self.sibling_gap = 60
        self.font = pygame.font.Font(None, 30)
        self.colors = {"default": (200, 200, 200), "traversal": (255, 255, 100), "end": (100, 255, 100)}

    def insert(self, word):
        current = self.root
        for char in word:
            current.color = self.colors["traversal"]
            yield f"Current node: '{current.char}'"

            if char not in current.children:
                current.children[char] = TrieNode(char)
            
            current.color = self.colors["default"]
            current = current.children[char]
        
        current.color = self.colors["end"]
        current.is_end_of_word = True
        yield f"Marking '{current.char}' as end of word."
        yield "Finished insertion."


    def search(self, word):
        current = self.root
        for char in word:
            current.color = self.colors["traversal"]
            yield f"Searching for '{char}'"

            if char not in current.children:
                yield f"Character '{char}' not found. Word does not exist."
                # Reset all colors
                q = [self.root]; visited = {self.root}
                while q:
                    node = q.pop(0)
                    node.color = self.colors["default"]
                    for child in node.children.values():
                        if child not in visited: q.append(child); visited.add(child)
                return
            
            current.color = self.colors["default"]
            current = current.children[char]

        # Check if the last node is the end of a word
        if current.is_end_of_word:
            current.color = self.colors["end"]
            yield f"Word '{word}' found!"
        else:
            current.color = self.colors["traversal"]
            yield f"Prefix '{word}' exists, but it's not a complete word."


    def _assign_positions(self, node, depth, x_offset):
        # A simple recursive positioning logic
        node.y = 70 + depth * self.level_gap
        
        children_nodes = list(node.children.values())
        children_width = sum(self._get_subtree_width(child) for child in children_nodes)
        
        current_x = x_offset
        if children_width > 0:
             # Center parent over children
            first_child_pos = self._assign_positions(children_nodes[0], depth + 1, current_x)
            last_child_pos = first_child_pos
            for i in range(1, len(children_nodes)):
                 last_child_pos = self._assign_positions(children_nodes[i], depth + 1, last_child_pos + self._get_subtree_width(children_nodes[i-1]))
            node.x = (first_child_pos + last_child_pos) / 2
            return last_child_pos
        else:
            node.x = x_offset + self.sibling_gap / 2
            return x_offset + self.sibling_gap
            
    def _get_subtree_width(self, node):
        if not node.children:
            return self.sibling_gap
        width = 0
        for child in node.children.values():
            width += self._get_subtree_width(child)
        return width

    def _draw_recursive(self, screen, node):
        if node is None: return

        # Draw edges to children
        for child in node.children.values():
            pygame.draw.line(screen, (255,255,255), (node.x, node.y), (child.x, child.y), 2)
            self._draw_recursive(screen, child)
        
        # Draw node circle
        pygame.draw.circle(screen, node.color, (node.x, node.y), self.node_radius)
        # Highlight if it's the end of a word
        if node.is_end_of_word:
            pygame.draw.circle(screen, (255, 255, 255), (node.x, node.y), self.node_radius, 3)
        
        # Draw character
        text_surf = self.font.render(node.char, True, (0,0,0))
        screen.blit(text_surf, text_surf.get_rect(center=(node.x, node.y)))

    def draw(self, screen):
        self._assign_positions(self.root, 0, 0)
        self._draw_recursive(screen, self.root)