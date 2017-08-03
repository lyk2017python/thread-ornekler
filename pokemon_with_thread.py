from threading import Thread
from pokemon import Pokemon
import requests
import time


class Fight(Thread):
    def __init__(self,pokemon1,pokemon2):
        super().__init__()
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.winner = None


    def get_winner(self):
        return self.winner
    def run(self):
        while self.pokemon1.can > 0 and self.pokemon2.can > 0:
            self.pokemon1.hasarVer(self.pokemon2)
            if self.pokemon2.can > 0:
                self.pokemon2.hasarVer(self.pokemon1)


        if self.pokemon1.can > 0:
            self.winner = self.pokemon1
        else:
            self.winner = self.pokemon2



class PokemonGetThread(Thread):
    is_completed = False
    def __init__(self,pokemon_uri,pokemon):
        super().__init__()

        self.pokemon = pokemon
        self.pokemon_url = pokemon_uri
        self.pokemonNesnesi = None

    def is_completed_thread(self):
        return self.is_completed

    def get_pokemon(self):
        return self.pokemonNesnesi

    def run(self):
        pokemonjson = requests.get(self.pokemon_url).json()
        yetenekler = []
        for yetenek in pokemonjson['abilities']:
            if yetenek["ability"] != None and yetenek["ability"]["name"] != None:
                yetenekler.append(yetenek["ability"]["name"])

        self.pokemonNesnesi = Pokemon(
            pokemonjson['name'],
            pokemonjson['weight'],
            pokemonjson['height'],
            yetenekler
        )
        for biri in pokemonjson['stats']:
            statName = biri['stat']['name']

            if statName == "speed":
                self.pokemonNesnesi.hiz = biri['base_stat']
            elif statName == "defense":
                self.pokemonNesnesi.savunma = biri['base_stat']
            elif statName == "attack":
                self.pokemonNesnesi.saldiri = biri['base_stat'] / 10
            elif statName == "hp":
                self.pokemonNesnesi.can = biri['base_stat']

            self.pokemonNesnesi.resim = pokemonjson["sprites"]["front_default"]

        self.is_completed = True


class Pokemonlar(Thread):
    def run(self):


        apiUrl = "http://pokeapi.co/api/v2/"
        pokemonListesi = requests.get(apiUrl + "pokemon/").json().get('results')
        pokemonlarThread = []
        for i in pokemonListesi:
            pokemonThread = PokemonGetThread(i.get('url'),i.get("name"))
            pokemonThread.start()
            pokemonlarThread.append({"pokemon":i.get('name'),"thread":pokemonThread})

        all_completed = False

        while all_completed is False:
            all_completed = True
            for i in pokemonlarThread:

                print("%s is_completed : %s " %(i.get("pokemon"),i.get("thread").is_completed_thread()))

                if i.get("thread").is_completed_thread() is False:
                    all_completed = False
            time.sleep(5)

        all_fight_completed = True
        #while all_fight_completed is False:
        for i in range(0,len(pokemonlarThread),2):
            pokemon1 = pokemonlarThread[i]
            pokemon2 = pokemonlarThread[i+1]
            fight = Fight(pokemon1.get("thread").get_pokemon(),pokemon2.get("thread").get_pokemon())
            fight.start()
            while fight.get_winner() is None:
                time.sleep(1)
            print(fight.get_winner().adi)

if __name__ == '__main__':
    p = Pokemonlar()
    p.start()
