import gamefunctions
import random

def main():
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)

    player_hp = 30
    player_gold = 10

    while True:
        print("\nYou are in town.")
        print(f"HP: {player_hp} | Gold: {player_gold}")
        print("1) Fight Monster")
        print("2) Sleep (Restore HP for 5 gold)")
        print("3) Quit")

        choice = input("Choose (1-3): ")

        if choice == "1":
            player_hp, player_gold = fight(player_hp, player_gold)
        elif choice == "2":
            if player_gold >= 5:
                player_hp = 30
                player_gold -= 5
                print("You feel rested!")
            else:
                print("Not enough gold!")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

def fight(player_hp, player_gold):
    monster = gamefunctions.random_monster()
    monster_hp = 15

    while player_hp > 0 and monster_hp > 0:
        print(f"Your HP: {player_hp}, Monster HP: {monster_hp}")
        action = input("1) Attack 2) Run: ")

        if action == "1":
            player_hp -= 3
            monster_hp -= 5
        elif action == "2":
            print("You ran away!")
            break
        else:
            print("Invalid input")

    if player_hp <= 0:
        print("You lost!")
    elif monster_hp <= 0:
        print("You won!")
        player_gold += 5

    return player_hp, player_gold

if __name__ == "__main__":
    main()
