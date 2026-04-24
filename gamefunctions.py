"""
gamefunctions.py

Provides utility functions for a simple adventure game.
Includes functionality for purchasing items, generating
random monsters, printing a welcome message, displaying
a formatted shop menu, and a text-based map interface.

Author: Luke Moxon
"""

import random
import os


# -------------------------------------------------
# Function: purchase_item
# -------------------------------------------------
def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """
    Attempts to purchase a specified quantity of an item.

    Parameters:
        itemPrice (int): Price of one item.
        startingMoney (int): Amount of money available.
        quantityToPurchase (int, optional): Number of items
            requested (default is 1).

    Returns:
        tuple:
            quantity_purchased (int): Number of items bought.
            remaining_money (int): Money left after purchase.
    """
    max_affordable = startingMoney // itemPrice
    quantity_purchased = min(quantityToPurchase, max_affordable)
    remaining_money = startingMoney - (quantity_purchased * itemPrice)

    return quantity_purchased, remaining_money


# -------------------------------------------------
# Function: random_monster
# -------------------------------------------------
def random_monster():
    """
    Generates a random monster dict with randomized stats.

    Returns:
        dict: name, description, health, power, money
    """
    monsters = [
        {
            "name": "Goblin",
            "description": "A sneaky goblin rushes at you.",
            "health_range": (5, 15),
            "power_range": (2, 6),
            "money_range": (10, 50)
        },
        {
            "name": "Vulture",
            "description": "A vulture guards treasure.",
            "health_range": (1, 3),
            "power_range": (1, 2),
            "money_range": (100, 1500)
        },
        {
            "name": "Troll",
            "description": "A massive troll blocks your path.",
            "health_range": (20, 35),
            "power_range": (5, 10),
            "money_range": (50, 200)
        }
    ]

    template = random.choice(monsters)

    return {
        "name": template["name"],
        "description": template["description"],
        "health": random.randint(*template["health_range"]),
        "power": random.randint(*template["power_range"]),
        "money": random.randint(*template["money_range"])
    }


# -------------------------------------------------
# Function: print_welcome
# -------------------------------------------------
def print_welcome(name, width=30):
    """
    Prints a centered welcome message.

    Parameters:
        name (str): The player's name.
        width (int): Width of the printed line.
    """
    message = f"Hello, {name}!"
    print(message.center(width))


# -------------------------------------------------
# Function: print_shop_menu
# -------------------------------------------------
def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Prints a formatted shop menu displaying two items.
    """
    p1 = f"${item1Price:.2f}"
    p2 = f"${item2Price:.2f}"

    print("/----------------------\\")
    print(f"| {item1Name:<12}{p1:>8} |")
    print(f"| {item2Name:<12}{p2:>8} |")
    print("\\----------------------/")


# -------------------------------------------------
# Function: new_map_state
# -------------------------------------------------
def new_map_state():
    """
    Creates and returns a fresh map state dictionary.

    The map is a 10x10 grid. Town is at (0, 0).
    Monsters are stored separately in state["monsters"].

    Returns:
        dict: map_state with player_pos and town_pos.
    """
    return {
        "player_pos": [0, 0],
        "town_pos": [0, 0],
    }


# -------------------------------------------------
# Helper: _random_unoccupied
# -------------------------------------------------
def _random_unoccupied(occupied, town_pos):
    """
    Returns a random [x, y] on the 10x10 grid not in occupied.
    """
    while True:
        pos = [random.randint(0, 9), random.randint(0, 9)]
        if tuple(pos) not in [tuple(o) for o in occupied]:
            return pos


# -------------------------------------------------
# Function: move_player
# -------------------------------------------------
def move_player(map_state, direction):
    """
    Moves the player one grid space in the given direction.

    Parameters:
        map_state (dict): Current map state (modified in place).
        direction (str): One of 'up', 'down', 'left', 'right'.

    Returns:
        str: "moved", "returned_to_town"
    """
    x, y = map_state["player_pos"]

    if direction == "up":
        y = max(0, y - 1)
    elif direction == "down":
        y = min(9, y + 1)
    elif direction == "left":
        x = max(0, x - 1)
    elif direction == "right":
        x = min(9, x + 1)

    was_at_town = (map_state["player_pos"] == list(map_state["town_pos"]))
    map_state["player_pos"] = [x, y]

    if [x, y] == list(map_state["town_pos"]) and not was_at_town:
        return "returned_to_town"
    else:
        return "moved"


# -------------------------------------------------
# Function: draw_map
# -------------------------------------------------
def draw_map(state):
    """
    Prints the current 10x10 text map to the terminal.
    Reads monsters from state["monsters"] (list of WanderingMonster objects).

    Symbols:
        P = player
        T = town square
        M = monster
        . = empty square

    Parameters:
        state (dict): Full game state including map_state and monsters.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n  === WORLD MAP ===")
    print("  Controls: w=up  s=down  a=left  d=right  q=quit to town\n")

    map_state = state["map_state"]
    player = map_state["player_pos"]
    town = list(map_state["town_pos"])

    # Build set of monster positions for quick lookup
    monster_positions = set()
    for m in state.get("monsters", []):
        monster_positions.add((m.x, m.y))

    for row in range(10):
        line = "  "
        for col in range(10):
            pos = [col, row]
            if pos == player:
                line += "P"
            elif pos == town:
                line += "T"
            elif (col, row) in monster_positions:
                line += "M"
            else:
                line += "."
        print(line)
    print()


# -------------------------------------------------
# Function: run_map_interface
# -------------------------------------------------
def run_map_interface(state):
    """
    Runs the text-based map interface loop.

    Each keypress:
      1. Moves the player
      2. Checks for monster collision -> returns "monster" + which monster
      3. Moves all monsters
      4. Redraws map

    Parameters:
        state (dict): Full game state (modified in place).

    Returns:
        tuple: ("town", None) or ("monster", WanderingMonster)
    """
    from WanderingMonster import WanderingMonster

    direction_map = {
        "w": "up",
        "s": "down",
        "a": "left",
        "d": "right"
    }

    map_state = state["map_state"]

    while True:
        draw_map(state)

        key = input("Move: ").strip().lower()

        if key == "q":
            map_state["player_pos"] = list(map_state["town_pos"])
            return "town", None

        if key not in direction_map:
            continue

        # 1. Move player
        result = move_player(map_state, direction_map[key])

        if result == "returned_to_town":
            draw_map(state)
            print("You returned to town!")
            input("Press Enter to continue...")
            return "town", None

        # 2. Check if player landed on a monster (BEFORE monsters move)
        px, py = map_state["player_pos"]
        encountered = None
        for m in state["monsters"]:
            if m.x == px and m.y == py:
                encountered = m
                break

        if encountered is not None:
            draw_map(state)
            print(f"A {encountered.monster_type} blocks your path!")
            input("Press Enter to fight...")
            return "monster", encountered

        # 3. Move all monsters
        town_pos = tuple(map_state["town_pos"])
        player_pos = tuple(map_state["player_pos"])
        for i, m in enumerate(state["monsters"]):
            # Other monster positions (exclude self)
            other_monsters = [(om.x, om.y) for j, om in enumerate(state["monsters"]) if j != i]
            forbidden = [town_pos, player_pos]
            m.move(other_monsters, forbidden)

        # 4. Check again if any monster walked into the player
        for m in state["monsters"]:
            if m.x == px and m.y == py:
                draw_map(state)
                print(f"A {m.monster_type} found you!")
                input("Press Enter to fight...")
                return "monster", m


# -------------------------------------------------
# Test Function
# -------------------------------------------------
def test_functions():
    """Run basic tests for all functions."""

    print("Testing purchase_item()")
    print(purchase_item(123, 1000, 3))
    print(purchase_item(123, 201, 3))
    print(purchase_item(341, 2112))

    print("\nTesting random_monster()")
    for _ in range(3):
        print(random_monster())

    print("\nTesting print_welcome()")
    print_welcome("Jeff", 20)
    print_welcome("Audrey", 30)
    print_welcome("Luke", 25)

    print("\nTesting print_shop_menu()")
    print_shop_menu("Apple", 31, "Pear", 1.23)
    print_shop_menu("Sword", 199.9, "Shield", 85)

    print("\nTesting new_map_state()")
    ms = new_map_state()
    print(ms)

    print("\nTesting move_player()")
    print(move_player(ms, "down"))
    print(ms["player_pos"])


if __name__ == "__main__":
    test_functions()
