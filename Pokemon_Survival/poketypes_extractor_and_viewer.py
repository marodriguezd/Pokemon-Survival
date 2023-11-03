import pickle
from time import sleep
from pokeload import get_all_pokemons, print_progress_bar


def load_pokemon_types_from_file(filename):
    try:
        print("Cargando el archivo de tipos...")
        with open(filename, "rb") as pokefile:
            bd_types_sorted = pickle.load(pokefile)
            for index in range(151):
                print_progress_bar(index + 1, 150)
                sleep(0.02)
        print("")
    except FileNotFoundError:
        print("¡Archivo no encontrado! Cargando de la base de datos...\n")
        bd_types_sorted = load_pokemon_types_from_database()
        save_pokemon_types_to_file(filename, bd_types_sorted)

    return bd_types_sorted


def load_pokemon_types_from_database():
    bd = get_all_pokemons()
    bd_types = set()
    index = 0
    print("Cargando el archivo de tipos...")
    for pokemon in bd:
        for type in pokemon["type"]:
            bd_types.add(type)
            print_progress_bar(index + 1, 150)
            sleep(0.01)
        index += 1
    return sorted(list(bd_types))


def save_pokemon_types_to_file(filename, bd_types_sorted):
    with open(filename, "wb") as pokefile:
        pickle.dump(bd_types_sorted, pokefile)
    print("\n¡Todos los tipos de pokemons han sido guardados!")


def save_pokemon_types_to_text_file(filename, bd_types_sorted):
    with open(filename, "w") as file:
        for item in bd_types_sorted:
            file.write(item + "\n")


def see_the_types(bd_types_sorted):
    for type in bd_types_sorted:
        print(type)


def main():
    types_filename = "pokemon_types_first_generation.pkl"
    types_sorted_filename = "pokemon_types_first_generation_sorted.txt"

    bd_types_sorted = load_pokemon_types_from_file(types_filename)
    save_pokemon_types_to_text_file(types_sorted_filename, bd_types_sorted)

    print("¡Lista de tipos de Pokémons cargada!\n")

    see_the_types(bd_types_sorted)


if __name__ == "__main__":
    main()
