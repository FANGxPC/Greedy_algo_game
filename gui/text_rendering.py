import pygame

def draw_text(surface, text, x, y, font, color, centered=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    
    surface.blit(text_surface, text_rect)
    return text_rect