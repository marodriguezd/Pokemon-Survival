import os.path
import pickle
import sys
from time import sleep

from requests_html import HTMLSession


pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 100,
    "level": 1,
    "type": None,
    "current_exp": 0
}

URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="


def get_pokemon(index):
    url = f"{URL_BASE}{index}"
    session = HTMLSession()

    new_pokemon = pokemon_base.copy()
    pokemon_page = session.get(url)

    new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text.split("\n")[0]  # Para coger solo name.

    new_pokemon["type"] = []
    new_pokemon["type"] = [img.attrs["alt"] for img in
                           pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img")]

    new_pokemon["attacks"] = []
    for attack_item in pokemon_page.html.find(".pkmain")[-1].find("tr .check3"):
        min_level = min_level_attack_giver(attack_item)
        attack = {
            "name": attack_item.find("td", first=True).find("a", first=True).text,
            "type": attack_item.find("td")[1].find("img", first=True).attrs["alt"],
            "min_level": min_level,
            "damage": attack_item.find("td")[3].text
        }
        new_pokemon["attacks"].append(attack)

    return new_pokemon


def min_level_attack_giver(attack_item):
    min_level = 1

    try:
        min_level = int(attack_item.find("th")[1].text.replace("--", "0"))
    except ValueError:
        min_level = int(attack_item.find("th", first=True).text.replace("--", "0"))
    finally:
        return min_level


def print_progress_bar(iteration, total, bar_length=50):
    progress = (iteration / total)
    arrow = '=' * int(round(bar_length * progress))
    spaces = ' ' * (bar_length - len(arrow))
    percentage = round(progress * 100, 2)
    if percentage > 100:
        percentage = 100
    sys.stdout.write(f'\r[{arrow + spaces}] {percentage}%')
    sys.stdout.flush()


def get_all_pokemons():
    # Utiliza os.path.expanduser para conseguir la ruta del usuario por defecto
    main_user_route = os.path.expanduser("~")

    # Utiliza os.makedirs con exist_ok=True para crear la carpeta si no existe
    os.makedirs(main_user_route + "\\Pokemon Survival", exist_ok=True)
    game_user_route = main_user_route + "\\Pokemon Survival"

    try:
        print("Cargando el archivo de Pokémons...")

        with open(f"{game_user_route}\\pokefile.pkl", "rb") as pokefile:
            all_pokemons = pickle.load(pokefile)
            for index in range(151):
                print_progress_bar(index+1, 150)
                sleep(0.04)
    except FileNotFoundError:
        print("¡Archivo no encontrado! Cargando de internet...")
        all_pokemons = []
        for index in range(151):
            all_pokemons.append(get_pokemon(index + 1))
            print_progress_bar(index+1, 150)

        with open(f"{game_user_route}\\pokefile.pkl", "wb") as pokefile:
            pickle.dump(all_pokemons, pokefile)
        print("\n¡Todos los pokemons han sido descargados!")

    print("\n¡Lista de Pokémons cargada!\n")
    return all_pokemons
