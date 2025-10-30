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
        # color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
    #     pygame.draw.rect(surface, color, self.rect, border_radius=8)
    #     pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=8)
        
    #     font = pygame.font.SysFont('arial', 24)
    #     text_surf = font.render(self.text, True, BUTTON_TEXT_COLOR)
    #     text_rect = text_surf.get_rect(center=self.rect.center)
    #     surface.blit(text_surf, text_rect)
    
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def click(self):
        if self.action:
            self.action()