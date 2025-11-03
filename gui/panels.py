import pygame
import os
from config import *

class BagPanel:
    def __init__(self, x, y, width, height, player_name, player_type="human", player_index=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.player_name = player_name
        self.player_type = player_type
        self.player_index = player_index
        self.items = []
        self.total_weight = 0
        self.capacity = 25
        self.score = 0
        self.score_rect = None
        self.item_images = {}
        self.animation_frame = 0
        self.animation_timer = 0
        
        self.icons = {
            "human": [
                pygame.image.load(os.path.join("assets", "images", "ui", "avatar11.png")).convert_alpha(),
                pygame.image.load(os.path.join("assets", "images", "ui", "avatar12.png")).convert_alpha()
            ],
            "ai": [
                pygame.image.load(os.path.join("assets", "images", "ui", "avatar21.png")).convert_alpha(),
                pygame.image.load(os.path.join("assets", "images", "ui", "avatar22.png")).convert_alpha()
            ]
        }
        
        icon_size = (32, 32)
        for player_type in self.icons:
            for i in range(len(self.icons[player_type])):
                self.icons[player_type][i] = pygame.transform.scale(self.icons[player_type][i], icon_size)
        
        self.player_colors = [
            (0, 150, 255),
            (255, 100, 0),
            (0, 200, 100),
            (200, 50, 200)
        ]
        
        self.progress_dark = (30, 30, 30)
        self.progress_medium = (60, 60, 60)
        self.progress_light = (90, 90, 90)
        self.progress_fill_dark = (0, 100, 0)
        self.progress_fill_light = (0, 220, 0)
        self.progress_bg = (20, 20, 20)
        
        self.slot_size = int(min(width, height) * 0.08)
        self.text_color = (255, 255, 255)
    
    def draw(self, surface):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_frame = 1 - self.animation_frame
        
        self.draw_pixel_art_panel(surface, self.rect)
        
        font_size = int(self.rect.height * 0.03)
        font = pygame.font.SysFont('Arial', font_size, bold=False)
        
        bar_width = 70
        bar_height = 620
        progress_y = self.rect.y + 20
        progress_x = self.rect.x + 20
        self.draw_pixel_art_progress_bar(surface, progress_x, progress_y, font)
        
        icon_size = int(bar_width * 1.2)
        icon_x = progress_x + (bar_width - icon_size) // 2
        icon_y = progress_y - icon_size - 5
        
        current_icon = self.icons[self.player_type][self.animation_frame]
        scaled_icon = pygame.transform.scale(current_icon, (icon_size, icon_size))
        surface.blit(scaled_icon, (icon_x, icon_y))
        
        name_font_size = int(icon_size * 0.1)
        name_font = pygame.font.SysFont('Arial', name_font_size, bold=True)
        
        text_surf = font.render(self.player_name, True, self.text_color)
        text_rect = text_surf.get_rect(
            midtop=(progress_x + bar_width // 2, 
                   icon_y + icon_size + 5)
        )
        surface.blit(text_surf, text_rect)
        
        score_text = f"Score: {self.score:.2f}"
        capacity_text = f"Bag: {(int)(self.total_weight)}/{self.capacity} kg"
        
        small_font_size = int(font_size * 0.5)
        small_font = pygame.font.SysFont('Arial', small_font_size)
        
        info_start_y = progress_y + bar_height + 15
        
        score_surf = small_font.render(score_text, True, self.text_color)
        score_rect = score_surf.get_rect(
            midtop=(self.rect.x + 20 + bar_width // 2, info_start_y)
        )
        self.score_rect = score_rect
        surface.blit(score_surf, score_rect)
        
        capacity_surf = small_font.render(capacity_text, True, self.text_color)
        capacity_rect = capacity_surf.get_rect(
            midtop=(self.rect.x + 20 + bar_width // 2, score_rect.bottom + 5)
        )
        surface.blit(capacity_surf, capacity_rect)
        

    def draw_pixel_art_panel(self, surface, rect):
        pixel_size = 4
        width_pixels = rect.width // pixel_size
        height_pixels = rect.height // pixel_size
        
        for py in range(height_pixels):
            for px in range(width_pixels):
                pixel_x = rect.x + px * pixel_size
                pixel_y = rect.y + py * pixel_size
                
                if px == 0 or px == width_pixels - 1 or py == 0 or py == height_pixels - 1:
                    color = (255, 255, 255)
                else:
                    color = (200, 200, 200)
                

    def draw_pixel_art_progress_bar(self, surface, x_pos, y_pos, font):
        bar_width = 70
        bar_height = 620
        pixel_size = 4
        
        width_pixels = bar_width // pixel_size
        height_pixels = bar_height // pixel_size
        
        for py in range(height_pixels):
            for px in range(width_pixels):
                pixel_x = x_pos + px * pixel_size
                pixel_y = y_pos + py * pixel_size
                
                if px == 0 or px == width_pixels - 1 or py == 0 or py == height_pixels - 1:
                    color = self.progress_dark
                elif px == 1 or px == width_pixels - 2 or py == 1 or py == height_pixels - 2:
                    color = self.progress_medium
                elif px == 2 or px == width_pixels - 3 or py == 2 or py == height_pixels - 3:
                    color = self.progress_light
                else:
                    color = self.progress_bg
                
                pygame.draw.rect(surface, color, (pixel_x, pixel_y, pixel_size, pixel_size))
        
        if self.capacity > 0 and self.total_weight > 0:
            fill_ratio = min(1.0, self.total_weight / self.capacity)
            fill_height_pixels = max(1, int(height_pixels * fill_ratio))
            
            fill_start_x = x_pos + 3 * pixel_size
            fill_start_y = y_pos + bar_height - (fill_height_pixels * pixel_size)
            
            for py in range(fill_height_pixels):
                for px in range(width_pixels - 6):
                    pixel_x = fill_start_x + px * pixel_size
                    pixel_y = fill_start_y + py * pixel_size
                    
                    if (px + py) % 4 == 0:
                        color = self.progress_fill_light
                    else:
                        color = self.progress_fill_dark
                    
                    if (px * py) % 7 == 0:
                        color = (min(255, color[0] + 10), min(255, color[1] + 10), min(255, color[2] + 10))
                    
                    pygame.draw.rect(surface, color, (pixel_x, pixel_y, pixel_size, pixel_size))
            
            top_cap_y = fill_start_y
            for px in range(width_pixels - 6):
                pixel_x = fill_start_x + px * pixel_size
                cap_color = (min(255, self.progress_fill_light[0] + 20), 
                           min(255, self.progress_fill_light[1] + 20), 
                           min(255, self.progress_fill_light[2] + 20))
                pygame.draw.rect(surface, cap_color, (pixel_x, top_cap_y, pixel_size, pixel_size))
        
        
        self.draw_pixel_corners(surface, x_pos, y_pos, bar_width, bar_height, pixel_size)

    def draw_pixel_corners(self, surface, x, y, width, height, pixel_size):
        corner_size = 3
        for i in range(corner_size):
            for j in range(corner_size):
                if i + j < corner_size:
                    color = self.progress_light if (i + j) % 2 == 0 else self.progress_medium
                    pygame.draw.rect(surface, color, (x + i * pixel_size, y + j * pixel_size, pixel_size, pixel_size))
                    color = self.progress_light if (i + j) % 2 == 0 else self.progress_medium
                    pygame.draw.rect(surface, color, (x + width - (i + 1) * pixel_size, y + j * pixel_size, pixel_size, pixel_size))
                    color = self.progress_dark if (i + j) % 2 == 0 else self.progress_medium
                    pygame.draw.rect(surface, color, (x + i * pixel_size, y + height - (j + 1) * pixel_size, pixel_size, pixel_size))
                    color = self.progress_dark if (i + j) % 2 == 0 else self.progress_medium
                    pygame.draw.rect(surface, color, (x + width - (i + 1) * pixel_size, y + height - (j + 1) * pixel_size, pixel_size, pixel_size))

    def draw_bag_items(self, surface, start_x, start_y):
        padding = 5
        slots_per_row = 5
        rows = 5
        
        available_width = self.rect.width - (start_x - self.rect.x) - padding
        available_height = self.rect.bottom - start_y - padding
        slot_size = min(self.slot_size, available_width // slots_per_row, available_height // rows - padding)
        
        for i in range(25):
            row = i // slots_per_row
            col = i % slots_per_row
            
            x = start_x + col * (slot_size + padding)
            y = start_y + row * (slot_size + padding)
            
            slot_rect = pygame.Rect(x, y, slot_size, slot_size)
            
            if i < len(self.items):
                self.draw_item(surface, slot_rect, self.items[i])
            else:
                pygame.draw.rect(surface, (50, 50, 50), slot_rect, 1)

    def draw_item(self, surface, slot_rect, item):
        if not item:
            return
            
        image_filename = item.get('image_filename')
        if not image_filename:
            pygame.draw.rect(surface, (100, 100, 100), slot_rect, border_radius=8)
            return

        try:
            base_num = ''.join(filter(str.isdigit, image_filename))
            if not base_num:
                base_num = '1'
                
            frame_prefix = 'i' if self.animation_frame == 0 else 'j'
            frame_filename = f"{frame_prefix}{base_num}.png"
            
            if frame_filename not in self.item_images:
                try:
                    image_path = os.path.join('assets','images', 'items', frame_filename)
                    if not os.path.exists(image_path):
                        image_path = os.path.join('assets', 'images', 'items', image_filename)
                    
                    item_image = pygame.image.load(image_path).convert_alpha()
                    self.item_images[frame_filename] = item_image
                except Exception as e:
                    print(f"Error loading {frame_filename}: {e}")
                    item_image = pygame.Surface((32, 32), pygame.SRCALPHA)
                    color = (100 + int(base_num) * 5, 100 + int(base_num) * 3, 200, 200)
                    pygame.draw.rect(item_image, color, (0, 0, 32, 32))
                    self.item_images[frame_filename] = item_image

            item_surface = pygame.Surface((slot_rect.width, slot_rect.height), pygame.SRCALPHA)
            
            if frame_filename in self.item_images:
                base_surface = pygame.Surface((slot_rect.width, slot_rect.height), pygame.SRCALPHA)
                
                scaled_img = pygame.transform.scale(
                    self.item_images[frame_filename],
                    (slot_rect.width, slot_rect.height)
                )
                
                mask = pygame.Surface((slot_rect.width, slot_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(mask, (255, 255, 255, 255), 
                              (0, 0, slot_rect.width, slot_rect.height), 
                              border_radius=8)
                
                scaled_img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                base_surface.blit(scaled_img, (0, 0))
                
                border_rect = pygame.Rect(0, 0, slot_rect.width, slot_rect.height)
                pygame.draw.rect(base_surface, (255, 215, 0, 255), 
                              border_rect, 2, border_radius=8)
                
                surface.blit(base_surface, slot_rect)
            
        except Exception as e:
            print(f"Error in draw_item: {e}")
            item_surface = pygame.Surface((slot_rect.width, slot_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(item_surface, (200, 200, 200, 200), 
                          (0, 0, slot_rect.width, slot_rect.height), 
                          border_radius=8)
            pygame.draw.rect(item_surface, (255, 215, 0, 255), 
                          (0, 0, slot_rect.width, slot_rect.height), 
                          2, border_radius=8)
            surface.blit(item_surface, slot_rect)
        
        thin_font = pygame.font.SysFont('arial', max(8, slot_rect.height // 8))
        weight = int(item.weight if hasattr(item, 'weight') else item.get('weight', 0))
        value = int(item.value if hasattr(item, 'value') else item.get('value', 0))
        
        weight_text = f"W:{weight}"
        weight_surf = thin_font.render(weight_text, True, (0, 0, 0))
        weight_rect = weight_surf.get_rect(topleft=(slot_rect.left + 1, slot_rect.top + 1))
        surface.blit(weight_surf, weight_rect)
        
        value_text = f"V:{value}"
        value_surf = thin_font.render(value_text, True, (0, 0, 0))
        value_rect = value_surf.get_rect(bottomright=(slot_rect.right - 1, slot_rect.bottom - 1))
        surface.blit(value_surf, value_rect)

    def get_score_position(self):
        if self.score_rect:
            return self.score_rect.center
        return (self.rect.centerx, self.rect.y + 50)
    
    def update_player_data(self, items, total_weight, capacity, score):
        self.items = items
        self.total_weight = total_weight
        self.capacity = capacity
        self.score = score

class ItemPanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.items = []
        self.item_rects = []
        self.item_images = {}
        self.text_color = (255, 255, 255)
        self.slot_size = int(min(width, height) * 0.18)
        self.animation_frame = 0
        self.animation_timer = 0
    
    def draw(self, surface):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_frame = 1 - self.animation_frame
            
        title_font_size = int(self.rect.height * 0.06)
        title_font = pygame.font.SysFont('arial', title_font_size, bold=True)
        
        text_surf = title_font.render("Available Items", True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.y + title_font_size))
        surface.blit(text_surf, text_rect)
        
        self.draw_items(surface)
    
    def draw_items(self, surface):
        self.item_rects = []
        padding = int(self.rect.width * 0.02)
        slots_per_row = 5
        start_y = self.rect.y + int(self.rect.height * 0.1)
        
        available_width = self.rect.width - (slots_per_row - 1) * padding
        slot_size = min(int(self.slot_size * 1.2), available_width // slots_per_row)
        
        for i, item in enumerate(self.items):
            if i >= 25: break
            row = i // slots_per_row
            col = i % slots_per_row
            x = self.rect.x + col * (slot_size + padding)
            y = start_y + row * (slot_size + padding)
            item_rect = pygame.Rect(x, y, slot_size, slot_size)
            self.item_rects.append(item_rect)
            self.draw_item(surface, item_rect, item)
    
    def draw_item(self, surface, item_rect, item):
        image_filename = item.get('image_filename')
        if not image_filename:
            pygame.draw.rect(surface, (100,100,100), item_rect, border_radius=8)
            return

        try:
            base_num = ''.join(filter(str.isdigit, image_filename))
            if not base_num:
                base_num = '1'
                
            frame_prefix = 'i' if self.animation_frame == 0 else 'j'
            frame_filename = f"{frame_prefix}{base_num}.png"
            
            if frame_filename not in self.item_images:
                try:
                    image_path = os.path.join('assets', 'images','items', frame_filename)
                    if not os.path.exists(image_path):
                        image_path = os.path.join('assets', 'images','items', image_filename)
                    
                    item_image = pygame.image.load(image_path).convert_alpha()
                    self.item_images[frame_filename] = item_image
                except Exception as e:
                    print(f"Error loading {frame_filename}: {e}")
                    item_image = pygame.Surface((32, 32), pygame.SRCALPHA)
                    color = (100 + int(base_num) * 5, 100 + int(base_num) * 3, 200, 200)
                    pygame.draw.rect(item_image, color, (0, 0, 32, 32))
                    self.item_images[frame_filename] = item_image

            item_surface = pygame.Surface((item_rect.width, item_rect.height), pygame.SRCALPHA)
            
            if frame_filename in self.item_images:
                scaled_img = pygame.transform.scale(
                    self.item_images[frame_filename],
                    (item_rect.width, item_rect.height)
                )
                mask = pygame.Surface((item_rect.width, item_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, item_rect.width, item_rect.height), 
                               border_radius=8)
                
                scaled_img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                item_surface.blit(scaled_img, (0, 0))
                
                border_rect = pygame.Rect(0, 0, item_rect.width, item_rect.height)
                pygame.draw.rect(item_surface, (255, 215, 0, 255), border_rect, 2, border_radius=8)
                
                surface.blit(item_surface, item_rect)
            
        except Exception as e:
            print(f"Error in draw_item: {e}")
            item_surface = pygame.Surface((item_rect.width, item_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(item_surface, (200, 200, 200, 200), 
                          (0, 0, item_rect.width, item_rect.height), 
                          border_radius=8)
            pygame.draw.rect(item_surface, (255, 215, 0, 255), 
                          (0, 0, item_rect.width, item_rect.height), 
                          2, border_radius=8)
            surface.blit(item_surface, item_rect)
        
        thin_font = pygame.font.SysFont('arial', max(8, item_rect.height // 8))
        weight = int(item.get('weight', 0))
        value = int(item.get('value', 0))
        
        weight_text = f"W:{weight}"
        weight_surf = thin_font.render(weight_text, True, (0, 0, 0))
        weight_rect = weight_surf.get_rect(topleft=(item_rect.left + 1, item_rect.top + 1))
        surface.blit(weight_surf, weight_rect)
        
        value_text = f"V:{value}"
        value_surf = thin_font.render(value_text, True, (0, 0, 0))
        value_rect = value_surf.get_rect(bottomright=(item_rect.right - 1, item_rect.bottom - 1))
        surface.blit(value_surf, value_rect)

    def update_items(self, items):
        self.items = items
    
    def get_clicked_item(self, mouse_pos):
        for i, rect in enumerate(self.item_rects):
            if rect.collidepoint(mouse_pos):
                return i
        return None
    
    def get_item_position(self, item_index):
        if 0 <= item_index < len(self.item_rects):
            rect = self.item_rects[item_index]
            return (rect.centerx, rect.centery)
        return None

class StatusPanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.turn_text = "Greedy Bag Race"
        self.text_color = (255, 255, 255)
    
    def draw(self, surface):
        title_font_size = int(self.rect.height * 0.5)
        turn_font_size = int(self.rect.height * 0.4)
        
        title_font = pygame.font.SysFont('arial', title_font_size, bold=True)
        turn_font = pygame.font.SysFont('arial', turn_font_size)
        
        
        turn_surf = turn_font.render(self.turn_text, True, self.text_color)
        turn_rect = turn_surf.get_rect(center=(self.rect.centerx, self.rect.centery))
        surface.blit(turn_surf, turn_rect)
    
    def update_turn(self, turn_text):
        self.turn_text = turn_text

class AmountSelector:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = False
        self.current_item_index = None
        self.current_item_weight = 0
        self.max_amount = 0
        self.amount_buttons = []
        
    def show(self, item_index, item_weight, max_amount):
        self.visible = True
        self.current_item_index = item_index
        self.current_item_weight = item_weight
        self.max_amount = min(int(item_weight), max_amount)
        self.amount_buttons = []
        
        button_size = 50
        buttons_per_row = 5
        padding = 10
        
        start_x = self.rect.x + padding
        start_y = self.rect.y + 60
        
        for amount in range(1, self.max_amount + 1):
            row = (amount - 1) // buttons_per_row
            col = (amount - 1) % buttons_per_row
            
            button_rect = pygame.Rect(
                start_x + col * (button_size + padding),
                start_y + row * (button_size + padding),
                button_size, button_size
            )
            
            self.amount_buttons.append((button_rect, amount))
        
    def hide(self):
        self.visible = False
        self.current_item_index = None
        self.amount_buttons = []
        
    def handle_event(self, event):
        if not self.visible: return False, None
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_rect, amount in self.amount_buttons:
                if button_rect.collidepoint(event.pos):
                    fraction = amount / self.current_item_weight if self.current_item_weight > 0 else 0
                    return True, fraction
            if not self.rect.collidepoint(event.pos):
                self.hide()
        return False, None
        
    def draw(self, surface):
        if not self.visible: return
        
        pygame.draw.rect(surface, PANEL_COLOR, self.rect, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=10)
        
        font = pygame.font.SysFont('arial', 24)
        small_font = pygame.font.SysFont('arial', 18)
        
        title_text = f"Pick Amount (Weight: {self.current_item_weight})"
        title_surf = font.render(title_text, True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(self.rect.centerx, self.rect.y + 25))
        surface.blit(title_surf, title_rect)
        
        for button_rect, amount in self.amount_buttons:
            pygame.draw.rect(surface, BUTTON_COLOR, button_rect, border_radius=5)
            pygame.draw.rect(surface, TEXT_COLOR, button_rect, 2, border_radius=5)
            
            amount_surf = small_font.render(str(amount), True, BUTTON_TEXT_COLOR)
            amount_rect = amount_surf.get_rect(center=button_rect.center)
            surface.blit(amount_surf, amount_rect)
        
        pass