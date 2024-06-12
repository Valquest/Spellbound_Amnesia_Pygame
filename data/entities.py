from core import core_funct

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
            "damage_enemy": core_funct.damage_enemy,
            "move_enemy": core_funct.move_enemy
        }
    },
    "Freeze 1": {

    },
    "Damage 2": {

    },
    "Fire ball 3": {

    },
    "Ice lance 2": {

    }
}