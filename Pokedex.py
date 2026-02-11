from Pokemon import Pokemon
import json

list_type = ["Fire", "Water", "Grass", "Rock", "Fighting", "Steel", "Dragon", "Ghost", "Poison", "Normal", "Flying", "Psy"]
page_size = 18

class Pokedex() :

    def __init__(self) :
        self.pokemon = self.load_pokemon_list()
        self.search = ""
        self.displayed_pokemon = self.searching()
        self.page = 1
        self.filter = ""

    def load_pokemon_list(self) :
        list_pokemon = []
        with open("pokedex.json", "r", encoding="utf-8") as file :
            content = json.load(file)
        
        for pokemon in content : 
            list_pokemon.append(Pokemon(pokemon["id"], pokemon["name"], pokemon["type"],  pokemon["image"], pokemon["type"], pokemon["stats"]["hp"], pokemon["stats"]["attack"], pokemon["stats"]["defense"], 0, 0, pokemon["hidden"]))

        return list_pokemon
        
    def switch_page(self, direction) :
        self.page = (self.page + direction) % (len(self.displayed_pokemon)+1)
        if self.page == 0 :
            self.page = 1

    def display_pokemon(self) :
        return self.displayed_pokemon[self.page]

    def searching(self) :
        list_page = []
        displayed_pokemon = []
    
        for i in range(len(self.pokemon)) :
            if self.search in self.pokemon[i].name or self.search == "":
                list_page.append(self.pokemon[i])
                #vérifier si on doit créer une nouvelle page
                if len(list_page)%page_size == 0:
                    displayed_pokemon.append(list_page)
                    list_page = []
        #ajouter la dernière page si elle contient des Pokémon
        if list_page:
            displayed_pokemon.append(list_page)
    
        print(displayed_pokemon)
        print(len(displayed_pokemon))
        return displayed_pokemon

    def type_filtring(self) :
        pokemon_remaining = self.pokemon.copy()
        filter_list = []
        for type in list_type :
            for pokemon in pokemon_remaining :
                if pokemon.type == type :
                    filter_list.append(pokemon)
                    pokemon_remaining.remove(pokemon)
        self.pokemon = filter_list
        

