import Pokemon
import json
import random



def apparition_pokemon():
    team_data=[]
    with open('equipe.json', 'r') as f:
        team_data = json.load(f)
    pokedex_data = []
    with open('pokedex.json', 'r') as f:
        pokedex_data = json.load(f)
    niv=0
    for i in team_data:
        if i["level"] > niv:
            niv = i["level"]
    
    if niv < 25:
        # Pokémon de base (sans pré-évolution) = sub_evo vide
        possible_pokemon = [pokemon for pokemon in pokedex_data if (not pokemon.get("sub_evo") or pokemon.get("sub_evo") == "") and pokemon["hidden"]==True]
        pokemon_level=random.randint(max(1, niv-5), niv+5)  # Niveau aléatoire autour du niveau du joueur
    elif niv < 50:
        # Pokémon évolués (avec pré-évolution ou évolution)
        possible_pokemon = [pokemon for pokemon in pokedex_data if (pokemon.get("evo") or pokemon.get("sub_evo")) and pokemon["hidden"]==True]
        pokemon_level=random.randint(max(1, niv-10), niv+10)  # Niveau aléatoire autour du niveau du joueur
    else:
        possible_pokemon = [pokemon for pokemon in pokedex_data if pokemon["hidden"]==True]
        pokemon_level=random.randint(max(1, niv-15), niv+15)  # Niveau aléatoire autour du niveau du joueur

    # Fallback 1: Si aucun pokemon caché trouvé au niveau approprié, prendre tous les cachés
    if not possible_pokemon:
        possible_pokemon = [pokemon for pokemon in pokedex_data if pokemon["hidden"]==True] 
        pokemon_level=random.randint(1, 100)  # Niveau aléatoire entre 1 et 100
        
    # Fallback 2: Si tous les pokemon sont découverts, prendre n'importe lequel
    if not possible_pokemon:
        possible_pokemon = pokedex_data
        pokemon_level=random.randint(1, 100)  # Niveau aléatoire entre 1 et 100
    
    if not possible_pokemon:
        raise ValueError("Aucun Pokémon disponible dans pokedex.json")

    chosen = random.choice(possible_pokemon)
    pokemon_aparue = Pokemon.Pokemon(
        chosen["id"], 
        chosen["name"], 
        chosen["type"], 
        chosen["image"], 
        chosen.get("coord", []),
        (chosen["stats"]["hp"],  
        chosen["stats"]["attack"],  
        chosen["stats"]["defense"],  
         ),
        pokemon_level,
        0, 
        chosen["evo"], 
        chosen["sub_evo"], 
        chosen["hidden"]
    )
    
    return pokemon_aparue
               
test=apparition_pokemon()
print(test.name)   