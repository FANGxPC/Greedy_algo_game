class Item:
    def __init__(self, name, weight, value, image_filename):
        self.name = name
        self.weight = int(weight)
        self.value = float(value)
        self.image_filename = image_filename
        self.original_weight = int(weight)
        self.original_value = float(value)
        self.unit_value = self.value / self.original_weight if self.original_weight > 0 else 0.0
        self.ratio = self.unit_value

    def __repr__(self):
        return f"Item({self.name}, w:{self.weight}, v:{self.value:.1f}, ratio:{self.ratio:.2f})"

    def __str__(self):
        return f"{self.name} (W:{self.weight}, V:{self.value:.1f})"

    def take_fraction(self, fraction: float):
        """Take a fraction (0 < fraction <= 1) of this item.
        Subtracts integer weight and proportional value.
        Returns a dict representing the taken portion.
        """
        if fraction is None or fraction <= 0:
            return None
        if self.weight <= 0:
            return None
        
        fraction = min(1.0, max(0.0, fraction))
        
        amount_to_take = int(round(self.weight * fraction))
        if amount_to_take <= 0:
            return None
        if amount_to_take > self.weight:
            amount_to_take = self.weight
        
        taken_value = amount_to_take * self.unit_value
        
        taken_item = {
            "name": self.name,
            "weight": amount_to_take,
            "value": taken_value,
            "image_filename": self.image_filename,
        }
        
        self.weight -= amount_to_take
        self.value -= taken_value
        
        if self.weight < 0:
            self.weight = 0
        if self.value < 0:
            self.value = 0.0
        
        return taken_item

    def is_depleted(self):
        """Item is gone when weight is exactly zero."""
        return self.weight == 0