import random
import json
import gamefunctions
from WanderingMonster import WanderingMonster
from combat import run_combat


# ---------------------------
def print_welcome(name):
    """Print welcome message."""
    print(f"\nWelcome, {name}!")


# ---------------------------
def save_game(state):
    """Save game state to JSON file. Converts monsters to dicts."""
    filename = input("Enter save file name: ")
    save_data = {
        "name": state["name"],
        "hp": state["hp"],
        "gold": state["gold"],
        "inventory": state["inventory"],
        "map_state": state["map_state"],
        "monsters": [m.to_dict() for m in state["monsters"]]
    }
    with open(filename, "w") as file:
        json.dump(save_data, file)
    print("Game saved!")


def load_game():
    """Load game state from JSON file. Reconstructs WanderingMonster objects."""
    filename = input("Enter save file name: ")
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        data["monsters"] = [WanderingMonster.from_dict(m) for m in data["monsters"]]
        print("Game loaded!")
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
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
def _spawn_initial_monster(state):
    """Spawn one monster avoiding town and player."""
    map_state = state["map_state"]
    forbidden = [
        tuple(map_state["town_pos"]),
        tuple(map_state["player_pos"])
    ]
    occupied = [(m.x, m.y) for m in state["monsters"]]
    m = WanderingMonster.random_spawn(occupied, forbidden)
    state["monsters"].append(m)


def _ensure_monsters(state):
    """If no monsters remain, spawn two new ones."""
    if len(state["monsters"]) == 0:
        print("The map is clear! New monsters appear...")
        for _ in range(2):
            _spawn_initial_monster(state)


# ---------------------------
def explore(state):
    """
    Run the map interface with wandering monsters.
    """
    map_state = state["map_state"]

    # Place player at town when entering explore
    map_state["player_pos"] = list(map_state["town_pos"])

    # Ensure at least one monster exists
    _ensure_monsters(state)

    while True:
        result, encountered_monster = gamefunctions.run_map_interface(state)

        if result == "town":
            print("You're back in town.")
            return

        elif result == "monster" and encountered_monster is not None:
            outcome = run_combat(state, encountered_monster)

            if outcome == "won":
                state["monsters"] = [
                    m for m in state["monsters"]
                    if not (m.x == encountered_monster.x and m.y == encountered_monster.y)
                ]
                print("The monster has been defeated.")
                _ensure_monsters(state)
                input("Press Enter to return to map...")

            elif outcome == "fled":
                input("Press Enter to return to map...")

            elif outcome == "lost":
                print("You wake up back in town...")
                state["hp"] = 30
                map_state["player_pos"] = list(map_state["town_pos"])
                return


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
        map_state = gamefunctions.new_map_state()
        state = {
            "name": name,
            "hp": 30,
            "gold": 100,
            "inventory": [],
            "map_state": map_state,
            "monsters": []
        }
        _spawn_initial_monster(state)

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
