# ⚔️ RPG Game
@2024 Calin Mihai-Catalin

The primary purpose of this RPG game is to provide an engaging and interactive experience where players can equip items, fight enemies, and customize their character’s stats. As you progress through the game, you can equip different types of gear (helmets, pants, weapons, etc.), which will modify your character’s attributes, such as Health Points (HP) and Attack Power (AP).

Given that the game is still under development, expect regular updates and improvements as new features are added and bugs are fixed. The game may also require adjustments for future compatibility with new Python versions or libraries.

## Features

### Character Customization:
- Equip different items to improve your character's stats, such as HP and AP.

### Dynamic Combat:
- Fight various enemies to earn loot and experience points.

### Loot Drops & Item Rarities:
- Enemies drop loot with various rarities: Common, Rare, Epic, and Legendary.
- Each item can provide different stat bonuses (e.g., increased HP or AP).

### Inventory System:
- Manage your items and equip the ones that best suit your playstyle.

### Item Bonuses:
- Each item provides stat bonuses, like increased HP or AP, when equipped.

### PyQt5 Popup:
- After defeating enemies, a PyQt5 popup will appear showing your loot drops. The rarity of the loot (Common, Rare, Epic, Legendary) will be highlighted.
- Bonuses from the equipment (e.g., increased HP or AP) will also be shown.

### Sound Effects:
- The game includes sound effects for loot drops.

## How to Play

1. **Start the game** and choose a character class.
2. **Fight enemies** and gain drops.
3. **Loot drops** will be displayed with a popup, showing the rarity of the item and any stat bonuses.
4. **Equip your items** to increase your HP, AP, or other stats.


## Installation

This game is coded in Python, utilizing the **PyQt5** library for the graphical interface and **pygame** for handling sound effects. You need to install these libraries before running the game.

### Prerequisites:
- Python 3.x
- PyQt5
- pygame

You can install the required libraries via pip:
```bash
pip install PyQt5 pygame
