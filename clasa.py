import random
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog
from PyQt5.QtGui import QPixmap
from pygame import mixer


class ClassStats:
    def __init__(self, ClassName, HP, Stamina, AP, Def):
        self.ClassName = ClassName
        self.HP = HP
        self.Stamina = Stamina
        self.AP = AP
        self.Def = Def

    @staticmethod
    def is_class_valid(ClassName):
        valid_classes = ["knight", "rogue"]
        ClassName = ClassName.lower()
        while ClassName not in valid_classes:
            print("This is not a valid class!")
            ClassName = input("Please select a valid class: ").lower()
        print(f"You have selected {ClassName.title()}")
        return ClassName


class Knight(ClassStats):
    def __init__(self, ClassName, HP, Stamina, AP, Def, Order):
        super().__init__(ClassName, HP, Stamina, AP, Def)
        self.BaseHP = HP  # Store the base HP as a constant reference
        self.Order = Order


class Rogue(ClassStats):
    def __init__(self, ClassName, HP, Stamina, AP, Def, Crit):
        super().__init__(ClassName, HP, Stamina, AP, Def)
        self.BaseHP = HP  # Store the base HP as a constant reference
        self.Crit = Crit


class Dungeon:
    def __init__(self, mode="easy"):
        self.mode = mode


class Monster:
    def __init__(self, Name, HP, AP, Def, EXP):
        self.Name = Name
        self.original_HP = HP  # Store the original HP for future reference
        self.HP = HP  # Set current HP based on original HP
        self.AP = AP
        self.Def = Def
        self.EXP = EXP

    def adjust_for_difficulty(self, difficulty):
        """Adjust the monster stats based on the dungeon difficulty."""
        if difficulty == "easy":
            self.HP = max(self.original_HP - random.randint(10, 30), 10)  # Prevent HP from going below 10
            self.AP = max(self.AP - random.randint(1, 5), 1)  # Prevent negative AP
            self.Def = max(self.Def - random.randint(1, 2), 1)  # Prevent negative Def
        elif difficulty == "hard":
            self.HP = self.original_HP + random.randint(20, 50)
            self.AP += random.randint(5, 10)
            self.Def += random.randint(2, 5)


class Loot:
    rarities = {
        "Common": 60,
        "Uncommon": 20,
        "Rare": 10,
        "Epic": 6,
        "Legendary": 3,
        "Relic": 1
    }

    items = {
        "Helmet": ["Common Helmet", "Uncommon Helmet", "Rare Helmet", "Epic Helmet", "Legendary Helmet", "Relic Helmet"],
        "Chest": ["Common Chest", "Uncommon Chest", "Rare Chest", "Epic Chest", "Legendary Chest", "Relic Chest"],
        "Pants": ["Common Pants", "Uncommon Pants", "Rare Pants", "Epic Pants", "Legendary Pants", "Relic Pants"],
        "Shoes": ["Common Shoes", "Uncommon Shoes", "Rare Shoes", "Epic Shoes", "Legendary Shoes", "Relic Shoes"],
        "Weapons": ["Common Sword", "Uncommon Bow", "Rare Dagger", "Epic Staff", "Legendary Sword", "Relic Blade"]
    }

    @classmethod
    def drop_loot(cls, is_boss):
        """Generate loot based on rarity."""
        rarity = random.choices(list(cls.rarities.keys()), weights=cls.rarities.values())[0]
        category = random.choice(list(cls.items.keys()))
        item = cls.items[category][list(cls.rarities.keys()).index(rarity)]
        return {"name": item, "rarity": rarity, "category": category}

    @staticmethod
    def get_stat_bonus(rarity, category):
        """Return the stat bonus for an item based on its rarity and category."""
        if category in ["Helmet", "Chest", "Pants", "Shoes"]:
            # Defensive gear (HP bonuses)
            hp_bonuses = {
                "Common": 5,
                "Uncommon": 10,
                "Rare": 25,
                "Epic": 50,
                "Legendary": 100,
                "Relic": 200
            }
            return hp_bonuses.get(rarity, 0)
        elif category == "Weapons":
            # Weapons (Attack Power bonuses)
            ap_bonuses = {
                "Common": 1,
                "Uncommon": 2,
                "Rare": 3,
                "Epic": 4,
                "Legendary": 5,
                "Relic": 6
            }
            return ap_bonuses.get(rarity, 0)
        return 0

    @staticmethod
    def get_rarity_color(rarity):
        """Return a color based on the rarity."""
        color_map = {
            "Common": "#FFFFFF",      # White for common items
            "Uncommon": "#00FF00",    # Green for uncommon items
            "Rare": "#0000FF",        # Blue for rare items
            "Epic": "#800080",        # Purple for epic items
            "Legendary": "#FFD700",   # Gold for legendary items
            "Relic": "#FF4500"        # Orange-Red for relic items
        }
        return color_map.get(rarity, "#FFFFFF")  # Default to white if rarity is unknown


class PlayerInventory:
    def __init__(self):
        self.inventory = []
        self.equipped = {
            "Helmet": None,
            "Chest": None,
            "Pants": None,
            "Shoes": None,
            "Weapons": None
        }

    def add_item(self, loot):
        """Add item to inventory."""
        self.inventory.append(loot)

    def equip_item(self, loot, player):
        """Equip item if possible and replace existing one if necessary."""
        category = loot["category"]
        if category in self.equipped:
            current_item = self.equipped[category]
            # Check if there is already an equipped item in the same category
            if current_item:
                print(f"You already have a {category.lower()} equipped: {current_item['name']}")
                swap_decision = input(f"Do you want to replace it with the new {loot['name']}? (Y/N): ").upper()
                if swap_decision == "Y":
                    self.inventory.append(current_item)  # Move old item to inventory
                    self.equipped[category] = loot  # Equip new item
                    print(f"Equipped {loot['name']} and replaced the old {current_item['name']}.")
                else:
                    print("You chose not to replace the item.")
            else:
                # No item equipped in this category
                self.equipped[category] = loot
                print(f"Equipped new {loot['name']}.")

            # Apply stat bonus based on rarity
            stat_bonus = Loot.get_stat_bonus(loot["rarity"], category)

            if category in ["Helmet", "Chest", "Pants", "Shoes"]:
                # Defensive gear (HP increase)
                print(f"Your HP has been increased by {stat_bonus} HP.")
                # Increase player's max HP (BaseHP)
                player.BaseHP += stat_bonus  # Increase BaseHP
                # If current HP is less than BaseHP, heal the player to max HP
                if player.HP < player.BaseHP:
                    player.HP = player.BaseHP
            elif category == "Weapons":
                # Weapons (AP increase)
                print(f"Your AP has been increased by {stat_bonus}.")
        else:
            print(f"Invalid category for equipment: {category}")

    def display(self):
        """Display all items in the inventory."""
        for item in self.inventory:
            color = Loot.get_rarity_color(item['rarity'])  # Get color based on rarity
            print(
                f"\033[38;2;{int(color[1:3], 16)};{int(color[3:5], 16)};{int(color[5:7], 16)}m{item['name']} ({item['rarity']})\033[0m")


class LootPopup(QDialog):
    def __init__(self, loot):
        super().__init__()
        self.setWindowTitle("Loot Dropped!")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()
        label = QLabel(f"You obtained: {loot['name']} ({loot['rarity']})")
        color = Loot.get_rarity_color(loot['rarity'])  # Get color based on rarity
        label.setStyleSheet(f"font-size: 14px; color: {color};")
        layout.addWidget(label)
        try:
            pixmap = QPixmap("chest.jpg").scaled(100, 100)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)
        except Exception as e:
            print(f"Could not load loot image: {e}")
        self.setLayout(layout)


def play_loot_sound():
    try:
        mixer.init()
        mixer.music.load("loot.mp3")
        mixer.music.play()
    except Exception as e:
        print(f"Error playing loot sound: {e}")