import pygame

class VisualNode:
    def __init__(self, value, x=0, y=0):
        self.value = value
        self.left = None
        self.right = None
        self.x = x
        self.y = y
        self.color = (200, 200, 200)

class BSTVisualizer:
    def __init__(self, screen_width):
        self.root = None
        self.screen_width = screen_width
        self.node_radius = 25
        self.level_gap = 80

    def insert(self, value):
        if self.root is None:
            self.root = VisualNode(value)
            yield
            return

        current = self.root
        while True:
            current.color = (255, 0, 0)
            yield

            if value < current.value:
                if current.left is None:
                    current.left = VisualNode(value)
                    current.color = (200, 200, 200)
                    yield
                    break
                current.color = (200, 200, 200)
                current = current.left
            else:
                if current.right is None:
                    current.right = VisualNode(value)
                    current.color = (200, 200, 200)
                    yield
                    break
                current.color = (200, 200, 200)
                current = current.right

    def _get_nodes_inorder(self, node, nodes):
        if node is None:
            return
        self._get_nodes_inorder(node.left, nodes)
        nodes.append(node)
        self._get_nodes_inorder(node.right, nodes)
        return nodes

    def _draw_recursive(self, screen, node, font):
        if node is None:
            return
        
        # Draw edges first
        if node.left:
            pygame.draw.line(screen, (255, 255, 255), (node.x, node.y), (node.left.x, node.left.y), 2)
            self._draw_recursive(screen, node.left, font)
        if node.right:
            pygame.draw.line(screen, (255, 255, 255), (node.x, node.y), (node.right.x, node.right.y), 2)
            self._draw_recursive(screen, node.right, font)

        # Draw node circle and text
        pygame.draw.circle(screen, node.color, (node.x, node.y), self.node_radius)
        text_surf = font.render(str(node.value), True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(node.x, node.y))
        screen.blit(text_surf, text_rect)

    def draw(self, screen, font):
        if not self.root:
            return
        
        # Step 1: Get nodes in horizontal order
        inorder_nodes = self._get_nodes_inorder(self.root, [])
        
        # Step 2: Calculate optimal spacing
        total_nodes = len(inorder_nodes)
        spacing = self.screen_width / (total_nodes + 1)
        
        # Step 3: Assign final x and y coordinates
        x_coords = {node: i * spacing for i, node in enumerate(inorder_nodes, 1)}
        
        q = [(self.root, 0)] # Queue for level-order traversal to set y-coords
        visited = {self.root}
        
        while q:
            curr_node, depth = q.pop(0)
            curr_node.x = x_coords[curr_node]
            curr_node.y = 70 + depth * self.level_gap
            
            if curr_node.left and curr_node.left not in visited:
                q.append((curr_node.left, depth + 1))
                visited.add(curr_node.left)
            if curr_node.right and curr_node.right not in visited:
                q.append((curr_node.right, depth + 1))
                visited.add(curr_node.right)
                
        # Step 4: Draw the tree
        self._draw_recursive(screen, self.root, font)