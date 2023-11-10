import random
from Pokemon_Survival.combate_pokemon_enemy_related import enemy_attack, capture_with_pokeball
from Pokemon_Survival.combate_pokemon_play_related import load_game, delete_play, save_game
from Pokemon_Survival.combate_pokemon_player_related import any_player_pokemon_lives, get_inventory_info, player_attack, \
    get_player_profile, item_lottery, add_actual_combat
from Pokemon_Survival.combate_pokemon_pokemon_related import choose_pokemon, get_pokemon_info, cure_pokemon, \
    assign_experience
from Pokemon_Survival.pokeload import get_all_pokemons


def print_actual_battle_and_stats(player_pokemon, enemy_pokemon, player_profile):
    print(f"\nContrincantes: {get_pokemon_info(player_pokemon)} VS "
          f"{get_pokemon_info(enemy_pokemon, True, player_profile)}")
    print(f"\nInventario: {get_inventory_info(player_profile)}")


def user_action_in_game(action, player_pokemon, enemy_pokemon, attack_history, player_profile):
    enemy_can_attack = True

    if action.upper() == "A":
        player_attack(player_pokemon, enemy_pokemon)
        attack_history.append(player_pokemon)
    elif action.upper() == "V":
        cure_pokemon(player_profile, player_pokemon)
    elif action.upper() == "P":
        its_captured = capture_with_pokeball(player_profile, enemy_pokemon)
        if its_captured:
            enemy_can_attack = False
    elif action.upper() == "C":
        player_pokemon = choose_pokemon(player_profile)

    return [enemy_can_attack, player_pokemon]


def player_pokemon_is_dead(player_profile, player_pokemon):
    for pokemon in player_profile["pokemon_inventory"]:
        if pokemon["current_health"] < 0:
            pokemon["current_health"] = 0  # Para que la salud del Pokémon muerto sea 0 sí o sí

    print(f"\n¡Han matado a {player_pokemon['name']}!")


def fight(player_profile, enemy_pokemon):
    print("\n--- NUEVO COMBATE ---")

    attack_history = []
    print(f"Vas a luchar contra: {enemy_pokemon['name']}")
    player_pokemon = choose_pokemon(player_profile)

    its_captured = False
    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0 and not its_captured:
        print_actual_battle_and_stats(player_pokemon, enemy_pokemon, player_profile)

        action = ""  # Para poder empezar
        while action.upper() not in ["A", "P", "V", "C"]:
            action = input("¿Qué desea hacer?: "
                           "[A]tacar, "
                           "[P]okeball, "
                           "Poción de [V]ida, "
                           "[C]ambiar: ")

        reaction_to_user_actions = user_action_in_game(action, player_pokemon, enemy_pokemon, attack_history, player_profile)
        if reaction_to_user_actions[1] != player_pokemon:
            player_pokemon = reaction_to_user_actions[1]
        if reaction_to_user_actions[0]:
            enemy_attack(player_pokemon, enemy_pokemon)
        else:
            break  # Para salir si ha sido capturado ya que es la única vez que no ataca

        if player_pokemon["current_health"] <= 0 and any_player_pokemon_lives(player_profile):
            player_pokemon_is_dead(player_profile, player_pokemon)
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


def game_loader(pokemon_list):
    if YesOrNo("\n¿Desea cargar partida? [S/N]: "):
        data = load_game()
        if data is not None:
            delete_play()
            return data

    return get_player_profile(pokemon_list)


def main():
    isGameEnded = False
    pokemon_list = get_all_pokemons()
    player_profile = game_loader(pokemon_list)

    while not isGameEnded:

        # Main game loop
        while any_player_pokemon_lives(player_profile) and not isGameEnded:
            enemy_pokemon = random.choice(pokemon_list)

            fight(player_profile, enemy_pokemon)
            if any_player_pokemon_lives(player_profile):
                item_lottery(player_profile)
            add_actual_combat(player_profile)

            if any_player_pokemon_lives(player_profile) and not YesOrNo("¿Desea seguir o guardar y salir? [S/N]: "):
                isGameEnded = True
                save_game(player_profile)

        print(f"\nHas terminado en el combate nº{player_profile['combats']}")

        if not isGameEnded:
            if not YesOrNo("¿Desea volverlo a intentar? [S/N]: "):
                break

        input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    main()
