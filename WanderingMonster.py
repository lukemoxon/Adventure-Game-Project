"""
WanderingMonster.py

Defines the WanderingMonster class for use in the adventure game.
Monsters wander the 10x10 map, avoid forbidden squares, and can
be serialized to/from JSON-safe dictionaries.

Author: Luke Moxon
"""

import random


# Monster templates for random spawning
MONSTER_TEMPLATES = [
    {
        "monster_type": "Goblin",
        "color": [0, 200, 0],
        "hp_range": (5, 15),
        "power_range": (2, 6),
        "money_range": (10, 50),
        "description": "A sneaky goblin rushes at you."
    },
    {
        "monster_type": "Vulture",
        "color": [200, 200, 0],
        "hp_range": (1, 3),
        "power_range": (1, 2),
        "money_range": (100, 1500),
        "description": "A vulture guards treasure."
    },
    {
        "monster_type": "Troll",
        "color": [180, 0, 0],
        "hp_range": (20, 35),
        "power_range": (5, 10),
        "money_range": (50, 200),
        "description": "A massive troll blocks your path."
    }
]


class WanderingMonster:
    """
    Represents a wandering monster on the game map.

    Attributes:
        x (int): Grid x coordinate.
        y (int): Grid y coordinate.
        monster_type (str): Type name of the monster.
        color (list): RGB color as [r, g, b].
        hp (int): Current hit points.
        power (int): Attack power.
        money (int): Gold dropped on defeat.
        description (str): Flavor text shown during combat.
    """

    def __init__(self, x, y, monster_type, color, hp,
                 power=3, money=20, description="A monster appears!"):
        """
        Initialize a WanderingMonster.

        Parameters:
            x (int): Grid x coordinate.
            y (int): Grid y coordinate.
            monster_type (str): Type of monster.
            color (list or tuple): RGB color [r, g, b].
            hp (int): Hit points.
            power (int): Attack power.
            money (int): Gold on defeat.
            description (str): Combat flavor text.
        """
        self.x = x
        self.y = y
        self.monster_type = monster_type
        self.color = list(color)
        self.hp = hp
        self.power = power
        self.money = money
        self.description = description

    # -------------------------------------------------
    # Class method: random_spawn
    # -------------------------------------------------
    @classmethod
    def random_spawn(cls, occupied, forbidden, grid_w=10, grid_h=10):
        """
        Create a WanderingMonster at a random valid location.

        Parameters:
            occupied (list): List of (x, y) tuples of other monster positions.
            forbidden (list): List of (x, y) tuples of forbidden positions
                              (e.g., town, player location).
            grid_w (int): Grid width (default 10).
            grid_h (int): Grid height (default 10).

        Returns:
            WanderingMonster: A new monster at a valid position.
        """
        blocked = set(tuple(p) for p in occupied) | set(tuple(p) for p in forbidden)

        while True:
            x = random.randint(0, grid_w - 1)
            y = random.randint(0, grid_h - 1)
            if (x, y) not in blocked:
                break

        template = random.choice(MONSTER_TEMPLATES)
        return cls(
            x=x,
            y=y,
            monster_type=template["monster_type"],
            color=template["color"],
            hp=random.randint(*template["hp_range"]),
            power=random.randint(*template["power_range"]),
            money=random.randint(*template["money_range"]),
            description=template["description"]
        )

    # -------------------------------------------------
    # Class method: from_dict
    # -------------------------------------------------
    @classmethod
    def from_dict(cls, data):
        """
        Reconstruct a WanderingMonster from a JSON-safe dictionary.

        Parameters:
            data (dict): Dictionary with monster fields.

        Returns:
            WanderingMonster: Reconstructed monster object.
        """
        return cls(
            x=data["x"],
            y=data["y"],
            monster_type=data["monster_type"],
            color=data["color"],
            hp=data["hp"],
            power=data["power"],
            money=data["money"],
            description=data["description"]
        )

    # -------------------------------------------------
    # Instance method: to_dict
    # -------------------------------------------------
    def to_dict(self):
        """
        Convert the monster to a JSON-safe dictionary.

        Returns:
            dict: All monster fields as JSON-safe primitives.
        """
        return {
            "x": self.x,
            "y": self.y,
            "monster_type": self.monster_type,
            "color": self.color,
            "hp": self.hp,
            "power": self.power,
            "money": self.money,
            "description": self.description
        }

    # -------------------------------------------------
    # Instance method: move
    # -------------------------------------------------
    def move(self, occupied, forbidden, grid_w=10, grid_h=10):
        """
        Attempt to move the monster one step in a random direction.
        Stays put if all directions are blocked or out of bounds.

        Parameters:
            occupied (list): List of (x, y) tuples of other monster positions.
            forbidden (list): List of (x, y) tuples of forbidden positions
                              (player pos, town pos, etc.).
            grid_w (int): Grid width.
            grid_h (int): Grid height.
        """
        blocked = set(tuple(p) for p in occupied) | set(tuple(p) for p in forbidden)

        directions = [
            (0, -1),  # up
            (0, 1),   # down
            (-1, 0),  # left
            (1, 0),   # right
        ]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < grid_w and 0 <= ny < grid_h:
                if (nx, ny) not in blocked:
                    self.x = nx
                    self.y = ny
                    return
        # No valid move found — stay put
