import gamefunctions

def main():
    # Get player name
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)

    # Initialize player gold and inventory
    gold = 100
    inventory = []
    print(f"\nYou start with {gold} gold.\n")

    # Show shop
    gamefunctions.print_shop_menu()
    choice = input("Choose item (1 = Sword, 2 = Shield, 3 = Potion): ")

    # Purchase item
    items = ["Sword", "Shield", "Potion"]
    if choice in ["1", "2", "3"]:
        item_index = int(choice) - 1
        gamefunctions.purchase_item(items[item_index], inventory)
    else:
        print("Invalid choice.")

    print(f"Your inventory: {inventory}")

    # Encounter a monster
    monster = gamefunctions.random_monster()
    print("\nA monster appears!")
    print(f"{monster} attacks!")

if __name__ == "__main__":
    main()