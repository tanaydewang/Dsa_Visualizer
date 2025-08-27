import pygame
import math

class RBNode:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.color = "RED"
        self.x = 0
        self.y = 0

class RBTreeVisualizer:
    def __init__(self, screen_width):
        self.TNULL = RBNode(None)
        self.TNULL.color = "BLACK"
        self.root = self.TNULL
        self.screen_width = screen_width
        self.node_radius = 25
        self.level_gap = 80
        self.font = pygame.font.Font(None, 30)
        self.colors = {"RED": (255, 80, 80), "BLACK": (50, 50, 50)}

    def _left_rotate(self, x):
        y = x.right; x.right = y.left
        if y.left != self.TNULL: y.left.parent = x
        y.parent = x.parent
        if x.parent is None: self.root = y
        elif x == x.parent.left: x.parent.left = y
        else: x.parent.right = y
        y.left = x; x.parent = y

    def _right_rotate(self, x):
        y = x.left; x.left = y.right
        if y.right != self.TNULL: y.right.parent = x
        y.parent = x.parent
        if x.parent is None: self.root = y
        elif x == x.parent.right: x.parent.right = y
        else: x.parent.left = y
        y.right = x; x.parent = y

    def _fix_insert(self, k):
        while k != self.root and k.parent.color == "RED":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "RED":
                    u.color = "BLACK"; k.parent.color = "BLACK"; k.parent.parent.color = "RED"; k = k.parent.parent
                else:
                    if k == k.parent.left: k = k.parent; self._right_rotate(k)
                    k.parent.color = "BLACK"; k.parent.parent.color = "RED"; self._left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == "RED":
                    u.color = "BLACK"; k.parent.color = "BLACK"; k.parent.parent.color = "RED"; k = k.parent.parent
                else:
                    if k == k.parent.right: k = k.parent; self._left_rotate(k)
                    k.parent.color = "BLACK"; k.parent.parent.color = "RED"; self._right_rotate(k.parent.parent)
            if k == self.root: break
        self.root.color = "BLACK"

    def insert(self, value):
        node = RBNode(value); node.left = self.TNULL; node.right = self.TNULL
        y = None; x = self.root
        while x != self.TNULL:
            y = x
            if node.value < x.value: x = x.left
            else: x = x.right
        node.parent = y
        if y is None: self.root = node
        elif node.value < y.value: y.left = node
        else: y.right = node
        if node.parent is None: node.color = "BLACK"; yield; return
        if node.parent.parent is None: yield; return
        self._fix_insert(node); yield

    def _get_nodes_inorder(self, node, nodes):
        if node == self.TNULL: return
        self._get_nodes_inorder(node.left, nodes)
        nodes.append(node)
        self._get_nodes_inorder(node.right, nodes)
        return nodes
    
    def _draw_recursive(self, screen, node):
        if node == self.TNULL: return
        
        if node.left != self.TNULL:
            pygame.draw.line(screen, (255,255,255), (node.x, node.y), (node.left.x, node.left.y), 2)
            self._draw_recursive(screen, node.left)
        if node.right != self.TNULL:
            pygame.draw.line(screen, (255,255,255), (node.x, node.y), (node.right.x, node.right.y), 2)
            self._draw_recursive(screen, node.right)
        
        pygame.draw.circle(screen, self.colors[node.color], (node.x, node.y), self.node_radius)
        pygame.draw.circle(screen, (255,255,255), (node.x, node.y), self.node_radius, 2)
        text_surf = self.font.render(str(node.value), True, (255,255,255) if node.color=="BLACK" else (0,0,0))
        text_rect = text_surf.get_rect(center=(node.x, node.y))
        screen.blit(text_surf, text_rect)

    def draw(self, screen):
        if self.root == self.TNULL: return

        inorder_nodes = self._get_nodes_inorder(self.root, [])
        total_nodes = len(inorder_nodes)
        spacing = self.screen_width / (total_nodes + 1)
        x_coords = {node: i * spacing for i, node in enumerate(inorder_nodes, 1)}

        q = [(self.root, 0)]; visited = {self.root}
        while q:
            curr_node, depth = q.pop(0)
            if curr_node in x_coords: curr_node.x = x_coords[curr_node]
            curr_node.y = 70 + depth * self.level_gap
            
            if curr_node.left not in visited and curr_node.left != self.TNULL:
                q.append((curr_node.left, depth + 1)); visited.add(curr_node.left)
            if curr_node.right not in visited and curr_node.right != self.TNULL:
                q.append((curr_node.right, depth + 1)); visited.add(curr_node.right)

        self._draw_recursive(screen, self.root)