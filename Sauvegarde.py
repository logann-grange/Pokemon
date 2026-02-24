import json
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SAVE_FILE = os.path.join(PROJECT_ROOT, "save.json")

def save_game(player,map):
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump({
            "player": {
                "pos": player.pos,
                "hitbox": [player.hitbox.x, player.hitbox.y],
                "direction": player.direction,
            },
            "map": map.name
        }, file, indent=4)
        
def load_game(player, map):
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            player.pos = list(data["player"]["pos"])

            hitbox_data = data["player"].get("hitbox")
            if isinstance(hitbox_data, list) and len(hitbox_data) == 2:
                player.hitbox.x = int(hitbox_data[0])
                player.hitbox.y = int(hitbox_data[1])
            else:
                player.hitbox.x = int(player.pos[0])
                player.hitbox.y = int(player.pos[1]) + 16

            player.rect.topleft = (player.pos[0], player.pos[1])
            player.direction = data["player"]["direction"]
            map.name = data["map"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass
    return player, map