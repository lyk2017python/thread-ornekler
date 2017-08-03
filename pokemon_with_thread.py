from threading import Thread
from pokemon import Pokemon
import requests
import time


class PokemonGetThread(Thread):
    is_completed = False
    def __init__(self,pokemon_uri,pokemon):
        Thread.__init__(self)
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

if __name__ == '__main__':
    p = Pokemonlar()
    p.start()
