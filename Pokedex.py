from Pokemon import Pokemon
import json

list_type = ["Fire", "Water","Electric", "Grass", "Rock","Ground", "Fighting", "Steel", "Dragon", "Ghost", "Poison", "Normal", "Flying", "Psy", "Ice", "Darkness", "Fairy"]
page_size = 18

class Pokedex() :

    def __init__(self) :
        self.pokemon = self.load_pokemon_list()
        self.search = ""
        self.displayed_pokemon = self.searching()
        self.page = 1
        self.selected_pokemon = None
        self.num_unlock = self.get_num_unlock()

    def load_pokemon_list(self) :
        list_pokemon = []
        with open("pokedex.json", "r", encoding="utf-8") as file :
            content = json.load(file)
        
        for pokemon in content : 
            list_pokemon.append(Pokemon(pokemon["id"], pokemon["name"], pokemon["type"],  pokemon["image"], pokemon["type"], pokemon["stats"]["hp"], pokemon["stats"]["attack"], pokemon["stats"]["defense"], 0, 0, pokemon["evo"], pokemon["sub_evo"], pokemon["hidden"]))

        return list_pokemon
        
    def switch_page(self, direction) :
        self.page = (self.page + direction) % (len(self.displayed_pokemon)+1)
        if self.page == 0 and direction == 1:
            self.page = 1
        if self.page == 0 and direction == -1:
            self.page = len(self.displayed_pokemon)

    def display_pokemon(self) :
        return self.displayed_pokemon[self.page]

    def searching(self) :
        list_page = []
        displayed_pokemon = []
    
        for i in range(len(self.pokemon)) :
            if self.search.upper() in self.pokemon[i].name.upper() or self.search == "":
                list_page.append(self.pokemon[i])
                #vérifier si on doit créer une nouvelle page
                if len(list_page)%page_size == 0:
                    displayed_pokemon.append(list_page)
                    list_page = []
        #ajouter la dernière page si elle contient des Pokémon
        if list_page:
            displayed_pokemon.append(list_page)

        return displayed_pokemon
    
    def get_pokemon_by_id(self, id) :
        for pokemon in self.pokemon :
            if pokemon.id == id :
                return pokemon
    
    def select_pokemon(self, pokemon:Pokemon) :
        if not pokemon.hidden :
            self.selected_pokemon = pokemon

    def get_num_unlock(self) :
        num = 0
        for pokemon in self.pokemon :
            if not pokemon.hidden :
                num += 1
        return num
    
    def get_index_from_pokemon(self, pokemon) :
        for i in range(len(self.displayed_pokemon[self.page-1])) :
            if self.displayed_pokemon[self.page-1][i] == pokemon :
                return i
    
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
            return max_len - 1

        # Vérifier que l'index est valide
        if new_index < 0 or new_index >= max_len:
            return current_index

        # Sauter les cases cachées - vérifier avant d'accéder
        max_attempts = 20  # Sécurité
        attempts = 0
    
        while 0 <= new_index < max_len and attempts < max_attempts:
            if not self.displayed_pokemon[page_index][new_index].hidden:
                return new_index  # Case valide trouvée !
            new_index += num
            attempts += 1

        # Si aucune case valide trouvée, rester sur place
        return current_index
        



        
        

