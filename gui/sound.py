import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_files = {
            "MENU": "assets/sounds/main_menu.mp3",
            "SELECT_MODE": "assets/sounds/main_menu.mp3",
            "DIFFICULTY_SELECT": "assets/sounds/main_menu.mp3",
            "IN_GAME_SINGLE": "assets/sounds/background.mp3",
            "IN_GAME_MULTI": "assets/sounds/background.mp3",
            "YOU_WIN": "assets/sounds/win.mp3",
            "AI_WIN": "assets/sounds/lost.mp3",
            "PLAYER1_WIN": "assets/sounds/win.mp3",
            "PLAYER2_WIN": "assets/sounds/win.mp3"
        }
        self.current_music = None
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound effects"""
        sound_effects = {
            'click': "assets/sounds/click.wav",
            'pick_item': "assets/sounds/pick_item.wav"
        }
        
        try:
            for sound_name, file_path in sound_effects.items():
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    print(f"Loaded sound: {sound_name}")
                else:
                    print(f"Sound file not found: {file_path}")
            
            for sound in self.sounds.values():
                sound.set_volume(0.5)
                
        except Exception as e:
            print(f"Error loading sounds: {e}")
    
    def play_background_music(self, state):
        """Play background music for specific state"""
        music_file = self.music_files.get(state)
        
        if music_file and os.path.exists(music_file):
            if self.current_music != music_file:
                try:
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.3)
                    self.current_music = music_file
                    print(f"Playing music for {state}: {music_file}")
                except pygame.error as e:
                    print(f"Could not play music {music_file}: {e}")
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.current_music = None
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()