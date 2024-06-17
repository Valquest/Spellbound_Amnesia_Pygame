from core import core_funct, spells

card_types = {
    "Damage 1": {
        "Damage": 1,
        "Enemy to target": 0,
        "Card effects": {
            "damage_enemy": spells.damage_enemy
        }
    },
    "Freeze 1": {
        "Damage": 1,
        "Enemy to target": 1,
        "Turns frozen": 1,
        "Card effects": {
            "freeze_enemy": spells.freeze_enemy,
            "damage_enemy": spells.damage_enemy

        }
    },
    "Damage 2": {
        "Damage": 2,
        "Enemy to target": 0,
        "Card effects": {
            "damage_enemy": spells.damage_enemy
        }
    },
    "Fire ball 3": {
        "Damage": 3,
        "Enemy to target": 0,
        "Card effects": {
            "damage_enemy": spells.damage_enemy
        }
    },
    "Ice lance 2": {
        "Damage": 2,
        "Enemy to target": 0,
        "Turns frozen": 2,
        "Card effects": {
            "freeze_enemy": spells.freeze_enemy,
            "damage_enemy": spells.damage_enemy
        }
    },
    "Gust 1": {
        "Damage": 1,
        "Enemy to target": 0,
        "Turns frozen": 2,
        "Move direction": -1,
        "Move positions": 1,
        "Card effects": {
            "move_enemy": spells.move_enemy,
            "damage_enemy": spells.damage_enemy

        }
    },
    "Splash 3": {
        "Damage": 3,
        "Enemy to target": 0,
        "Card effects": {
            "damage_adjacent": spells.damage_adjacent,
            "damage_enemy": spells.damage_enemy
        }
    }
}
