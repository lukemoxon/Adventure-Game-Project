"""
gamefunctions.py

Provides utility functions for a simple adventure game.
Includes functionality for purchasing items, generating
random monsters, printing a welcome message, and displaying
a formatted shop menu.

This module is designed to be imported into another file
(e.g., game.py) and reused.

Author: Luke Moxon
"""

import random


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


if __name__ == "__main__":
    test_functions()
