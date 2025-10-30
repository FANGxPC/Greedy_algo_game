class Player:
    def __init__(self, name, bag_limit=10):
        self.name = name
        self.bag = []
        self.bag_limit = float(bag_limit)
        self.current_weight = 0.0
        self.total_value = 0.0

    def can_pick_fraction(self, item, fraction=1.0):
        """Check if a fraction of the item can be picked"""
        if fraction <= 0 or fraction > 1:
            return False
        weight_to_add = item.weight * fraction
        return (self.current_weight + weight_to_add) <= self.bag_limit

    def get_available_fraction(self, item):
        """Calculate maximum fraction that can be picked"""
        available_space = self.bag_limit - self.current_weight
        if available_space <= 0.001:
            return 0.0
        if item.weight <= 0.001:
            return 0.0
        return min(1.0, available_space / item.weight)

    def add_item_fraction(self, item, fraction=1.0):
        """Add a fraction of an item to the bag"""
        if fraction is None or fraction <= 0:
            return False, "Invalid fraction"
        if fraction > 1:
            fraction = 1.0
        
        max_fraction = self.get_available_fraction(item)
        if max_fraction <= 0:
            return False, "Not enough space in bag"
        if fraction > max_fraction:
            fraction = max_fraction
        
        taken_piece = item.take_fraction(fraction)
        if not taken_piece:
            return False, "Failed to take fraction"
        
        self.bag.append(taken_piece)
        self.current_weight += taken_piece["weight"]
        self.total_value += taken_piece["value"]
        return True, f"Added {fraction:.2f} of {item.name}"

    def get_item_count(self):
        return len(self.bag)

    def get_bag_status(self):
        bag_items = []
        for it in self.bag:
            bag_items.append({
                "name": it["name"],
                "weight": it["weight"],
                "value": it["value"],
            })

        return {
            "name": self.name,
            "bag": bag_items,
            "weight": self.current_weight,
            "value": self.total_value,
            "space_left": self.bag_limit - self.current_weight
        }

    def __str__(self):
        return f"{self.name}: {len(self.bag)} items, {self.current_weight:.1f}/{self.bag_limit} weight, {self.total_value:.1f} value"