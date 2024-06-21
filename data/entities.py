from core import spells

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
    },
    "Spark 1": {
        "Damage": 1,
        "Enemy to target": 0,
        "Chain length": 3,
        "Card effects": {
            "chain_damage": spells.chain_damage,
            "damage_enemy": spells.damage_enemy
        }
    },
    "Thunderbolt 2": {
        "Damage": 2,
        "Enemy to target": 0,
        "Chain length": 1,
        "Card effects": {
            "chain_damage": spells.chain_damage,
            "damage_enemy": spells.damage_enemy
        }
    }
}

stone_types = {
    "Stone1": {
        "rarity": 0.99,
        "image_name": ""
    },
    "Stone2": {
        "rarity": 0.89,
        "image_name": ""
    },
    "Stone3": {
        "rarity": 0.79,
        "image_name": ""
    },
    "Stone4": {
        "rarity": 0.69,
        "image_name": ""
    },
    "Stone5": {
        "rarity": 0.59,
        "image_name": ""
    },
    "Stone6": {
        "rarity": 0.49,
        "image_name": ""
    },
    "Stone7": {
        "rarity": 0.39,
        "image_name": ""
    }

}

player_inv = {
    "Stone1": 2,
    "Stone2": 3,
    "Stone3": 1,
    "Stone4": 5,
    "Stone5": 1,
    "Stone6": 2,
    "Stone7": 10
}
