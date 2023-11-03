import random
from pokeload import get_all_pokemons


def get_player_profile(pokemon_list):
    return {
        "player_name": input("¿Cuál es tu nombre?: "),
        "pokemon_inventory": [random.choice(pokemon_list) for a in range(3)],
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0
    }


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def get_pokemon_info(pokemon):
    return f"{pokemon['name']} | lvl {pokemon['level']} | hp {pokemon['current_health']}/{pokemon['base_health']}"


def choose_pokemon(player_profile):
    while True:
        print("\nElige con qué pokémon lucharás")
        for index in range(len(player_profile["pokemon_inventory"])):
            print(f"{index} - {get_pokemon_info(player_profile['pokemon_inventory'][index])}")
        try:
            return player_profile["pokemon_inventory"][int(input("¿Cuál eliges?: "))]
        except (ValueError, IndexError):
            print("Opción inválida")


def multiplier_type_calculator(player_pokemon, enemy_pokemon):
    multiplier = 1
    player_type = player_pokemon["type"][0]
    enemy_type = enemy_pokemon["type"][0]

    if enemy_type == "acero" and player_type in ["lucha", "fuego", "tierra"]:
        multiplier = 1.25
    elif enemy_type == "agua" and player_type in ["planta", "electrico"]:
        multiplier = 1.25
    elif enemy_type == "bicho" and player_type in ["volador", "fuego", "roca"]:
        multiplier = 1.25
    elif enemy_type == "dragon" and player_type in ["hada", "hielo", "dragon"]:
        multiplier = 1.25
    elif enemy_type == "electrico" and player_type == "tierra":
        multiplier = 1.25
    elif enemy_type == "fantasma" and player_type in ["fantasma", "siniestro"]:
        multiplier = 1.25
    elif enemy_type == "fuego" and player_type in ["tierra", "agua", "roca"]:
        multiplier = 1.25
    elif enemy_type == "hada" and player_type in ["acero", "veneno"]:
        multiplier = 1.25
    elif enemy_type == "hielo" and player_type in ["lucha", "acero", "roca", "fuego"]:
        multiplier = 1.25
    elif enemy_type == "lucha" and player_type in ["psiquico", "volador", "hielo"]:
        multiplier = 1.25
    elif enemy_type == "normal" and player_type == "lucha":
        multiplier = 1.25
    elif enemy_type == "planta" and player_type in ["volador", "bicho", "veneno", "hielo", "fuego"]:
        multiplier = 1.25
    elif enemy_type == "psiquico" and player_type in ["bicho", "fantasma", "siniestro"]:
        multiplier = 1.25
    elif enemy_type == "roca" and player_type in ["lucha", "tierra", "acero", "agua", "planta"]:
        multiplier = 1.25
    elif enemy_type == "tierra" and player_type in ["agua", "planta", "hielo"]:
        multiplier = 1.25
    elif enemy_type == "veneno" and player_type in ["tierra", "psiquico"]:
        multiplier = 1.25
    elif enemy_type == "volador" and player_type in ["roca", "hielo", "electrico"]:
        multiplier = 1.25

    if player_type == "acero" and enemy_type in ["lucha", "fuego", "tierra"]:
        multiplier = 0.75
    elif player_type == "agua" and enemy_type in ["planta", "electrico"]:
        multiplier = 0.75
    elif player_type == "bicho" and enemy_type in ["volador", "fuego", "roca"]:
        multiplier = 0.75
    elif player_type == "dragon" and enemy_type in ["hada", "hielo", "dragon"]:
        multiplier = 0.75
    elif player_type == "electrico" and enemy_type == "tierra":
        multiplier = 0.75
    elif player_type == "fantasma" and enemy_type in ["fantasma", "siniestro"]:
        multiplier = 0.75
    elif player_type == "fuego" and enemy_type in ["tierra", "agua", "roca"]:
        multiplier = 0.75
    elif player_type == "hada" and enemy_type in ["acero", "veneno"]:
        multiplier = 0.75
    elif player_type == "hielo" and enemy_type in ["lucha", "acero", "roca", "fuego"]:
        multiplier = 0.75
    elif player_type == "lucha" and enemy_type in ["psiquico", "volador", "hielo"]:
        multiplier = 0.75
    elif player_type == "normal" and enemy_type == "lucha":
        multiplier = 0.75
    elif player_type == "planta" and enemy_type in ["volador", "bicho", "veneno", "hielo", "fuego"]:
        multiplier = 0.75
    elif player_type == "psiquico" and enemy_type in ["bicho", "fantasma", "siniestro"]:
        multiplier = 0.75
    elif player_type == "roca" and enemy_type in ["lucha", "tierra", "acero", "agua", "planta"]:
        multiplier = 0.75
    elif player_type == "tierra" and enemy_type in ["agua", "planta", "hielo"]:
        multiplier = 0.75
    elif player_type == "veneno" and enemy_type in ["tierra", "psiquico"]:
        multiplier = 0.75
    elif player_type == "volador" and enemy_type in ["roca", "hielo", "electrico"]:
        multiplier = 0.75

    return multiplier


def pokemon_attacks_in_its_level(attacks, actual_level):
    posible_attacks_in_that_level = []

    for item in attacks:
        if item["min_level"] <= actual_level:
            posible_attacks_in_that_level.append(item)

    while True:
        if len(posible_attacks_in_that_level) > 4:
            posible_attacks_in_that_level.pop(0)
        else:
            break

    return posible_attacks_in_that_level


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


def enemy_attack(player_pokemon, enemy_pokemon):
    enemy_attacks = pokemon_attacks_in_its_level(enemy_pokemon["attacks"], player_pokemon["level"])

    enemy_attack = enemy_attacks[random.randint(0, len(enemy_attacks)-1)]

    enemy_damage_with_type_percentage_applied = int(enemy_attack['damage'].replace("--", "0")) * \
                                               multiplier_type_calculator(player_pokemon, enemy_pokemon)

    player_pokemon["current_health"] -= enemy_damage_with_type_percentage_applied


def assign_experience(attack_history):
    for pokemon in attack_history:
        points = random.randint(1, 5)
        pokemon["current_exp"] += points

        while pokemon["current_exp"] > 20:
            pokemon["current_exp"] -= 20
            pokemon["level"] += 1
            pokemon["current_health"] = pokemon["base_health"]
            print(f"Tu pokemon ha subido al nivel {get_pokemon_info(pokemon)}")


def cure_pokemon(player_profile, player_pokemon):
    pass


def capture_with_pokeball(player_profile, enemy_pokemon):
    pass


def fight(player_profile, enemy_pokemon):
    print("\n--- NUEVO COMBATE ---")

    attack_history = []
    player_pokemon = choose_pokemon(player_profile)
    # print(f"\nContrincantes: {get_pokemon_info(player_pokemon)} VS {get_pokemon_info(enemy_pokemon)}")

    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:
        action = "mondongo"
        print(f"\nContrincantes: {get_pokemon_info(player_pokemon)} VS {get_pokemon_info(enemy_pokemon)}")
        while action.upper() not in ["A", "P", "V", "C"]:
            action = input("¿Qué desea hacer?: "
                           "[A]tacar, "
                           "[P]okeball, "
                           "Poción de [V]ida, "
                           "[C]ambiar: ")

        if action.upper() == "A":
            player_attack(player_pokemon, enemy_pokemon)
            attack_history.append(player_pokemon)
            enemy_attack(player_pokemon, enemy_pokemon)
        elif action.upper() == "V":
            # Si el usuario tiene curas en el inventario, se aplica, cura 50 de vida hasta llegar a 100
            # Si el usuario no tiene, no se cura
            cure_pokemon(player_profile, player_pokemon)
        elif action.upper() == "P":
            # Si el usuario tiene pokeballs en el inventario, se tira una, hay una probabilidad de capturarlo
            # relativa a la salud restante del pokémon. Cuando se captura pasa a estar en el inventario con la misma
            # salud que tenía.
            capture_with_pokeball(player_profile, enemy_pokemon)
        elif action.upper() == "C":
            player_pokemon = choose_pokemon(player_profile)

        if player_pokemon["current_health"] <= 0 and any_player_pokemon_lives(player_profile):
            player_pokemon["current_health"] = 0  # Para que la salud del Pokémon muerto sea 0 sí o sí
            player_pokemon = choose_pokemon(player_profile)

    if enemy_pokemon["current_health"] > 0:
        print("¡Has ganado!")
        assign_experience(attack_history)

    print("--- FIN DEL COMBATE ---")
    input("\nPresiona ENTER para continuar...")


def item_lottery(player_profile):
    """Según un factor aleatorio, al jugador le puede tocar una pokeball o una cura"""
    pass


def main():
    pokemon_list = get_all_pokemons()
    player_profile = get_player_profile(pokemon_list)

    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)
        item_lottery(player_profile)

    print(f"Has perdido en el combate nº{player_profile['combats']}")


if __name__ == "__main__":
    main()
