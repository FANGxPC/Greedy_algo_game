import random
from backend.items import Item

class AI:
    def __init__(self, difficulty="Medium"):
        self.difficulty = difficulty
    
    def pick_item(self, available_items, player):
        """AI picks an item based on difficulty level"""
        if not available_items:
            return None, 1.0
        
        # Filter out depleted items
        valid_items = [item for item in available_items if not item.is_depleted()]
        if not valid_items:
            return None, 1.0
        
        if self.difficulty == "Easy":
            return self._easy_pick(valid_items, player)
        elif self.difficulty == "Medium":
            return self._medium_pick(valid_items, player)
        elif self.difficulty == "Hard":
            return self._hard_pick(valid_items, player)
        else:
            return self._medium_pick(valid_items, player)
    
    def _easy_pick(self, available_items, player):
        """Easy: Random pick from available items that fit (can take fractions)"""
        # Try to pick a random item, taking as much as possible
        random.shuffle(available_items)
        
        for item in available_items:
            max_fraction = player.get_available_fraction(item)
            if max_fraction > 0:
                # Easy AI takes random fraction between 0.5 and 1.0
                fraction = random.uniform(0.5, 1.0)
                fraction = min(fraction, max_fraction)
                return item, fraction
        
        return None, 1.0
    
    def _medium_pick(self, available_items, player):
        """Medium: 0/1 Knapsack - Prefers complete items but can take fractions if needed"""
        # Sort by value (descending)
        sorted_by_value = sorted(available_items, key=lambda x: x.value, reverse=True)
        
        for item in sorted_by_value:
            max_fraction = player.get_available_fraction(item)
            if max_fraction > 0:
                # Medium AI prefers complete items but will take fractions
                if max_fraction >= 0.95:  # Almost whole item
                    return item, 1.0
                elif max_fraction >= 0.7:  # Reasonable fraction
                    return item, max_fraction
        
        return None, 1.0
    
    def _hard_pick(self, available_items, player):
        """Hard: Fractional Knapsack - Optimizes value-to-weight ratio"""
        # Sort items by value-to-weight ratio (descending)
        sorted_items = sorted(available_items, key=lambda x: x.ratio, reverse=True)
        
        remaining_capacity = player.bag_limit - player.current_weight
        
        for item in sorted_items:
            if item.weight <= remaining_capacity:
                # Can take the whole item
                return item, 1.0
            elif item.weight > 0 and remaining_capacity > 0:
                # Take as much as possible (fraction)
                fraction = remaining_capacity / item.weight
                if fraction > 0.01:  # At least 1%
                    return item, fraction
        
        return None, 1.0
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty