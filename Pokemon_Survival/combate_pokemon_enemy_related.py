import random

from Pokemon_Survival.combate_pokemon_pokemon_related import pokemon_attacks_in_its_level


def enemy_attack(player_pokemon, enemy_pokemon):
    if enemy_pokemon["current_health"] > 0:
        enemy_attacks = pokemon_attacks_in_its_level(enemy_pokemon["attacks"], player_pokemon["level"])

        enemy_attack_selection = random.choice(enemy_attacks)

        enemy_damage_with_type_percentage_applied = int(enemy_attack_selection['damage'].replace("--", "0")) * \
                                                    multiplier_type_calculator(player_pokemon, enemy_pokemon)

        player_pokemon["current_health"] -= enemy_damage_with_type_percentage_applied


def capture_with_pokeball(player_profile, enemy_pokemon):
    if player_profile["pokeballs"] > 0 and len(player_profile["pokemon_inventory"]) < 6:
        base_probability = 0.10
        final_probability = 0

        if enemy_pokemon["current_health"] > 90:
            final_probability = base_probability * 1
        if enemy_pokemon["current_health"] > 80:
            final_probability = base_probability * 2
        if enemy_pokemon["current_health"] > 70:
            final_probability = base_probability * 3
        if enemy_pokemon["current_health"] > 60:
            final_probability = base_probability * 4
        if enemy_pokemon["current_health"] > 50:
            final_probability = base_probability * 5
        if enemy_pokemon["current_health"] > 40:
            final_probability = base_probability * 6
        if enemy_pokemon["current_health"] > 30:
            final_probability = base_probability * 7
        if enemy_pokemon["current_health"] > 20:
            final_probability = base_probability * 8
        if enemy_pokemon["current_health"] > 10:
            final_probability = base_probability * 9

        capture_rate = random.random()
        player_profile["pokeballs"] -= 1

        if capture_rate <= final_probability:
            player_profile["pokemon_inventory"].append(enemy_pokemon)
            print("¡Lo has capturado!")
            return True
        else:
            print("¡La captura falló!")
            return False
    elif len(player_profile["pokemon_inventory"]) < 6:
        print("¡Ya tienes la máxima cantidad de Pokémons en el inventario!")
    else:
        print(f"¡No tienes Pokeballs para capturar a {enemy_pokemon['name']}!")
        return False


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
