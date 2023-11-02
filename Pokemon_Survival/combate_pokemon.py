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
        print("Elige con qué pokémon lucharás")
        for index in range(len(player_profile["pokemon_inventory"])):
            print(f"{index} - {get_pokemon_info(player_profile['pokemon_inventory'][index])}")
        try:
            return player_profile["pokemon_inventory"][int(input("¿Cuál eliges?: "))]
        except (ValueError, IndexError):
            print("Opción inválida")


def player_attack(player_pokemon, enemy_pokemon):
    """Implementar multiplicadores en base al tipo de pokémon
    Acero: Débil frente al tipo Lucha, tipo Fuego y tipo Tierra
    Agua: Débil frente al tipo Planta y tipo Eléctrico
    Bicho: Débil frente al tipo Volador, tipo Fuego y tipo Roca
    Dragón: Débil frente al tipo Hada, tipo Hielo y tipo Dragón
    Eléctrico: Débil frente al tipo Tierra
    Fantasma: Débil frente al tipo Fantasma y tipo Siniestro
    Fuego: Débil frente al tipo Tierra, tipo Agua y tipo Roca
    Hada: Débil frente al tipo Acero y tipo Veneno
    Hielo: Débil frente al tipo Lucha, tipo Acero, tipo Roca y tipo Fuego
    Lucha: Débil frente al tipo Psíquico, tipo Volador y tipo Hielo
    Normal: Débil frente al tipo Lucha
    Planta: Débil frente al tipo Volador, tipo Bicho, tipo Veneno, tipo Hielo y tipo Fuego
    Psíquico: Débil frente al tipo Bicho, tipo Fantasma y tipo Siniestro
    Roca: Débil frente al tipo Lucha, tipo Tierra, tipo Acero, tipo Agua y tipo Planta
    Siniestro: Débil frente al tipo Lucha, tipo Hada y tipo Bicho
    Tierra: Débil frente al tipo Agua, tipo Planta y tipo Hielo
    Veneno: Débil frente al tipo Tierra y tipo Psíquico
    Volador: Débil frente al tipo Roca, tipo Hielo y tipo Eléctrico

    Cuando se elige el ataque del usuario, solo se muestran los ataques disponibles en ese nivel.
    * 1.25 o deseado"""

    pass


def enemy_attack(player_pokemon, enemy_pokemon):
    pass


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
    print(f"\nContrincantes: {get_pokemon_info(player_pokemon)} VS {get_pokemon_info(enemy_pokemon)}")

    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:
        action = None
        while action not in ["A", "P", "V", "C"]:
            action = input("¿Qué desea hacer?: "
                           "[A]tacar, "
                           "[P]okeball, "
                           "Poción de [V]ida, "
                           "[C]ambiar")

        if action == "A":
            player_attack(player_pokemon, enemy_pokemon)
            attack_history.append(player_pokemon)
            enemy_attack(player_pokemon, enemy_pokemon)
        elif action == "V":
            # Si el usuario tiene curas en el inventario, se aplica, cura 50 de vida hasta llegar a 100
            # Si el usuario no tiene, no se cura
            cure_pokemon(player_profile, player_pokemon)
        elif action == "P":
            # Si el usuario tiene pokeballs en el inventario, se tira una, hay una probabilidad de capturarlo
            # relativa a la salud restante del pokémon. Cuando se captura pasa a estar en el inventario con la misma
            # salud que tenía.
            capture_with_pokeball(player_profile, enemy_pokemon)
        elif action == "C":
            player_pokemon = choose_pokemon(player_profile)

        if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile):
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
