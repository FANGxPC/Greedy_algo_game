import pygame
import sys
import os

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

BG_COLOR = (45, 45, 65)
PANEL_COLOR = (60, 60, 80)
BUTTON_COLOR = (80, 120, 200)
BUTTON_HOVER_COLOR = (100, 140, 220)
BUTTON_TEXT_COLOR = (255, 255, 255)
TEXT_COLOR = (240, 240, 240)
PLAYER1_COLOR = (65, 105, 225)
PLAYER2_COLOR = (220, 60, 60)
HIGHLIGHT_COLOR = (255, 215, 0)

BAG_CAPACITY = 25

from gui.background import BackgroundManager
from gui.buttons import Button
from gui.panels import BagPanel, ItemPanel, StatusPanel, AmountSelector
from backend.game_engine import GameEngine
from gui.animations import AnimationManager

class GreedyBagRace:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        
        self.clock = pygame.time.Clock()
        
        self.game_state = "MENU"
        self.difficulty = "Medium"
        self.game_mode = None
        self.ai_move_timer = 0
        self.ai_move_delay = 60
        
        self.background_manager = BackgroundManager(self.screen_width, self.screen_height)
        self.animation_manager = AnimationManager()
        self.amount_selector = AmountSelector(
            self.screen_width//2 - 250, 
            self.screen_height//2 - 150, 
            500, 300
        )
        
        self.game_engine = GameEngine(bag_capacity=BAG_CAPACITY)
        
        self.init_audio()
        self.init_gui()
        
        print(f"Running in fullscreen: {self.screen_width}x{self.screen_height}")
    
    def init_audio(self):
        self.bgm_tracks = {}
        bgm_config = {
            "MENU": "assets/sounds/main_menu.mp3",
            "DIFFICULTY_SELECT": "assets/sounds/main_menu.mp3",
            "IN_GAME_SINGLE": "assets/sounds/background.mp3", 
            "IN_GAME_MULTI": "assets/sounds/background.mp3",
            "YOU_WIN": "assets/sounds/win.mp3",
            "AI_WIN": "assets/sounds/lost.mp3",
            "PLAYER1_WIN": "assets/sounds/win.mp3",
            "PLAYER2_WIN": "assets/sounds/win.mp3"
        }
        
        print("Available sound files:")
        sound_dir = "assets/sounds"
        if os.path.exists(sound_dir):
            for f in os.listdir(sound_dir):
                if f.endswith(('.mp3', '.wav', '.ogg')):
                    print(f"- {os.path.join(sound_dir, f)}")
        
        self.sounds = {}
        try:
            for state, path in bgm_config.items():
                full_path = os.path.join(os.getcwd(), path)
                if os.path.exists(path):
                    self.bgm_tracks[state] = path
                    print(f"Loaded BGM for {state}: {path}")
                else:
                    print(f"Warning: BGM file not found: {path}")
            
            sound_paths = {
                'click': "assets/sounds/click.wav",
                'pick_item': "assets/sounds/pick_item.wav",
                'win': "assets/sounds/win.mp3",
                'lose': "assets/sounds/lost.mp3"
            }
            
            for key, path in sound_paths.items():
                if os.path.exists(path):
                    self.sounds[key] = pygame.mixer.Sound(path)
                    print(f"Loaded sound effect: {key} from {path}")
                else:
                    print(f"Warning: Sound file not found: {path}")
                    
        except Exception as e:
            print(f"Audio initialization error: {e}")
        
        self.play_bgm("MENU")
    
    def play_bgm(self, state):
        if state in self.bgm_tracks:
            try:
                pygame.mixer.music.load(self.bgm_tracks[state])
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"Error playing BGM for {state}: {e}")
    
    def init_gui(self):
        panel_width = self.screen_width // 4
        panel_height = self.screen_height - 200
        item_panel_width = self.screen_width // 3
        
        self.player1_panel = BagPanel(50, 150, panel_width, panel_height, "Player 1", player_type="human", player_index=0)
        self.player2_panel = BagPanel(self.screen_width  - 150, 150, panel_width, panel_height, "Player 2", player_type="ai", player_index=1)
        self.item_panel = ItemPanel(
            (self.screen_width - item_panel_width) // 2, 
            150, 
            item_panel_width, 
            self.screen_height - 200
        )
        self.status_panel = StatusPanel(50, 50, self.screen_width - 100, 80)
        
        button_width = 300
        button_height = 70
        base_y = self.screen_height // 2

        self.menu_buttons = [
            Button(700, 300, button_width-70, button_height+20, 
                  "▶️ Start Game", self.show_mode_select),
            Button(950, 300, button_width-70, button_height+20, 
                  "❌ Quit Game", self.quit_game)
        ]
        
        self.mode_buttons = [
            Button(650,  450, button_width+350, button_height+70, 
                  "🎮 Single Player", self.show_difficulty_select),
            Button(650, 650, button_width+350, button_height+70, 
                  "👥 Multiplayer", self.start_multiplayer),
            Button(70,900, 100, 100, 
                  "🔙 Back", self.show_main_menu)
        ]
        
        self.difficulty_buttons = [
            Button(750, 330, button_width+100, button_height+50, 
                  "😊 Easy", lambda: self.set_difficulty("Easy")),
            Button(750, 330 + 180, button_width+100, button_height+50, 
                  "😐 Medium", lambda: self.set_difficulty("Medium")),
            Button(750, 330 + 350, button_width+100, button_height+50, 
                  "😈 Hard", lambda: self.set_difficulty("Hard")),
            Button(70,900, 100, 100, 
                  "🔙 Back", self.show_main_menu)
        ]

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "MENU":
                    self.handle_click(event, self.menu_buttons)
                elif self.game_state == "MODE_SELECT":
                    self.handle_click(event, self.mode_buttons)
                elif self.game_state == "DIFFICULTY_SELECT":
                    self.handle_difficulty_click(event)
                elif self.game_state in ["IN_GAME_SINGLE", "IN_GAME_MULTI"]:
                    self.handle_game_click(event)
                elif self.game_state in ["YOU_WIN", "AI_WIN", "PLAYER1_WIN", "PLAYER2_WIN"]:
                    if hasattr(self, 'game_over_back_button') and self.game_over_back_button.is_hovered():
                        self.game_over_back_button.click()
    
    def handle_click(self, event, buttons):
        for button in buttons:
            if button.is_hovered():
                self.play_sound('click')
                button.click()
    
    def handle_difficulty_click(self, event):
        for button in self.difficulty_buttons:
            if button.is_hovered():
                self.play_sound('click')
                button.click()
    
    def handle_game_click(self, event):
        game_state = self.game_engine.get_game_state()
        current_player = game_state["players"][game_state["current_player"]]
        
        if not self.game_engine.is_ai_turn() and current_player["space_left"] <= 0:
            self.game_engine.skip_turn()
            return
        
        handled, fraction = self.amount_selector.handle_event(event)
        if handled and fraction is not None:
            game_state = self.game_engine.get_game_state()
            item_index = self.amount_selector.current_item_index
            if item_index is not None and 0 <= item_index < len(game_state["available_items"]):
                item = game_state["available_items"][item_index]
                item_value = item['value'] * fraction
                start_pos = self.item_panel.get_item_position(item_index)
                
                current_player_index = self.game_engine.current_player_index
                if current_player_index == 0:
                    end_pos = self.player1_panel.get_score_position()
                else:
                    end_pos = self.player2_panel.get_score_position()

                if start_pos and end_pos:
                    self.animation_manager.add_particle_effect(start_pos)
                    self.animation_manager.add_score_animation(item_value, start_pos, end_pos)

                self.play_sound('pick_item')
                self.game_engine.human_pick_fraction(item_index, float(fraction))
            self.amount_selector.hide()
            return
        
        if self.amount_selector.visible and not self.amount_selector.rect.collidepoint(event.pos):
            self.amount_selector.hide()
            return
        
        if not self.game_engine.is_ai_turn() and current_player["space_left"] > 0:
            item_index = self.item_panel.get_clicked_item(event.pos)
            if item_index is not None and not self.amount_selector.visible:
                self.show_amount_selector(item_index)
    
    def show_amount_selector(self, item_index):
        game_state = self.game_engine.get_game_state()
        if item_index >= len(game_state["available_items"]):
            return
        
        item = game_state["available_items"][item_index]
        item_weight = item["weight"]
        
        current_player = game_state["players"][game_state["current_player"]]
        available_space = current_player["space_left"]
        max_amount = min(int(item_weight), int(available_space))
        
        if max_amount > 0:
            self.amount_selector.show(item_index, item_weight, max_amount)
    
    def handle_game_over_click(self, event):
        self.show_main_menu()
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.animation_manager.update()
        self.background_manager.update(self.game_state)
        
        if self.game_state == "MENU":
            for button in self.menu_buttons:
                button.update_hover(mouse_pos)
        elif self.game_state == "DIFFICULTY_SELECT":
            for button in self.difficulty_buttons:
                button.update_hover(mouse_pos)
        
        if self.game_state in ["IN_GAME_SINGLE", "IN_GAME_MULTI"]:
            if not self.game_engine.game_over:
                current = self.game_engine.get_current_player()

                if current.current_weight >= current.bag_limit:
                    self.game_engine.skip_turn()
                elif self.game_engine.is_ai_turn():
                    if self.ai_move_timer < self.ai_move_delay:
                        self.ai_move_timer += 1
                    else:
                        self.ai_move_timer = 0
                        pre_move_state = self.game_engine.get_game_state()
                        self.game_engine.ai_make_move()
                        post_move_state = self.game_engine.get_game_state()

                        p2_score_before = pre_move_state['players'][1]['value']
                        p2_score_after = post_move_state['players'][1]['value']
                        score_diff = p2_score_after - p2_score_before

                        pre_items = { (item['name'], item['original_weight']): item for item in pre_move_state['available_items'] }
                        post_items = { (item['name'], item['original_weight']): item for item in post_move_state['available_items'] }
                        
                        picked_item_pos = None

                        for i, item_before in enumerate(pre_move_state['available_items']):
                            key = (item_before['name'], item_before['original_weight'])
                            if key not in post_items:
                                picked_item_pos = self.item_panel.get_item_position(i)
                                break
                            else:
                                item_after = post_items[key]
                                if item_after['weight'] < item_before['weight']:
                                    picked_item_pos = self.item_panel.get_item_position(i)
                                    break
                        
                        if picked_item_pos:
                            self.play_sound('pick_item')
                            self.animation_manager.add_particle_effect(picked_item_pos)
                            if score_diff > 0:
                                end_pos = self.player2_panel.get_score_position()
                                self.animation_manager.add_score_animation(score_diff, picked_item_pos, end_pos)

            self.update_panels()

            if self.game_engine.game_over:
                winner = self.game_engine.get_winner()
                if self.game_mode == "single":
                    if winner and "Player" in winner.name:
                        self.change_state("YOU_WIN")
                        self.play_sound('win')
                    else:
                        self.change_state("AI_WIN")
                        self.play_sound('lose')
                else:
                    if winner and "Player 1" in winner.name:
                        self.change_state("PLAYER1_WIN")
                    else:
                        self.change_state("PLAYER2_WIN")
                    self.play_sound('win')

    def update_panels(self):
        game_state = self.game_engine.get_game_state()
        self.player1_panel.update_player_data(
            game_state["players"][0]["bag"],
            game_state["players"][0]["weight"],
            self.game_engine.bag_capacity,
            game_state["players"][0]["value"]
        )
        self.player2_panel.update_player_data(
            game_state["players"][1]["bag"],
            game_state["players"][1]["weight"],
            self.game_engine.bag_capacity,
            game_state["players"][1]["value"]
        )
        self.item_panel.update_items(game_state["available_items"])
        self.status_panel.update_turn(f"Current Turn: {game_state['players'][game_state['current_player']]['name']}")
    
    def render(self):
        background = self.background_manager.get_background(self.game_state)
        if background:
            background.draw(self.screen)
        else:
            self.screen.fill(BG_COLOR)
        
        if self.game_state == "MENU":
            self.render_menu()
        elif self.game_state == "MODE_SELECT":
            self.render_mode_select()
        elif self.game_state == "DIFFICULTY_SELECT":
            self.render_difficulty_select()
        elif self.game_state in ["IN_GAME_SINGLE", "IN_GAME_MULTI"]:
            self.render_game()
        elif self.game_state in ["YOU_WIN", "AI_WIN", "PLAYER1_WIN", "PLAYER2_WIN"]:
            self.render_game_over()
        
        pygame.display.flip()
    
    def render_menu(self):
        for button in self.menu_buttons:
            button.draw(self.screen)
    
    def render_mode_select(self):
        for button in self.mode_buttons:
            button.draw(self.screen)
    
    def render_difficulty_select(self):
        for button in self.difficulty_buttons:
            button.draw(self.screen)
    
    def render_game(self):
        self.player1_panel.draw(self.screen)
        self.player2_panel.draw(self.screen)
        self.item_panel.draw(self.screen)
        self.status_panel.draw(self.screen)
        
        if self.amount_selector.visible:
            self.amount_selector.draw(self.screen)

        self.animation_manager.draw(self.screen)
        
        small_font = pygame.font.SysFont('arial', self.screen_height // 40)
        
        if self.game_mode == "single":
            mode_text = "Single Player" if self.game_state == "IN_GAME_SINGLE" else "Multiplayer"
        
        info_text = ""
        info_surf = small_font.render(info_text, True, TEXT_COLOR)
        info_rect = info_surf.get_rect(center=(self.screen_width//2, self.screen_height - 30))
        self.screen.blit(info_surf, info_rect)
    
    def render_game_over(self):
        font = pygame.font.SysFont('arial', self.screen_height // 50)
        
        winner = self.game_engine.get_winner()
        winner_name = winner.name if winner else "Tie"
        
        game_state = self.game_engine.get_game_state()
        p1_value = game_state["players"][0]["value"]
        p2_value = game_state["players"][1]["value"]
        
        score_text = f"{p1_value:.1f} - {p2_value:.1f}"
        score_surf = font.render(score_text, True, TEXT_COLOR)
        score_rect = score_surf.get_rect(midbottom=(self.screen_width//2, self.screen_height - 50))
        
        winner_text = f"Winner: {winner_name}" if winner_name != "Tie" else "🏆 Tie! 🏆"
        winner_surf = font.render(winner_text, True, HIGHLIGHT_COLOR)
        winner_rect = winner_surf.get_rect(midbottom=(self.screen_width//2, score_rect.top - 5))
        
        line_y = winner_rect.top - 5
        pygame.draw.line(self.screen, HIGHLIGHT_COLOR, 
                        (self.screen_width//2 - 50, line_y), 
                        (self.screen_width//2 + 50, line_y), 1)
        
        self.screen.blit(winner_surf, winner_rect)
        self.screen.blit(score_surf, score_rect)
        
        back_button = Button(40,900, 150, 150, "🔙 Menu", self.show_main_menu)
        back_button.draw(self.screen)
        
        self.game_over_back_button = back_button
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def change_state(self, new_state):
        old_state = self.game_state
        self.game_state = new_state
        
        if old_state != new_state:
            self.play_bgm(new_state)
    
    def start_single_player(self):
        self.change_state("DIFFICULTY_SELECT")
    
    def start_multiplayer(self):
        self.game_mode = "multi"
        self.game_engine.initialize_game(["Player 1", "Player 2"], is_multiplayer=True)
        self.change_state("IN_GAME_MULTI")
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.game_mode = "single"
        self.game_engine.initialize_game(["Player", f"AI ({difficulty})"], is_multiplayer=False, ai_difficulty=difficulty)
        self.change_state("IN_GAME_SINGLE")
    
    def show_main_menu(self):
        self.change_state("MENU")
        
    def show_mode_select(self):
        self.change_state("MODE_SELECT")
        
    def show_difficulty_select(self):
        self.change_state("DIFFICULTY_SELECT")
        
    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GreedyBagRace()
    game.run()
