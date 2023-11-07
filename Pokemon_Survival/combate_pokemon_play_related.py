import os
import pickle
from time import sleep
from Pokemon_Survival.pokeload import print_progress_bar


def save_game(sorted_data):
    # Utiliza os.path.expanduser para conseguir la ruta del usuario por defecto
    main_user_route = os.path.expanduser("~")

    # Utiliza os.makedirs con exist_ok=True para crear la carpeta si no existe
    os.makedirs(main_user_route + "\\Pokemon Survival", exist_ok=True)
    game_user_route = main_user_route + "\\Pokemon Survival"

    print("Guardando partida...")

    with open(f"{game_user_route}\\pokegame.pkl", "wb") as pkgame:
        for index in range(151):
            print_progress_bar(index + 1, 150)
            sleep(0.04)
        pickle.dump(sorted_data, pkgame)
    print("\n¡La partida ha sido guardada con éxito!")


def load_game():
    # Utiliza os.path.expanduser para conseguir la ruta del usuario por defecto
    main_user_route = os.path.expanduser("~")

    # Utiliza os.makedirs con exist_ok=True para crear la carpeta si no existe
    os.makedirs(main_user_route + "\\Pokemon Survival", exist_ok=True)
    game_user_route = main_user_route + "\\Pokemon Survival"

    try:
        print("Cargando partida guardada...")

        with open(f"{game_user_route}\\pokegame.pkl", "rb") as pkgame:
            for index in range(151):
                print_progress_bar(index+1, 150)
                sleep(0.04)
            return pickle.load(pkgame)
    except FileNotFoundError:
        print("No existe un archivo de guardado previo.")
        return None


def delete_play():
    # Utiliza os.path.expanduser para conseguir la ruta del usuario por defecto
    main_user_route = os.path.expanduser("~")

    # Utiliza os.makedirs con exist_ok=True para crear la carpeta si no existe
    os.makedirs(main_user_route + "\\Pokemon Survival", exist_ok=True)
    game_user_route = main_user_route + "\\Pokemon Survival"

    if os.path.exists(game_user_route + "\\pokegame.pkl"):
        os.remove(game_user_route + "\\pokegame.pkl")
