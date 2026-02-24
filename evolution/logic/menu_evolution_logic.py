import os
import json

# Get project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

def load_pokedex_data(pokedex_file="pokedex.json"):
    # If path is relative (just filename), make it relative to project root
    if not os.path.isabs(pokedex_file) and not os.path.exists(pokedex_file):
        pokedex_file = os.path.join(PROJECT_ROOT, pokedex_file)
    with open(pokedex_file, "r", encoding="utf-8") as file:
        return json.load(file)


def find_pokemon_and_evolution(pokedex_data, pokemon_name):
    pokemon = None
    for entry in pokedex_data:
        if entry["name"].lower() == pokemon_name.lower():
            pokemon = entry
            break

    if not pokemon:
        return None, None

    next_pokemon = None
    for entry in pokedex_data:
        if int(entry["id"]) == int(pokemon["id"]) + 1:
            next_pokemon = entry
            break

    return pokemon, next_pokemon


def build_pokemon_image_path(pokemon_id):
    return f"./Asset/front/{int(pokemon_id)}.png"


def load_team(team_file="equipe.json"):
    # If path is relative (just filename), make it relative to project root
    if not os.path.isabs(team_file) and not os.path.exists(team_file):
        team_file = os.path.join(PROJECT_ROOT, team_file)
    try:
        with open(team_file, "r", encoding="utf-8") as file:
            team = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        team = []

    if not isinstance(team, list):
        return []
    return team


def save_team(team, team_file="equipe.json"):
    # If path is relative (just filename), make it relative to project root
    if not os.path.isabs(team_file) and not os.path.exists(team_file):
        team_file = os.path.join(PROJECT_ROOT, team_file)
    with open(team_file, "w", encoding="utf-8") as file:
        json.dump(team, file, indent=4, ensure_ascii=False)


def update_team_with_evolution(team, pokemon_name, evolved_pokemon, current_level=None, current_xp=None):
    for index, member in enumerate(team):
        if str(member.get("name", "")).lower() == pokemon_name.lower():
            level = current_level if current_level is not None else member.get("level", 1)
            xp = current_xp if current_xp is not None else member.get("xp", 0)

            evo_hp = evolved_pokemon["stats"]["hp"]
            evo_attack = evolved_pokemon["stats"]["attack"]
            evo_defense = evolved_pokemon["stats"]["defense"]

            final_hp = evo_hp * 2 * level // 100 + 10 + level
            final_attack = evo_attack * 2 * level // 100 + 5
            final_defense = evo_defense * 2 * level // 100 + 5

            team[index] = {
                "id": evolved_pokemon["id"],
                "name": evolved_pokemon["name"],
                "type": evolved_pokemon.get("type"),
                "hp": final_hp,
                "hp_base": evo_hp,
                "attack": final_attack,
                "attack_base": evo_attack,
                "defense": final_defense,
                "defense_base": evo_defense,
                "level": level,
                "xp": xp,
            }
            break

    return team


def reveal_pokedex_entry(pokemon_id, pokedex_file="pokedex.json"):
    # If path is relative (just filename), make it relative to project root
    if not os.path.isabs(pokedex_file) and not os.path.exists(pokedex_file):
        pokedex_file = os.path.join(PROJECT_ROOT, pokedex_file)
    pokedex_data = load_pokedex_data(pokedex_file)

    for entry in pokedex_data:
        if int(entry["id"]) == int(pokemon_id):
            entry["hidden"] = False

    with open(pokedex_file, "w", encoding="utf-8") as file:
        json.dump(pokedex_data, file, indent=4, ensure_ascii=False)
