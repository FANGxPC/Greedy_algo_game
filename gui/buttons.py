import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
    
    def draw(self, surface):
        pass
        
    
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def click(self):
        if self.action:
            self.action()