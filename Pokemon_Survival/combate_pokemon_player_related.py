import os
import random
from Pokemon_Survival.combate_pokemon_enemy_related import multiplier_type_calculator
from Pokemon_Survival.combate_pokemon_pokemon_related import pokemon_attacks_in_its_level


def YesOrNo(text_to_show):
    while True:
        try:
            player_wants = input(text_to_show)
            if player_wants.upper() not in ["S", "N"]:
                raise ValueError
            elif player_wants.upper() == "S":
                return True
            else:
                return False
        except ValueError:
            print("Opción inválida, responda con Ss o Nn.")


def if_player_wants_to_change_it_name(actual_name):
    if YesOrNo("¿Desea cambiar su nombre? [S/N]: "):
        new_user_name = input("¿Cuál será su nuevo nombre?: ")
    else:
        return actual_name

    return new_user_name


def set_or_get_player_name():
    # Utiliza os.path.expanduser para conseguir la ruta del usuario por defecto
    main_user_route = os.path.expanduser("~")

    # Utiliza os.makedirs con exist_ok=True para crear la carpeta si no existe
    os.makedirs(main_user_route + "\\Pokemon Survival", exist_ok=True)
    game_user_route = main_user_route + "\\Pokemon Survival"

    try:
        with open(f"{game_user_route}\\username.txt", "r") as name_in_game:
            user_name = name_in_game.read().split("\n")[0]
            print(f"\nBienvenid@ de vuelta {user_name}")
            new_user_name = if_player_wants_to_change_it_name(user_name)
            if user_name != new_user_name:
                with open(f"{game_user_route}\\username.txt", "w") as actual_name:
                    actual_name.write(new_user_name + "\n")
                    user_name = new_user_name
    except FileNotFoundError:
        with open(f"{game_user_route}\\username.txt", "w") as name_in_game:
            user_name = input("¿Cuál es su nombre?: ")
            name_in_game.write(user_name + "\n")

    return user_name


def get_player_profile(pokemon_list):
    # Selecciona Pokémon únicos aleatoriamente para el inventario
    pokemon_inventory = []
    while len(pokemon_inventory) < 3:
        random_pokemon = random.choice(pokemon_list)
        if random_pokemon not in pokemon_inventory:
            pokemon_inventory.append(random_pokemon)

    user_name = set_or_get_player_name()

    return {
        "player_name": user_name,
        "pokemon_inventory": pokemon_inventory,
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0
    }


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def get_inventory_info(player):
    return f"Pokeballs: {player['pokeballs']} | Pociones de Vida: {player['health_potion']}"


def player_attack(player_pokemon, enemy_pokemon):
    """Cuando se elige el ataque del usuario, solo se muestran los ataques disponibles en ese nivel."""
    player_attacks = pokemon_attacks_in_its_level(player_pokemon["attacks"], player_pokemon["level"])

    while True:
        print("\nElige qué ataque harás")
        for index in range(len(player_attacks)):
            print(f"{index} - {player_attacks[index]['name']}")
        try:
            user_attack = player_attacks[int(input("¿Cuál eliges?: "))]
            break
        except (ValueError, IndexError):
            print("Opción inválida")

    user_damage_with_type_percentage_applied = int(user_attack['damage'].replace("--", "0")) * \
                                               multiplier_type_calculator(player_pokemon, enemy_pokemon)

    enemy_pokemon["current_health"] -= user_damage_with_type_percentage_applied


def item_lottery(player_profile):
    """Según un factor aleatorio, al jugador le puede tocar una pokeball o una cura"""
    PROBABILITY = 0.33  # 33% de probabilidad
    lottery = random.random()  # Random entre 0 y 1

    if lottery <= PROBABILITY:
        if random.randint(0, 1) == 0:
            player_profile["pokeballs"] += 1
            print("¡Has obtenido 1 Pokeball!")
        else:
            player_profile["health_potion"] += 1
            print("¡Has obtenido 1 Poción de Vida!")


def add_actual_combat(player_profile):
    player_profile["combats"] += 1
