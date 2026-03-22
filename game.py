import gamefunctions


def main():
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name, 30)

    gold = 100
    print(f"\nYou start with {gold} gold.\n")

    # Show shop
    gamefunctions.print_shop_menu("Sword", 50, "Shield", 40)

    choice = input("Choose item (1 = Sword, 2 = Shield): ")

    if choice == "1":
        qty, gold = gamefunctions.purchase_item(50, gold, 1)
    elif choice == "2":
        qty, gold = gamefunctions.purchase_item(40, gold, 1)
    else:
        print("Invalid choice.")
        qty = 0

    print(f"You bought {qty} item(s). Gold left: {gold}")

    # Encounter monster
    monster = gamefunctions.random_monster()
    print("\nA monster appears!")
    print(monster["name"])
    print(monster["description"])
    print(f"Health: {monster['health']}")
    print(f"Power: {monster['power']}")
    print(f"Gold drop: {monster['money']}")


if __name__ == "__main__":
    main()
