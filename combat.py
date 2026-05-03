"""
combat.py

Text-based combat screen for the adventure game.
Displays combat info in the terminal with HP bars
and combat options.

Author: Luke Moxon
"""

# -------------------------
# Helper: draw_hp_bar
# -------------------------
def draw_hp_bar(current, max_hp, width=20):
    """Draw a text based HP bar."""
    ratio = max(0, current / max_hp)
    filled = int(width * ratio)
    empty = width - filled
    bar = "[" + "█" * filled + "░" * empty + "]"
    return f"{bar} {current}/{max_hp}"


# -------------------------
# Helper: draw_combat_scene
# -------------------------
def draw_combat_scene(state, monster, monster_hp, message):
    """Print the full combat screen in the terminal."""
    print("\n" + "=" * 40)
    print("          ⚔  COMBAT ⚔")
    print("=" * 40)
    print(f"\n  {state['name']:<15}  vs  {monster.monster_type}")
    print(f"  HP: {draw_hp_bar(state['hp'], 30)}")
    print(f"  {monster.monster_type} HP: {draw_hp_bar(monster_hp, monster.hp)}")
    print(f"\n  {message}")
    print("\n" + "-" * 40)
    print("  1) Attack")
    print("  2) Run")

    has_potion = any(i["type"] == "special" for i in state["inventory"])
    if has_potion:
        print("  3) Use Potion")
    print("-" * 40)


# -------------------------
# Helper: attack_animation
# -------------------------
def attack_animation(state, monster, monster_hp):
    """Print a simple text attack animation."""
    frames = [
        f"  {state['name']} steps forward...",
        f"  {state['name']} swings!",
        f"  ⚔  SLASH!  ⚔",
    ]
    import time
    for frame in frames:
        print(frame)
        time.sleep(0.4)


# -------------------------
# Main: run_combat
# -------------------------
def run_combat(state, wandering_monster):
    """
    Run the text based combat screen.

    Parameters:
        state (dict): Game state (hp, gold, inventory, name).
        wandering_monster (WanderingMonster): The monster being fought.

    Returns:
        str: "won", "lost", or "fled"
    """
    import time
    import os

    monster_hp = wandering_monster.hp
    message = f"A {wandering_monster.monster_type} appears! {wandering_monster.description}"

    while state["hp"] > 0 and monster_hp > 0:

        os.system('cls' if os.name == 'nt' else 'clear')
        draw_combat_scene(state, wandering_monster, monster_hp, message)

        choice = input("\n  Choose action: ").strip()

        # ---- ATTACK ----
        if choice == "1":
            damage = 3
            weapon_broke = False

            for item in list(state["inventory"]):
                if item.get("equipped"):
                    damage += item["damage"]
                    item["durability"] -= 1
                    if item["durability"] <= 0:
                        state["inventory"].remove(item)
                        weapon_broke = True

            attack_animation(state, wandering_monster, monster_hp)
            time.sleep(0.3)

            monster_hp -= damage
            state["hp"] -= wandering_monster.power

            if weapon_broke:
                message = f"Dealt {damage} damage! Your weapon broke!"
            else:
                message = (f"Dealt {damage} damage! "
                           f"{wandering_monster.monster_type} hit you "
                           f"for {wandering_monster.power}!")

        # ---- RUN ----
        elif choice == "2":
            print("\n  You ran away!")
            time.sleep(1)
            return "fled"

        # ---- POTION ----
        elif choice == "3":
            has_potion = any(
                i["type"] == "special" for i in state["inventory"]
            )
            if has_potion:
                for item in list(state["inventory"]):
                    if item["type"] == "special":
                        state["inventory"].remove(item)
                        break
                monster_hp = 0
                message = "Potion used! Monster defeated instantly!"
                os.system('cls' if os.name == 'nt' else 'clear')
                draw_combat_scene(state, wandering_monster, monster_hp, message)
                time.sleep(1.5)
                state["gold"] += wandering_monster.money
                return "won"
            else:
                message = "No potions available!"

        else:
            message = "Invalid choice!"

    # --- Combat over ---
    os.system('cls' if os.name == 'nt' else 'clear')

    if state["hp"] <= 0:
        draw_combat_scene(state, wandering_monster, monster_hp,
                          "You were defeated...")
        time.sleep(2)
        return "lost"
    else:
        earned = wandering_monster.money
        state["gold"] += earned
        draw_combat_scene(state, wandering_monster, monster_hp,
                          f"Victory! You earned {earned} gold!")
        time.sleep(2)
        return "won"
