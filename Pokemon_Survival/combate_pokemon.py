import random
from Pokemon_Survival.combate_pokemon_enemy_related import enemy_attack, capture_with_pokeball
from Pokemon_Survival.combate_pokemon_play_related import load_game, delete_play, save_game
from Pokemon_Survival.combate_pokemon_player_related import any_player_pokemon_lives, get_inventory_info, player_attack, \
    get_player_profile, item_lottery, add_actual_combat
from Pokemon_Survival.combate_pokemon_pokemon_related import choose_pokemon, get_pokemon_info, cure_pokemon, \
    assign_experience
from Pokemon_Survival.pokeload import get_all_pokemons


def fight(player_profile, enemy_pokemon):
    print("\n--- NUEVO COMBATE ---")

    attack_history = []
    print(f"Vas a luchar contra: {enemy_pokemon['name']}")
    player_pokemon = choose_pokemon(player_profile)
    # print(f"\nContrincantes: {get_pokemon_info(player_pokemon)} VS {get_pokemon_info(enemy_pokemon)}")

    its_captured = False
    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0 and not its_captured:
        action = "mondongo"
        print(f"\nContrincantes: {get_pokemon_info(player_pokemon)} VS "
              f"{get_pokemon_info(enemy_pokemon, True, player_profile)}")
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
            enemy_attack(player_pokemon, enemy_pokemon)  # Para que al cambiar de pokémon se efectúe el ataque enemigo.

        if player_pokemon["current_health"] <= 0 and any_player_pokemon_lives(player_profile):
            for pokemon in player_profile["pokemon_inventory"]:
                if pokemon["name"] == player_pokemon["name"]:
                    pokemon["current_health"] = 0  # Para que la salud del Pokémon muerto sea 0 sí o sí
                    break
            player_pokemon = choose_pokemon(player_profile)

    if player_pokemon["current_health"] > 0:
        print("¡Has ganado!")
        assign_experience(attack_history)

    print("--- FIN DEL COMBATE ---")
    input("\nPresiona ENTER para continuar...")


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


def main():
    isResumed = False
    isGameEnded = False
    if YesOrNo("¿Desea cargar partida? [S/N]: "):
        isResumed = True
        data = load_game()
        delete_play()

    while True:
        if isResumed and data:
            pokemon_list = data[0]
            player_profile = data[1]
            data = None
        else:
            pokemon_list = get_all_pokemons()
            player_profile = get_player_profile(pokemon_list)

        while any_player_pokemon_lives(player_profile):
            if isResumed and data:
                enemy_pokemon = data[2]
            else:
                enemy_pokemon = random.choice(pokemon_list)

            fight(player_profile, enemy_pokemon)
            if any_player_pokemon_lives(player_profile):
                item_lottery(player_profile)
            add_actual_combat(player_profile)

            isResumed = False

            if not YesOrNo("¿Desea seguir o guardar y salir? [S/N]: ") and not any_player_pokemon_lives(player_profile):
                sorted_data = [pokemon_list, player_profile, enemy_pokemon]
                save_game(sorted_data)
                isGameEnded = True
                break

        print(f"Has perdido en el combate nº{player_profile['combats']}")

        if not isGameEnded:
            if not YesOrNo("¿Desea volverlo a intentar? [S/N]: "):
                break


if __name__ == "__main__":
    main()
