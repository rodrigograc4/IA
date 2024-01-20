import asyncio
import getpass
import json
import os
import math
import random
import websockets
from classes import *


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        while True:
            try:
                state = json.loads(await websocket.recv())
                if "digdug" in state and "enemies" in state:
                    key = key_maker(state)

                    await websocket.send(json.dumps({"cmd": "key", "key": key}))
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


def key_maker(state):
    if "digdug" in state and "enemies" in state:
        digdug = state["digdug"]
        enemies = state["enemies"]
        rocks = state["rocks"]

        key = make_decision(digdug, enemies, rocks)                         # Make the Decision
        if key:
            return key
        
    print("\n -------------------------------------- RANDOM KEY -------------------------------------- \n")

    possible_keys = ["w", "a", "s", "d", " "]
    return random.choice(possible_keys)



def make_decision(digdug, enemies, rocks):
    if not enemies:
        print("\n NEW LEVEL \n")
        return " "

    distances = []
    distance_rock = []
    nearest_enemy = None
    rock_distance = None
    FixDirection.update_previous_digdug_positions(digdug)                   # Update Previous DigDug Positions
    Camping.add_enemy_positions(enemies)                                    # Update Enemy Positions for Camping

    for enemy in enemies:
        distance = Distance.calculate_distance(digdug, enemy["pos"])
        distances.append((distance, enemy))                                 # Calculate Distance between DigDug and Enemy

    for rock in rocks:
        distance = Distance.calculate_distance(digdug, rock["pos"])
        distance_rock.append((distance, rock))                              # Calculate Distance between DigDug and Rock

    distances.sort(key=lambda x: x[0])
    nearest_enemy = distances[0][1]                                         # Nearest Enemy

    distance_rock.sort(key=lambda x: x[0])
    rock_distance = distance_rock[0][1]                                     # Nearest Rock
    
    Fire.update_previous_fygar_positions(nearest_enemy["pos"])              # Update Previous Fygar Positions
    
    Camping.create_camping_spot(digdug, nearest_enemy["id"])                # Create Camping Spot


    if EnemyStuck.check_enemy_stuck(nearest_enemy["id"]):                                          
        return enemy_stuck_strategy(digdug, enemies, nearest_enemy, rock_distance, rocks)                                               # If Enemy is Stuck, Do this Strategy
    elif Camping.check_enemy_positions(digdug, nearest_enemy["id"]):
        move_result = Camping.move_to_camping_spot(digdug, nearest_enemy["id"], nearest_enemy["pos"], nearest_enemy["name"])            # If possible Camping, Do this Strategy
        if move_result is not None:
            return camping_strategy(digdug, enemies, nearest_enemy, rock_distance, rocks, rock, move_result)                            # Else, Do the Default Strategy
        else:
            return default_strategy(digdug, enemies, nearest_enemy, rocks, rock_distance)
    else:
        return default_strategy(digdug, enemies, nearest_enemy, rocks, rock_distance)
        

    
def enemy_stuck_strategy(digdug, enemies, nearest_enemy, rock_distance, rocks):
    if Move_Twice.check_move_twice():                                                               # If DigDug is in a position to move twice, Move Twice
        return Move_Twice.second_move()
    elif Move_Three.check_move_three():                                                             # If DigDug is in a position to move three times, Move Three
        return Move_Three.third_move()
    elif Wallpassing.pooka_wallpassing(digdug, enemies):                                            # If Pooka is Wallpassing, Avoid it
        return Wallpassing.avoid_wallpassing(digdug, enemies)
    elif Fire.fire_in_range(digdug, enemies):                                                       # If Fygar's fire is in Range, Avoid it
        return Fire.avoid_fire(digdug, enemies)
    elif Camping.is_in_camping_spot(digdug, nearest_enemy["id"]):                                   # If DigDug is in the Camping Spot
        return Attack.attack_enemy(digdug, nearest_enemy["pos"], nearest_enemy["name"])
    elif Rock.rock_above_digdug(digdug, rock_distance["pos"]):                                      # If Rock is above DigDug, Move Away
        return Rock.dont_go_below_rock(digdug, nearest_enemy["pos"])
    elif Rock.rock_in_range(digdug, rock_distance["pos"]):                                          # If Rock is in Range, Avoid it
        return Rock.avoid_rocks(digdug, nearest_enemy["pos"], rocks)
    elif FixDirection.correct_direction(digdug, nearest_enemy["pos"]):                              # If DigDug is facing the wrong direction, fix it
        return FixDirection.fix_attack_direction(digdug, nearest_enemy["pos"])
    elif EnemyStuck.stuck_enemy_in_range(digdug, nearest_enemy["pos"], nearest_enemy["name"]):      # If Stuck Enemy is in Range, Attack it
        return Attack.attack_enemy(digdug, nearest_enemy["pos"], nearest_enemy["name"])
    else:
        return EnemyStuck.move_toward_stuck_enemy(digdug, nearest_enemy["pos"])                     # Move toward Stuck Enemy
    


def camping_strategy(digdug, enemies, nearest_enemy, rock_distance, rocks, rock, move_result):
    if Move_Twice.check_move_twice():                                                               # If DigDug is in a position to move twice, Move Twice
        return Move_Twice.second_move()
    elif Move_Three.check_move_three():                                                             # If DigDug is in a position to move three times, Move Three
        return Move_Three.third_move()
    elif Wallpassing.pooka_wallpassing(digdug, enemies):                                            # If Pooka is Wallpassing, Avoid it
        return Wallpassing.avoid_wallpassing(digdug, enemies)
    elif Fire.fire_in_range(digdug, enemies):                                                       # If Fygar's fire is in Range, Avoid it
        return Fire.avoid_fire(digdug, enemies)
    elif Camping.rock_in_camp_spot(rock, digdug, nearest_enemy["id"]):                              # If Rock is in the Camping Spot, Don't go there
        print("\n ROCK IN CAMPING SPOT \n")
        return default_strategy(digdug, enemies, nearest_enemy, rocks, rock_distance)
    elif Camping.is_in_camping_spot(digdug, nearest_enemy["id"]):                                   # If DigDug is in the Camping Spot
        return Attack.attack_enemy(digdug, nearest_enemy["pos"], nearest_enemy["name"])
    elif Rock.rock_above_digdug(digdug, rock_distance["pos"]):                                      # If Rock is above DigDug, Move Away
        return Rock.dont_go_below_rock(digdug, nearest_enemy["pos"])
    elif Rock.rock_in_range(digdug, rock_distance["pos"]):                                          # If Rock is in Range, Avoid it
        return Rock.avoid_rocks(digdug, nearest_enemy["pos"], rocks)
    elif FixDirection.correct_direction(digdug, nearest_enemy["pos"]):                              # If DigDug is facing the wrong direction, fix it
        return FixDirection.fix_attack_direction(digdug, nearest_enemy["pos"])
    elif Enemy.enemy_in_range(digdug, nearest_enemy["pos"], nearest_enemy["name"]):                 # If Enemy is in Range, Attack it
        return Attack.attack_enemy(digdug, nearest_enemy["pos"], nearest_enemy["name"])
    else:
        return move_result



def default_strategy(digdug, enemies, nearest_enemy, rocks, rock_distance):     
    if Move_Twice.check_move_twice():                                                               # If DigDug is in a position to move twice, Move Twice
        return Move_Twice.second_move()
    elif Move_Three.check_move_three():                                                             # If DigDug is in a position to move three times, Move Three
        return Move_Three.third_move()
    elif Borders.check_borders(digdug):                                                             # If DigDug is in a position to go out of bounds, Fix it
        return Borders.fix_borders(digdug)
    elif Wallpassing.pooka_wallpassing(digdug, enemies):                                            # If Pooka is Wallpassing, Avoid it
        return Wallpassing.avoid_wallpassing(digdug, enemies)
    elif Fire.fire_in_range(digdug, enemies):                                                       # If Fygar's fire is in Range, Avoid it
        return Fire.avoid_fire(digdug, enemies)
    elif Camping.is_in_camping_spot(digdug, nearest_enemy["id"]):                                   # If DigDug is in the Camping Spot
        return Attack.attack_enemy(digdug, nearest_enemy["pos"], nearest_enemy["name"])
    elif Rock.rock_above_digdug(digdug, rock_distance["pos"]):                                      # If Rock is above DigDug, Move Away
        return Rock.dont_go_below_rock(digdug, nearest_enemy["pos"])
    elif Rock.rock_in_range(digdug, rock_distance["pos"]):                                          # If Rock is in Range, Avoid it
        return Rock.avoid_rocks(digdug, nearest_enemy["pos"], rocks)
    elif FixDirection.correct_direction(digdug, nearest_enemy["pos"]):                              # If DigDug is facing the wrong direction, fix it
        return FixDirection.fix_attack_direction(digdug, nearest_enemy["pos"])
    elif Enemy.enemy_in_range(digdug, nearest_enemy["pos"], nearest_enemy["name"]):                 # If Enemy is in Range, Attack it
        return Attack.attack_enemy(digdug, nearest_enemy["pos"], nearest_enemy["name"])
    elif Enemy.enemy_in_range(digdug, nearest_enemy["pos"], nearest_enemy["name"]) == False: 
        return Enemy.move_toward_enemy(digdug, nearest_enemy["pos"])                                # If None of the above, Move toward Enemy
    else:
        print("\n END OF IFS \n")
        return None
    


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
