import random
import json

# ---------------------------
def print_welcome(name):
    """Print welcome message."""
    print(f"\nWelcome, {name}!")

def random_monster():
    """Return a random monster."""
    return random.choice(["Goblin", "Orc", "Troll"])

# ---------------------------
def save_game(state):
    """Save game state to JSON file."""
    filename = input("Enter save file name: ")
    with open(filename, "w") as file:
        json.dump(state, file)
    print("Game saved!")

def load_game():
    """Load game state from JSON file."""
    filename = input("Enter save file name: ")
    try:
        with open(filename, "r") as file:
            state = json.load(file)
        print("Game loaded!")
        return state
    except:
        print("Error loading file.")
        return None

# ---------------------------
def buy_item(state):
    """Buy items and add to inventory."""
    print("\nShop:")
    print("1) Sword (50 gold)")
    print("2) Potion (30 gold)")

    choice = input("Choose item: ")

    if choice == "1" and state["gold"] >= 50:
        state["gold"] -= 50
        state["inventory"].append({
            "name": "Sword",
            "type": "weapon",
            "damage": 5,
            "durability": 5,
            "equipped": False
        })
        print("You bought a sword!")

    elif choice == "2" and state["gold"] >= 30:
        state["gold"] -= 30
        state["inventory"].append({
            "name": "Potion",
            "type": "special"
        })
        print("You bought a potion!")

    else:
        print("Invalid choice or not enough gold.")

# ---------------------------
def equip_weapon(state):
    """Equip a weapon from inventory."""
    weapons = [i for i in state["inventory"] if i["type"] == "weapon"]

    if not weapons:
        print("No weapons available.")
        return

    print("\nWeapons:")
    for i, w in enumerate(weapons):
        print(f"{i+1}) {w['name']} (Durability: {w['durability']})")

    choice = input("Choose weapon: ")

    if choice.isdigit() and 1 <= int(choice) <= len(weapons):
        for w in weapons:
            w["equipped"] = False
        weapons[int(choice)-1]["equipped"] = True
        print("Weapon equipped!")

# ---------------------------
def fight(state):
    """Combat loop."""
    monster = random_monster()
    monster_hp = 15

    print(f"\nA {monster} appears!")

    while state["hp"] > 0 and monster_hp > 0:
        print(f"Your HP: {state['hp']} | Monster HP: {monster_hp}")

        # Special item check
        for item in state["inventory"]:
            if item["type"] == "special":
                use = input("Use potion to win instantly? (y/n): ")
                if use == "y":
                    print("Monster defeated instantly!")
                    state["inventory"].remove(item)
                    state["gold"] += 10
                    return

        action = input("1) Attack  2) Run: ")

        if action == "1":
            damage = 3

            # Weapon bonus
            for item in state["inventory"]:
                if item.get("equipped"):
                    damage += item["damage"]
                    item["durability"] -= 1
                    print("Weapon used!")

                    if item["durability"] <= 0:
                        print("Your weapon broke!")
                        state["inventory"].remove(item)

            monster_hp -= damage
            state["hp"] -= 2

        elif action == "2":
            print("You ran away!")
            return

    if state["hp"] <= 0:
        print("You lost...")
    else:
        print("You won!")
        state["gold"] += 10

# ---------------------------
def main():
    """Main game loop."""

    print("1) New Game")
    print("2) Load Game")
    start = input("Choose: ")

    if start == "2":
        state = load_game()
        if state is None:
            return
    else:
        name = input("Enter your name: ")
        print_welcome(name)
        state = {
            "name": name,
            "hp": 30,
            "gold": 100,
            "inventory": []
        }

    while True:
        print(f"\nHP: {state['hp']} | Gold: {state['gold']}")
        print("1) Fight")
        print("2) Sleep (restore HP for 5 gold)")
        print("3) Shop")
        print("4) Equip Weapon")
        print("5) Save and Quit")

        choice = input("Choose: ")

        if choice == "1":
            fight(state)
        elif choice == "2":
            if state["gold"] >= 5:
                state["hp"] = 30
                state["gold"] -= 5
                print("You feel rested!")
            else:
                print("Not enough gold.")
        elif choice == "3":
            buy_item(state)
        elif choice == "4":
            equip_weapon(state)
        elif choice == "5":
            save_game(state)
            print("Goodbye!")
            break
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()
