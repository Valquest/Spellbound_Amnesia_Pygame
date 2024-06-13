from core import core_funct, spells

card_types = {
    "Damage 1": (1, 0, "damage_enemy"),
    "Freeze 1": (1, 1),
    "Damage 2": (2, 0),
    "Fire ball 3": (3, 0),
    "Ice lance 2": (2, 0)
}

card_types2 = {
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
            "damage_enemy": spells.damage_enemy,
            "freeze_enemy": spells.freeze_enemy
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
            "damage_enemy": spells.damage_enemy,
            "freeze_enemy": spells.freeze_enemy
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
    }
}
