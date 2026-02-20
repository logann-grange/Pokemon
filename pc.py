from Pokedex import  Pokedex
from Pokemon import Pokemon
import json

class Pc(Pokedex) :

    def __init__(self):
        super().__init__()
        self.pokemon = self.load_pokemon_list("equipe")
        self.displayed_pokemon = self.searching()
        self.team = self.refresh_team()

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
                self.change_team_index_in_json(i)
            elif self.selected_pokemon == self.team[i]:
                self.team[i] = None
                for pokemon in self.pokemon : 
                    if pokemon == self.selected_pokemon :
                        pokemon.index_team = None
                self.change_team_index_in_json(i)
                return
    
    def switch_to_first_index(self) :
        for pokemon in self.pokemon : 
            if pokemon == self.selected_pokemon :
                old_index = self.selected_pokemon.index_team
                for poke in self.team :
                    if poke is not None and poke.index_team == 0 :
                        poke.index_team = old_index
                pokemon.index_team = 0
            

    def change_team_index_in_json(self, index):
        with open("equipe.json", "r", encoding="utf-8") as file:
            content = json.load(file)
    
        for i, pokemon in enumerate(content):
            if pokemon["id"] == self.selected_pokemon.id:
                content[i]["index_team"] = index
                break
    
        with open("equipe.json", "w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=4)
    
    def refresh_team(self) :
        self.team = [None, None, None, None, None, None]
        for pokemon in self.pokemon :
            if pokemon.index_team is not None :
                self.team[pokemon.index_team] = pokemon
        #raffraichisement ne fonctionne pas
        return self.team

