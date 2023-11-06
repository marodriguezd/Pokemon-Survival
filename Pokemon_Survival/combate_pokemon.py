import random

from Pokemon_Survival.combate_pokemon_enemy_related import enemy_attack, capture_with_pokeball
from Pokemon_Survival.combate_pokemon_player_related import any_player_pokemon_lives, get_inventory_info, player_attack, \
    get_player_profile, item_lottery
from Pokemon_Survival.combate_pokemon_pokemon_related import choose_pokemon, get_pokemon_info, cure_pokemon, \
    assign_experience
from pokeload import get_all_pokemons


def fight(player_profile, enemy_pokemon):
    print("\n--- NUEVO COMBATE ---")

    attack_history = []
    print(f"Vas a luchar contra: {enemy_pokemon['name']}")
    player_pokemon = choose_pokemon(player_profile)
    # print(f"\nContrincantes: {get_pokemon_info(player_pokemon)} VS {get_pokemon_info(enemy_pokemon)}")

    its_captured = False
    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0 and not its_captured:
        action = "mondongo"
        print(f"\nContrincantes: {get_pokemon_info(player_pokemon)} VS {get_pokemon_info(enemy_pokemon)}")
        print(f"\nInventario: {get_inventory_info(player_profile)}")
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
            its_captured = capture_with_pokeball(player_profile, enemy_pokemon)
        elif action.upper() == "C":
            player_pokemon = choose_pokemon(player_profile)

        if player_pokemon["current_health"] <= 0 and any_player_pokemon_lives(player_profile):
            player_pokemon["current_health"] = 0  # Para que la salud del Pokémon muerto sea 0 sí o sí
            player_pokemon = choose_pokemon(player_profile)

    if player_pokemon["current_health"] > 0:
        print("¡Has ganado!")
        assign_experience(attack_history)

    print("--- FIN DEL COMBATE ---")
    input("\nPresiona ENTER para continuar...")


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
