import pygame
import time
import os

class AnimatedBackground:
    def __init__(self, frames, fps=2):
        self.frames = frames
        self.fps = fps
        self.frame_delay = 1.0 / fps
        self.current_frame = 0
        self.last_frame_time = time.time()
    
    def update(self):
        current_time = time.time()
        if current_time - self.last_frame_time >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_frame_time = current_time
    
    def get_current_frame(self):
        return self.frames[self.current_frame]
    
    def draw(self, surface):
        surface.blit(self.get_current_frame(), (0, 0))
    
    def set_fps(self, fps):
        self.fps = fps
        self.frame_delay = 1.0 / fps

class BackgroundManager:
    def __init__(self, screen_width, screen_height, fps=2):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        self.backgrounds = {}
        self.load_all_backgrounds()
    
    def load_all_backgrounds(self):
        background_config = {
            "MENU": {
                "frame1": "assets/images/ui/bg1.png",
                "frame2": "assets/images/ui/bg2.png"
            },
            "MODE_SELECT": {
                "frame1": "assets/images/ui/mode1.png",
                "frame2": "assets/images/ui/mode2.png"
            },
            "DIFFICULTY_SELECT": {
                "frame1": "assets/images/ui/diff1.png",
                "frame2": "assets/images/ui/diff2.png"
            },
            "IN_GAME_SINGLE": {
                "frame1": "assets/images/ui/game1.png",
                "frame2": "assets/images/ui/game2.png"
            },
            "IN_GAME_MULTI": {
                "frame1": "assets/images/ui/game1.png",
                "frame2": "assets/images/ui/game2.png"
            },
            "YOU_WIN": {
                "frame1": "assets/images/ui/uwin1.png",
                "frame2": "assets/images/ui/uwin2.png"
            },
            "AI_WIN": {
                "frame1": "assets/images/ui/aiw1.png",
                "frame2": "assets/images/ui/aiw2.png"
            },
            "PLAYER1_WIN": {
                "frame1": "assets/images/ui/p11.png",
                "frame2": "assets/images/ui/p12.png"
            },
            "PLAYER2_WIN": {
                "frame1": "assets/images/ui/p21.png",
                "frame2": "assets/images/ui/p22.png"
            }
        }
        
        for state, config in background_config.items():
            try:
                if os.path.exists(config["frame1"]):
                    frame1 = pygame.image.load(config["frame1"])
                    frame1 = pygame.transform.scale(frame1, (self.screen_width, self.screen_height))
                else:
                    frame1 = self.create_fallback_background(state)
                
                if os.path.exists(config["frame2"]):
                    frame2 = pygame.image.load(config["frame2"])
                    frame2 = pygame.transform.scale(frame2, (self.screen_width, self.screen_height))
                else:
                    frame2 = self.create_variant_background(state, frame1)
                
                self.backgrounds[state] = AnimatedBackground([frame1, frame2], fps=self.fps)
                print(f"Loaded background for {state} at {self.fps} FPS")
                
            except Exception as e:
                print(f"Error loading background for {state}: {e}")
                frame1 = self.create_fallback_background(state)
                frame2 = self.create_variant_background(state, frame1)
                self.backgrounds[state] = AnimatedBackground([frame1, frame2], fps=self.fps)
    
    def create_fallback_background(self, state):
        """Create a colored fallback background based on game state"""
        surface = pygame.Surface((self.screen_width, self.screen_height))
        
        color_map = {
            "MENU": (30, 30, 80),
            "SELECT_MODE": (40, 30, 70),
            "DIFFICULTY_SELECT": (30, 50, 70),
            "IN_GAME_SINGLE": (20, 40, 30),
            "IN_GAME_MULTI": (40, 20, 30),
            "YOU_WIN": (30, 60, 30),
            "AI_WIN": (60, 30, 30),
            "PLAYER1_WIN": (30, 30, 80),
            "PLAYER2_WIN": (80, 30, 30)
        }
        
        base_color = color_map.get(state, (30, 30, 80))
        surface.fill(base_color)
        
        for i in range(50):
            x = pygame.time.get_ticks() % self.screen_width
            y = (i * 40 + pygame.time.get_ticks() // 10) % self.screen_height
            radius = 5 + (i % 3)
            color_variant = (
                min(255, base_color[0] + 20 + i * 2),
                min(255, base_color[1] + 20 + i * 2),
                min(255, base_color[2] + 20 + i * 2)
            )
            pygame.draw.circle(surface, color_variant, (x, y), radius)
        
        return surface
    
    def create_variant_background(self, state, base_frame):
        """Create a slightly different version of the background for animation"""
        variant = base_frame.copy()
        
        if state in ["YOU_WIN", "AI_WIN", "PLAYER1_WIN", "PLAYER2_WIN"]:
            for i in range(20):
                x = (pygame.time.get_ticks() // 5 + i * 50) % self.screen_width
                y = (pygame.time.get_ticks() // 8 + i * 30) % self.screen_height
                pygame.draw.circle(variant, (255, 255, 200), (x, y), 3)
        else:
            for i in range(10):
                x = (pygame.time.get_ticks() // 10 + i * 100) % self.screen_width
                y = (i * 80) % self.screen_height
                pygame.draw.circle(variant, (100, 100, 150, 100), (x, y), 8)
        
        return variant
    
    def get_background(self, state):
        return self.backgrounds.get(state)
    
    def update(self, state):
        if state in self.backgrounds:
            self.backgrounds[state].update()
    
    def set_fps(self, fps):
        self.fps = fps
        for background in self.backgrounds.values():
            background.set_fps(fps)