from clasa import ClassStats, Knight, Rogue, Monster, Loot, PlayerInventory, LootPopup, play_loot_sound, Dungeon
from PyQt5.QtWidgets import QApplication
import sys
import time
import random


def display_loot_popup(loot):
    """Display a popup for the loot drop."""
    app = QApplication.instance() or QApplication(sys.argv)
    popup = LootPopup(loot)
    popup.exec_()


def adventure(knight, rogue):
    while True:  # Loop for restarting the game if the player chooses to respawn
        user_input = input("Please enter your class (Knight/Rogue): ").lower()
        selected_class = ClassStats.is_class_valid(user_input)

        # Assign selected class
        if selected_class == knight.ClassName.lower():
            player = knight
        elif selected_class == rogue.ClassName.lower():
            player = rogue
        else:
            print("Error in class selection!")
            return  # Exit if the class is not valid

        # Ask for dungeon difficulty
        dungeon_mode = input("Select dungeon difficulty (Easy/Hard): ").lower()
        while dungeon_mode not in ["easy", "hard"]:
            print("Invalid choice! Please select 'Easy' or 'Hard'.")
            dungeon_mode = input("Select dungeon difficulty (Easy/Hard): ").lower()

        print(f"{player.ClassName} - Stats: HP={player.HP}, Stamina={player.Stamina}, AP={player.AP}, Def={player.Def}")
        print(f"You have chosen '{dungeon_mode.title()}' difficulty.\n")

        # Create player inventory
        player_inventory = PlayerInventory()

        # Start Adventure
        agree = input("Would you like to begin your adventure? (Y/N): ").upper()
        if agree in {"Y", "YES"}:
            print("Generating world, please wait...")
            time.sleep(2)
            result = start_adventure(player, player_inventory, player, dungeon_mode)  # Start adventure
            if result == "exit":  # If the game is done, exit the loop
                print("Game over.")
                break  # Exit the main loop and quit the game
        else:
            print("The game will quit now. See you next time, adventurer!")
            break  # Exit the main loop and quit the game


def start_adventure(player, player_inventory, original_player, dungeon_mode):
    print("Your adventure begins!")
    time.sleep(1)

    # Monster pool
    monsters = [
        Monster("Wolf", 100, 20, 10, 5),
        Monster("Goblin", 150, 25, 15, 8),
        Monster("Orc", 300, 50, 25, 15),
        Monster("Boss Demon", 300, 75, 50, 100),  # Boss enemy
    ]

    maps = ["Howling Abyss", "Piltover Plain", "Noxus Camp"]

    # Randomly choose a map
    map_name = random.choice(maps)
    time.sleep(2)  # Simulating world generation time
    print(f"Entering {map_name}...")  # Display the map
    time.sleep(1)  # Delay before starting the adventure

    # Create a Dungeon
    dungeon = Dungeon(mode=dungeon_mode)

    while player.HP > 0:
        # Encounter a random monster
        monster = random.choice(monsters)
        print(f"A wild {monster.Name} appears! Prepare for battle.")
        monster.adjust_for_difficulty(dungeon.mode)  # Adjust monster stats based on dungeon difficulty

        # Combat loop
        combat_result = combat(player, monster, player_inventory)

        # If the player conceded, continue to the next monster
        if combat_result == "concede":
            print("You have fled from battle. A new monster awaits!")
            continue  # Restart the loop to encounter a new monster

        # If the player is still alive and defeated the monster, heal the player
        if player.HP > 0:
            heal_player(player, monster)
            decision = input("Would you like to continue the adventure and face another monster? (Y/N): ").upper()
            if decision == "N":
                print("Thank you for playing! Farewell, adventurer.")
                return "exit"  # Signal to exit the main loop
        else:
            break  # Exit if HP is 0

    # Handle player death (respawn or quit)
    if player.HP <= 0:
        respawn_decision = input("Would you like to respawn and start over? (Y/N): ").upper()
        if respawn_decision == "Y":
            print("Respawning...")
            result = reset_game(original_player, player_inventory)  # Respawn the player
            if result == "restart":
                return "restart"  # Signal to restart adventure
        else:
            print("Thank you for playing! Game over.")  # Exit the game gracefully
            return "exit"  # Signal to exit the main loop

    return "exit"  # Return exit if the game ends


def heal_player(player, monster):
    """Heal the player after defeating a monster based on their base health."""
    # Determine the healing percentage
    if monster.Name == "Boss Demon":
        heal_chance = random.choices([25, 50, 75, 100], weights=[30, 30, 30, 10])[0]  # Higher chance for full heal
    else:
        heal_chance = random.choices([25, 50, 75], weights=[40, 40, 20])[0]

    # Calculate heal amount based on the player's BaseHP
    heal_amount = int(player.BaseHP * (heal_chance / 100))
    player.HP = min(player.HP + heal_amount, player.BaseHP)  # Cap HP at the BaseHP value
    print(f"After defeating the {monster.Name}, you are healed for {heal_chance}% ({heal_amount} HP).")
    print(f"Current HP: {player.HP}/{player.BaseHP}")


def combat(player, monster, player_inventory):
    while player.HP > 0 and monster.HP > 0:
        print(f"{player.ClassName}: HP={player.HP}, {monster.Name}: HP={monster.HP}")

        # Player's turn
        action = input("Choose your action: [1] Attack, [2] Defend, [3] Concede: ")

        if action == "1":  # Attack
            damage = max(1, player.AP - monster.Def + random.randint(-5, 5))
            damage = max(damage, int(player.AP * 0.1))  # Ensure that minimum damage is 10% of AP
            crit_chance = getattr(player, "CritRate", 20)
            if random.randint(1, 100) <= crit_chance:
                damage *= 2
                print("Critical hit!")
            monster.HP -= damage
            print(f"You attack the {monster.Name} for {damage} damage!")
        elif action == "2":  # Defend
            print("You defend!")
            continue
        elif action == "3":  # Concede (Flee from battle)
            print(f"You flee from the {monster.Name}!")
            return "concede"  # Signal to concede and choose a new monster
        else:
            print("Invalid action! Please choose [1] Attack, [2] Defend, or [3] Concede.")
            continue

        # Check if the monster is still alive before it retaliates
        if monster.HP > 0:
            # Monster's turn
            monster_damage = max(1, monster.AP - player.Def + random.randint(-5, 5))
            if random.randint(1, 100) <= 10:  # Monster crit chance
                monster_damage *= 2
                print(f"The {monster.Name} lands a critical hit!")
            player.HP -= monster_damage
            print(f"The {monster.Name} attacks you for {monster_damage} damage!")

    # End combat
    if player.HP > 0:
        print(f"You defeated the {monster.Name}!")
        loot = Loot.drop_loot(monster.Name == "Boss Demon")
        player_inventory.add_item(loot)

        # Ask player if they want to equip the loot
        equip_decision = input(f"Do you want to equip the new {loot['name']}? (Y/N): ").upper()
        if equip_decision == "Y":
            # Pass player to equip_item to modify their stats
            player_inventory.equip_item(loot, player)

        # Play loot sound and show loot popup
        play_loot_sound()
        display_loot_popup(loot)

        print("\nCurrent Inventory:")
        player_inventory.display()
    else:
        print("You were defeated. Game over.")


def reset_game(player, player_inventory):
    # Reset player stats
    player_inventory.inventory.clear()
    if isinstance(player, Knight):
        player.BaseHP = 500  # Reset BaseHP
        player.HP = player.BaseHP  # Set HP to BaseHP
        player.Stamina, player.AP, player.Def = 100, 50, 50
    elif isinstance(player, Rogue):
        player.BaseHP = 250  # Reset BaseHP
        player.HP = player.BaseHP  # Set HP to BaseHP
        player.Stamina, player.AP, player.Def = 150, 100, 25

    # Restart adventure but return control to the caller
    return "restart"  # This signals that the game should be restarted


if __name__ == "__main__":
    print("RPG GAME TEST")
    knight = Knight("Knight", 500, 100, 50, 50, "Order of the Sword")
    rogue = Rogue("Rogue", 250, 150, 100, 25, "100% Crit")
    adventure(knight, rogue)