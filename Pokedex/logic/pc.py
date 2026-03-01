from Pokedex.logic.Pokedex import Pokedex
from Pokedex.logic.Pokemon import Pokemon
import json
import os

class Pc(Pokedex) :

    def __init__(self):
        super().__init__()
        self.pokemon = self.load_pokemon_list("equipe")
        self.displayed_pokemon = self.searching()
        self.team = self.refresh_team()

    def load_pokemon_list(self, file="equipe"):
        list_pokemon = []
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        equipe_file = os.path.join(project_root, "data", f"{file}.json")
        pokedex_file = os.path.join(project_root, "data", "pokedex.json")

        try:
            with open(equipe_file, "r", encoding="utf-8") as file_handle:
                equipe_content = json.load(file_handle)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        try:
            with open(pokedex_file, "r", encoding="utf-8") as file_handle:
                pokedex_content = json.load(file_handle)
        except (FileNotFoundError, json.JSONDecodeError):
            pokedex_content = []

        for index, pokemon_data in enumerate(equipe_content):
            pokemon_info = None
            for poke in pokedex_content:
                if int(poke["id"]) == int(pokemon_data["id"]):
                    pokemon_info = poke
                    break

            if not pokemon_info:
                continue

            pokemon = Pokemon(
                pokemon_data["id"],
                pokemon_data["name"],
                pokemon_data["type"],
                pokemon_info.get("image", ""),
                pokemon_info.get("coord", []),
                pokemon_data["hp_base"],
                pokemon_data["attack_base"],
                pokemon_data["defense_base"],
                pokemon_data.get("level", 1),
                pokemon_data.get("xp", 0),
                pokemon_info.get("evo", ""),
                pokemon_info.get("sub_evo", ""),
                pokemon_info.get("hidden", False),
            )

            pokemon.index_team = pokemon_data.get("index_team", index if index < 6 else None)
            list_pokemon.append(pokemon)

        return list_pokemon

    # def load_pokemon_list(self, file) :
    #     list_pokemon = []
    #     with open(f"{file}.json", "r", encoding="utf-8") as file :
    #         content = json.load(file)
        
    #     for pokemon in content : 
    #         list_pokemon.append(Pokemon(pokemon["id"], pokemon["name"], None, pokemon["type"],  pokemon["image"], pokemon["type"], pokemon["stats"]["hp"], pokemon["stats"]["attack"], pokemon["stats"]["defense"], 0, 0, pokemon["evo"], pokemon["sub_evo"], pokemon["hidden"], index_team = pokemon["index_team"]))

    #     return list_pokemon

    def change_displayed_index(self, num, page):
        if self.selected_pokemon == None or page != self.page:
            return 0

        current_index = self.get_index_from_pokemon(self.selected_pokemon)
        new_index = current_index + num
    
        page_index = self.page - 1
        max_len = len(self.displayed_pokemon[page_index])

        # Vérifications des limites
        if (num == 6 and new_index >= max_len) or (num == -6 and new_index < 0):
            return current_index
        elif num == 1 and new_index >= 18:
            self.switch_page(1)
            return 0
        elif num == -1 and new_index < 0:
            if page_index != 0 :
                self.switch_page(-1)
                return len(self.displayed_pokemon[self.page-1])-1
            return current_index

        # Vérifier que l'index est valide
        if new_index < 0 or new_index >= max_len:
            return current_index
        
        return new_index
    
    def add_to_team(self) :
        for i in range(len(self.team)) :
            if self.team[i] == None and self.selected_pokemon not in self.team:
                self.team[i] = self.selected_pokemon
                for pokemon in self.pokemon : 
                    if pokemon == self.selected_pokemon :
                        pokemon.index_team = i
                self.selected_pokemon.change_team_index_in_json(i)
            elif self.selected_pokemon == self.team[i]:
                self.team[i] = None
                for pokemon in self.pokemon : 
                    if pokemon == self.selected_pokemon :
                        pokemon.index_team = None
                self.selected_pokemon.change_team_index_in_json(None)
                return
    
    def switch_to_first_index(self):
        if self.selected_pokemon is None:
            return
    
        # Si le pokemon n'est pas dans la team ou deja 1er, on ne fait rien
        if self.selected_pokemon.index_team is None or self.selected_pokemon.index_team == 0:
            return

        old_index = self.selected_pokemon.index_team

        for poke in self.team:
            if poke is not None and poke.index_team == 0:
                poke.index_team = old_index
                poke.change_team_index_in_json(old_index)
                self.team[old_index] = poke
                break

        self.selected_pokemon.index_team = 0
        self.selected_pokemon.change_team_index_in_json(0)
        self.team[0] = self.selected_pokemon
            
    
    def refresh_team(self) :
        self.team = [None, None, None, None, None, None]
        for pokemon in self.pokemon :
            if pokemon.index_team is not None :
                self.team[pokemon.index_team] = pokemon
        return self.team

