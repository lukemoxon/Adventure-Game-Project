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
    Generates a random monster with randomized stats.

    Parameters:
        None

    Returns:
        dict: A dictionary containing:
            name (str)
            description (str)
            health (int)
            power (int)
            money (int)
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
def print_welcome(name, width):
    """
    Prints a centered welcome message.

    Parameters:
        name (str): The player's name.
        width (int): Width of the printed line.

    Returns:
        None
    """
    message = f"Hello, {name}!"
    print(message.center(width))


# -------------------------------------------------
# Function: print_shop_menu
# -------------------------------------------------
def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Prints a formatted shop menu displaying two items.

    Parameters:
        item1Name (str): Name of first item.
        item1Price (float): Price of first item.
        item2Name (str): Name of second item.
        item2Price (float): Price of second item.

    Returns:
        None
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

    The map is a 10x10 grid.
    Town is at (0, 0) (upper-left).
    Monster starts at a random location that is not the town.

    Returns:
        dict: map_state with keys:
            player_pos (list): [x, y] player position.
            town_pos (tuple): (x, y) of the town square.
            monster_pos (list): [x, y] of the monster square.
    """
    town_pos = (0, 0)
    monster_pos = _random_unoccupied([town_pos], town_pos)
    return {
        "player_pos": [0, 0],
        "town_pos": town_pos,
        "monster_pos": monster_pos
    }


# -------------------------------------------------
# Helper: _random_unoccupied
# -------------------------------------------------
def _random_unoccupied(occupied, town_pos):
    """
    Returns a random [x, y] position on the 10x10 grid
    that is not in the occupied list.

    Parameters:
        occupied (list): List of (x, y) tuples already taken.
        town_pos (tuple): Town position to also exclude.

    Returns:
        list: [x, y]
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
    Moves the player one grid space in the given direction,
    enforcing 10x10 grid boundaries.

    Parameters:
        map_state (dict): Current map state (modified in place).
        direction (str): One of 'up', 'down', 'left', 'right'.

    Returns:
        str: One of:
            "moved"             - normal movement
            "returned_to_town"  - player stepped onto town square
            "monster_encounter" - player stepped onto monster square
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

    # Only update if actually moved away from town first
    was_at_town = (map_state["player_pos"] == list(map_state["town_pos"]))
    map_state["player_pos"] = [x, y]

    if [x, y] == list(map_state["monster_pos"]):
        return "monster_encounter"
    elif [x, y] == list(map_state["town_pos"]) and not was_at_town:
        return "returned_to_town"
    else:
        return "moved"


# -------------------------------------------------
# Function: draw_map
# -------------------------------------------------
def draw_map(map_state):
    """
    Prints the current 10x10 text map to the terminal.

    Symbols:
        P = player
        T = town square
        M = monster square
        . = empty square

    Parameters:
        map_state (dict): Current map state.

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n  === WORLD MAP ===")
    print("  Controls: w=up  s=down  a=left  d=right  q=quit to town\n")

    player = map_state["player_pos"]
    town = list(map_state["town_pos"])
    monster = map_state["monster_pos"]

    for row in range(10):
        line = "  "
        for col in range(10):
            pos = [col, row]
            if pos == player:
                line += "P"
            elif pos == town:
                line += "T"
            elif pos == monster:
                line += "M"
            else:
                line += "."
        print(line)
    print()


# -------------------------------------------------
# Function: run_map_interface
# -------------------------------------------------
def run_map_interface(map_state):
    """
    Runs the text-based map interface loop.

    The player navigates using w/a/s/d keys.
    The loop ends when the player returns to town,
    encounters a monster, or presses 'q'.

    Parameters:
        map_state (dict): Current map state (modified in place).

    Returns:
        str: "town" if player returned to town or quit,
             "monster" if player encountered a monster.
    """
    direction_map = {
        "w": "up",
        "s": "down",
        "a": "left",
        "d": "right"
    }

    while True:
        draw_map(map_state)

        key = input("Move: ").strip().lower()

        if key == "q":
            print("Returning to town...")
            map_state["player_pos"] = list(map_state["town_pos"])
            return "town"

        if key not in direction_map:
            continue

        result = move_player(map_state, direction_map[key])

        if result == "returned_to_town":
            draw_map(map_state)
            print("You returned to town!")
            input("Press Enter to continue...")
            return "town"

        elif result == "monster_encounter":
            draw_map(map_state)
            print("A monster is here!")
            input("Press Enter to fight...")
            return "monster"


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

    print("\nTesting draw_map()")
    draw_map(ms)


if __name__ == "__main__":
    test_functions()
