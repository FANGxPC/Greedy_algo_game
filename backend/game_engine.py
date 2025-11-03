import random
from backend.player import Player
from backend.ai import AI
from backend.items import Item

class GameEngine:
    def __init__(self, bag_capacity=25):
        self.players = []
        self.available_items = []
        self.bag_capacity = bag_capacity
        self.current_player_index = 0
        self.game_over = False
        self.ai_players = {}
    
    def initialize_game(self, player_names, is_multiplayer=False, ai_difficulty="Medium"):
        """Initialize the game with players"""
        self.players = [Player(name, self.bag_capacity) for name in player_names]
        self.available_items = self._generate_items()
        self.current_player_index = 0
        self.game_over = False
        self.ai_players = {}
        
        if not is_multiplayer and len(player_names) == 2:
            self.ai_players[1] = AI(ai_difficulty)
    
    def _generate_items(self):
        """Generate random items for the game by selecting 25 random items from the available 50"""
        all_item_numbers = list(range(1, 51))
        selected_numbers = random.sample(all_item_numbers, 25)
        
        items = []
        for i in selected_numbers:
            name = f"Item {i}"
            weight = random.randint(1, 10)
            value = random.randint(5, 25)
            image_filename = f"i{i}.png"
            items.append(Item(name, weight, value, image_filename))
        
        items.sort(key=lambda x: int(''.join(filter(str.isdigit, x.image_filename))))
        return items
    
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def is_ai_turn(self):
        return self.current_player_index in self.ai_players
    
    def human_pick_fraction(self, item_index, fraction: float):
        """Human player picks a fraction of an item."""
        if self.game_over or self.is_ai_turn():
            return False, "Not human player's turn"

        if item_index < 0 or item_index >= len(self.available_items):
            return False, "Invalid item index"

        item = self.available_items[item_index]
        if item.is_depleted():
            return False, "Item is already depleted"

        current_player = self.get_current_player()
        max_fraction = current_player.get_available_fraction(item)
        if max_fraction <= 0:
            return False, "Not enough space in bag"
        if fraction > max_fraction:
            fraction = max_fraction
        if fraction <= 0:
            return False, "Invalid fraction"

        success, message = current_player.add_item_fraction(item, fraction)
        if success:
            self.available_items = [it for it in self.available_items if not it.is_depleted()]
            self._next_turn()
            return True, message
        else:
            return False, message
    
    def skip_turn(self):
        """Skip current player's turn"""
        self._next_turn()
    
    def get_max_available_fraction(self, item_index):
        """Get maximum fraction that can be picked for an item"""
        if item_index < 0 or item_index >= len(self.available_items):
            return 0.0
        
        item = self.available_items[item_index]
        if item.is_depleted():
            return 0.0
        
        current_player = self.get_current_player()
        return current_player.get_available_fraction(item)
    
    def ai_make_move(self):
        """AI player makes a move based on difficulty"""
        if not self.is_ai_turn():
            return None, None
        
        current_player = self.get_current_player()
        
        if current_player.current_weight >= current_player.bag_limit:
            self._next_turn()
            return None, None
        
        ai = self.ai_players[self.current_player_index]
        difficulty = ai.difficulty
        
        valid_items = [item for item in self.available_items if not item.is_depleted()]
        if not valid_items:
            self._next_turn()
            return None, None
        
        if difficulty == "Easy":
            item, fraction = self._ai_random_pick(valid_items, current_player)
        elif difficulty == "Medium":
            item, fraction = self._ai_01_knapsack(valid_items, current_player)
        else:
            item, fraction = self._ai_fractional_knapsack(valid_items, current_player)
        
        if item and fraction > 0:
            success, _ = current_player.add_item_fraction(item, fraction)
            if success:
                self.available_items = [it for it in self.available_items if not it.is_depleted()]
                self._next_turn()
                return item, fraction
        
        self._next_turn()
        return None, None
    
    def _ai_random_pick(self, valid_items, player):
        """Easy: Random pick of a random item"""
        pickable_items = [item for item in valid_items if player.get_available_fraction(item) > 0]
        if not pickable_items:
            return None, 0

        item = random.choice(pickable_items)
        max_frac = player.get_available_fraction(item)
        fraction = random.uniform(0.1, max_frac)
        return item, fraction
    
    def _ai_01_knapsack(self, valid_items, player):
        """Medium: 0/1 knapsack - pick whole items greedily by value/weight ratio"""
        if not valid_items:
            return None, 0
        sorted_items = sorted(valid_items, key=lambda x: x.ratio, reverse=True)
        for item in sorted_items:
            max_frac = player.get_available_fraction(item)
            if max_frac >= 0.99:
                return item, 1.0
        if sorted_items:
            item = sorted_items[0]
            max_frac = player.get_available_fraction(item)
            if max_frac > 0:
                return item, max_frac
        return None, 0
    
    def _ai_fractional_knapsack(self, valid_items, player):
        """Hard: Fractional knapsack - greedy by value/weight ratio"""
        if not valid_items:
            return None, 0
        sorted_items = sorted(valid_items, key=lambda x: x.ratio, reverse=True)
        for item in sorted_items:
            max_frac = player.get_available_fraction(item)
            if max_frac > 0:
                return item, max_frac
        return None, 0
    
    def _next_turn(self):
        """Move to next player and check game over condition"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self._check_game_over()
    
    def _check_game_over(self):
        """Check if game should end"""
        all_bags_full = all(player.current_weight >= player.bag_limit for player in self.players)
        no_items_left = len(self.available_items) == 0
        self.game_over = all_bags_full or no_items_left
    
    def get_winner(self):
        """Determine the winner based on total value collected"""
        if not self.game_over:
            return None
        
        max_value = max(player.total_value for player in self.players)
        winners = [player for player in self.players if player.total_value == max_value]
        
        if len(winners) == 1:
            return winners[0]
        else:
            return None
    
    def get_game_state(self):
        """Return current game state for frontend"""
        return {
            "players": [player.get_bag_status() for player in self.players],
            "available_items": [
                {
                    "name": item.name,
                    "weight": item.weight,
                    "value": item.value,
                    "ratio": item.ratio,
                    "original_weight": item.original_weight,
                    "image_filename": item.image_filename
                }
                for item in self.available_items
            ],
            "current_player": self.current_player_index,
            "game_over": self.game_over,
            "winner": self.get_winner().name if self.get_winner() else None
        }
    
    def set_ai_difficulty(self, difficulty):
        """Change AI difficulty during game"""
        for ai in self.ai_players.values():
            ai.set_difficulty(difficulty)