import random
import json
import gamefunctions


# ---------------------------
def print_welcome(name):
    """Print welcome message."""
    print(f"\nWelcome, {name}!")


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
def fight(state, monster=None):
    """
    Combat loop.

    Parameters:
        state (dict): Game state.
        monster (dict, optional): A monster dict from gamefunctions.random_monster().
                                  If None, generates a new one.

    Returns:
        str: "won", "lost", or "fled"
    """
    if monster is None:
        monster = gamefunctions.random_monster()

    monster_hp = monster["health"]
    monster_name = monster["name"]

    print(f"\n{monster['description']}")
    print(f"A {monster_name} appears! (HP: {monster_hp}, Power: {monster['power']})")

    while state["hp"] > 0 and monster_hp > 0:
        print(f"\nYour HP: {state['hp']} | {monster_name} HP: {monster_hp}")

        # Special item check
        for item in state["inventory"]:
            if item["type"] == "special":
                use = input("Use potion to win instantly? (y/n): ")
                if use == "y":
                    print("Monster defeated instantly!")
                    state["inventory"].remove(item)
                    state["gold"] += monster["money"]
                    return "won"

        action = input("1) Attack  2) Run: ")

        if action == "1":
            damage = 3

            # Weapon bonus
            for item in list(state["inventory"]):
                if item.get("equipped"):
                    damage += item["damage"]
                    item["durability"] -= 1
                    print("Weapon used!")
                    if item["durability"] <= 0:
                        print("Your weapon broke!")
                        state["inventory"].remove(item)

            monster_hp -= damage
            state["hp"] -= monster["power"]
            print(f"You dealt {damage} damage! Monster dealt {monster['power']} damage!")

        elif action == "2":
            print("You ran away!")
            return "fled"

    if state["hp"] <= 0:
        print("You lost...")
        return "lost"
    else:
        earned = monster["money"]
        print(f"You won! Earned {earned} gold.")
        state["gold"] += earned
        return "won"


# ---------------------------
def explore(state):
    """
    Run the map interface. Handle monster encounters and
    town returns. After combat, return to map at same spot
    with a new monster in a random unoccupied location.
    """
    # Initialize map state if not present
    if "map_state" not in state:
        state["map_state"] = gamefunctions.new_map_state()

    map_state = state["map_state"]

    # Place player at town when entering explore
    map_state["player_pos"] = list(map_state["town_pos"])

    while True:
        result = gamefunctions.run_map_interface(map_state)

        if result == "town":
            print("You're back in town.")
            return

        elif result == "monster":
            monster = gamefunctions.random_monster()
            outcome = fight(state, monster)

            if outcome == "lost":
                # Respawn player in town, reset map
                print("You wake up back in town...")
                state["hp"] = 30
                state["map_state"] = gamefunctions.new_map_state()
                return

            else:
                # Stay at monster location, place new monster elsewhere
                current_pos = map_state["player_pos"]
                occupied = [tuple(current_pos), tuple(map_state["town_pos"])]
                map_state["monster_pos"] = gamefunctions._random_unoccupied(
                    occupied, map_state["town_pos"]
                )
                print("The area is now safe. You may continue exploring.")
                input("Press Enter to return to map...")
                # Continue the while loop — player stays on map


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
            "inventory": [],
            "map_state": gamefunctions.new_map_state()
        }

    while True:
        if state["hp"] <= 0:
            print("You have died. Game over.")
            break

        print(f"\nHP: {state['hp']} | Gold: {state['gold']}")
        print("1) Explore")
        print("2) Sleep (restore HP for 5 gold)")
        print("3) Shop")
        print("4) Equip Weapon")
        print("5) Save and Quit")

        choice = input("Choose: ")

        if choice == "1":
            explore(state)
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
