import pygame
import math
import random

class Animation:
    def __init__(self, duration=1000):
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.completed = False
    
    def update(self):
        current_time = pygame.time.get_ticks()
        progress = (current_time - self.start_time) / self.duration
        
        if progress >= 1:
            self.completed = True
            progress = 1
        
        return progress

class ScoreAnimation(Animation):
    def __init__(self, score, start_pos, end_pos, color=(255, 255, 0)):
        super().__init__(duration=1200)
        self.score = score
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.current_pos = start_pos
        self.color = color
        self.alpha = 255
        self.scale = 1.0
    
    def update(self):
        progress = super().update()
        
        eased_progress = 1 - (1 - progress) ** 4
        
        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]
        self.current_pos = (
            self.start_pos[0] + dx * eased_progress,
            self.start_pos[1] + dy * eased_progress
        )
        
        if progress < 0.2:
            self.scale = 1.0 + 1.5 * (progress / 0.2)
        else:
            self.scale = 2.5 - 1.5 * ((progress - 0.2) / 0.8)

        if progress > 0.6:
            self.alpha = int(255 * (1 - (progress - 0.6) / 0.4))
        
        return self.completed
    
    def draw(self, surface):
        font_size = int(12 * self.scale)
        if font_size < 1: return

        try:
            font = pygame.font.Font("assets/fonts/pixel_font.ttf", font_size)
        except:
            font = pygame.font.SysFont('Courier New', font_size, bold=True)

        text_surf = font.render(f"+{self.score:.0f}", True, self.color)
        text_surf.set_alpha(self.alpha)
        
        outline_surf = font.render(f"+{self.score:.0f}", True, (0,0,0))
        outline_surf.set_alpha(self.alpha)

        text_rect = text_surf.get_rect(center=self.current_pos)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
             surface.blit(outline_surf, text_rect.move(dx, dy))

        surface.blit(text_surf, text_rect)


class ParticleEffect(Animation):
    def __init__(self, position, color=(255, 215, 0), particle_count=25):
        super().__init__(duration=800)
        self.position = position
        self.color = color
        self.particles = []
        self.pixel_size = 4
        
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            self.particles.append({
                'position': list(position),
                'velocity': [math.cos(angle) * speed, math.sin(angle) * speed - 2],
                'size': random.randint(2, 5),
                'life': 1.0
            })
    
    def update(self):
        progress = super().update()
        
        for particle in self.particles:
            particle['position'][0] += particle['velocity'][0]
            particle['position'][1] += particle['velocity'][1]
            particle['velocity'][1] += 0.15
            particle['life'] = 1.0 - progress
            particle['size'] *= 0.96
        
        return self.completed
    
    def draw(self, surface):
        for particle in self.particles:
            if particle['life'] > 0:
                alpha = int(255 * particle['life'])
                size = int(particle['size'])
                if size <= 0: continue

                px = int(particle['position'][0] / self.pixel_size) * self.pixel_size
                py = int(particle['position'][1] / self.pixel_size) * self.pixel_size
                
                particle_color = (*self.color, alpha)
                
                pygame.draw.rect(surface, particle_color, 
                                (px, py, size * self.pixel_size, size * self.pixel_size))


class TextFlashAnimation(Animation):
    def __init__(self, text, position, font_size=24, color=(255, 255, 255), flash_count=3):
        super().__init__(duration=1000)
        self.text = text
        self.position = position
        self.font_size = font_size
        self.color = color
        self.flash_count = flash_count
        self.alpha = 255
    
    def update(self):
        progress = super().update()
        
        flash_progress = progress * self.flash_count
        flash_phase = flash_progress % 1.0
        
        self.alpha = 255 if flash_phase < 0.5 else 128
        
        if progress > 0.7:
            self.alpha = int(255 * (1 - (progress - 0.7) / 0.3))
        
        return self.completed
    
    def draw(self, surface):
        try:
            font = pygame.font.Font("assets/fonts/pixel_font.ttf", self.font_size)
        except:
            font = pygame.font.SysFont('Courier New', self.font_size, bold=True)

        text_surf = font.render(self.text, True, self.color)
        text_surf.set_alpha(self.alpha)
        
        outline_surf = font.render(self.text, True, (0, 0, 0))
        outline_surf.set_alpha(self.alpha // 2)
        
        text_rect = text_surf.get_rect(center=self.position)
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            surface.blit(outline_surf, text_rect.move(dx, dy))
        
        surface.blit(text_surf, text_rect)

class ProgressBarAnimation(Animation):
    def __init__(self, target_value, duration=500):
        super().__init__(duration=duration)
        self.target_value = target_value
        self.current_value = 0
        self.start_value = 0
    
    def set_start_value(self, start_value):
        self.start_value = start_value
        self.current_value = start_value
    
    def update(self):
        progress = super().update()
        self.current_value = self.start_value + (self.target_value - self.start_value) * progress
        return self.completed

class AnimationManager:
    def __init__(self):
        self.animations = []
    
    def add_animation(self, animation):
        self.animations.append(animation)
    
    def add_score_animation(self, score, start_pos, end_pos, color=(255, 255, 0)):
        self.animations.append(ScoreAnimation(score, start_pos, end_pos, color))
    
    def add_particle_effect(self, position, color=(255, 215, 0), particle_count=25):
        self.animations.append(ParticleEffect(position, color, particle_count))
    
    def add_text_flash(self, text, position, font_size=24, color=(255, 255, 255), flash_count=3):
        self.animations.append(TextFlashAnimation(text, position, font_size, color, flash_count))
    
    def add_progress_animation(self, target_value, duration=500):
        animation = ProgressBarAnimation(target_value, duration)
        self.animations.append(animation)
        return animation
    
    def update(self):
        self.animations = [anim for anim in self.animations if not anim.completed]
        for animation in self.animations:
            animation.update()
    
    def draw(self, surface):
        for animation in self.animations:
            if hasattr(animation, 'draw'):
                animation.draw(surface)
    
    def clear_all(self):
        self.animations = []
    
    def has_animations(self):
        return len(self.animations) > 0
