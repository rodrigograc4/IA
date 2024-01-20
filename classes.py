import math
from collections import Counter
import random



                                                                                                                        
# ██████  ██ ███████ ████████  █████  ███    ██  ██████ ███████ 
# ██   ██ ██ ██         ██    ██   ██ ████   ██ ██      ██      
# ██   ██ ██ ███████    ██    ███████ ██ ██  ██ ██      █████   
# ██   ██ ██      ██    ██    ██   ██ ██  ██ ██ ██      ██      
# ██████  ██ ███████    ██    ██   ██ ██   ████  ██████ ███████                                                                                                                                     


class Distance:
    @staticmethod
    def calculate_distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)                       # Calculate Distance between two points




# ███████ ███    ██ ███████ ███    ███ ██    ██ 
# ██      ████   ██ ██      ████  ████  ██  ██  
# █████   ██ ██  ██ █████   ██ ████ ██   ████   
# ██      ██  ██ ██ ██      ██  ██  ██    ██    
# ███████ ██   ████ ███████ ██      ██    ██    
                                                        

class Enemy:
    @staticmethod
    def attack_range(enemy_name):
        if enemy_name == "Fygar":
            attack_range = 2.0                     # Fygar Attack range
        elif enemy_name == "Pooka":
            attack_range = 3.0                      # Pooka Attack Range
        else:
            attack_range = 3.0                      # Default Attack Range

        return attack_range

    def enemy_in_range(digdug, enemy_pos, enemy_name):
        attack_range = Enemy.attack_range(enemy_name)

        distance = Distance.calculate_distance(digdug, enemy_pos)
        return distance <= attack_range

    @staticmethod
    def move_toward_enemy(digdug, enemy):
        digdug_x, digdug_y = digdug
        enemy_x, enemy_y = enemy

        if enemy_x > digdug_x:                          # If Enemy is to the Right of DigDug, Move Right
            return "d"
        elif enemy_x < digdug_x:                        # If Enemy is to the Left of DigDug, Move Left
            return "a"
        elif enemy_y > digdug_y:                        # If Enemy is Below DigDug, Move Down
            return "s"
        elif enemy_y < digdug_y:                        # If Enemy is Above DigDug, Move Up
            return "w"
        else:
            print("\n MOVE TOWARD ENEMY FAIL \n")
            return None




# ██████   ██████   ██████ ██   ██ 
# ██   ██ ██    ██ ██      ██  ██  
# ██████  ██    ██ ██      █████   
# ██   ██ ██    ██ ██      ██  ██  
# ██   ██  ██████   ██████ ██   ██ 


class Rock:
    @staticmethod
    def rock_above_digdug(digdug, rock_pos):
        digdug_x, digdug_y = digdug
        rock_x, rock_y = rock_pos

        return digdug_x == rock_x and digdug_y-2 == rock_y

    @staticmethod
    def dont_go_below_rock(digdug, enemy_pos):
        digdug_x, digdug_y = digdug
        enemy_x, enemy_y = enemy_pos

        if enemy_x > digdug_x:
            return "d"
        elif enemy_x < digdug_x:
            return "a"
        elif enemy_y > digdug_y:
            return "s"
        elif enemy_y < digdug_y:
            Move_Twice.move_up = True
            Move_Three.move_up = True
            print("DONT GO BELOW ROCK")
            return random.choice(["a", "d"])
        else:
            print("DONT GO BELOW ROCK FAIL")
            

    @staticmethod
    def rock_in_range(digdug, rock_pos):
        rock_range = 2                                                # Rock Range
        distance = Distance.calculate_distance(digdug, rock_pos)
        return distance < rock_range

    @staticmethod
    def avoid_rocks(digdug, enemy, rocks):
        digdug_x, digdug_y = digdug
        enemy_x, enemy_y = enemy

        valid_moves = []

        for rock in rocks:
            rock_x, rock_y = rock["pos"]

            if digdug_x < rock_x:
                if enemy_y <= digdug_y:
                    valid_moves.append("w")
                elif enemy_y > digdug_y:
                    valid_moves.append("s")
            elif digdug_x > rock_x:
                if enemy_y <= digdug_y:
                    valid_moves.append("w")
                elif enemy_y > digdug_y:
                    valid_moves.append("s")
            elif digdug_y < rock_y:
                if enemy_x <= digdug_x:
                    valid_moves.append("a")
                elif enemy_x > digdug_x:
                    valid_moves.append("d")
            elif digdug_y > rock_y:
                if enemy_x <= digdug_x:
                    valid_moves.append("a")
                elif enemy_x > digdug_x:
                    valid_moves.append("d")

        # Choose a valid move randomly from the list
        if valid_moves:
            return random.choice(valid_moves)
        else:
            # If no valid move is found, return None
            print("\n AVOID ROCKS FAIL \n")
            return None



            
# ███████ ██ ██████  ███████ 
# ██      ██ ██   ██ ██      
# █████   ██ ██████  █████   
# ██      ██ ██   ██ ██      
# ██      ██ ██   ██ ███████             


class Fire:
    previous_fygar_positions = []
    previous_pos = None

    @staticmethod
    def update_previous_fygar_positions(enemy):
        Fire.previous_pos = Fire.get_previous_position()
        Fire.previous_fygar_positions.append(tuple(enemy))

    @staticmethod
    def get_previous_position():
        if not Fire.previous_fygar_positions:
            return None
        return Fire.previous_fygar_positions[-1]
    
    @staticmethod
    def previous_fygar_position(enemy):
        if enemy is None:
            return (9, 9)  # No movement

        current_pos = enemy

        if Fire.previous_pos is None:
            return (9, 9)  # Default to (0, 0) if not found

        dx = current_pos[0] - Fire.previous_pos[0]
        dy = current_pos[1] - Fire.previous_pos[1]

        return (dx, dy)

    @staticmethod
    def fire_in_range(digdug, enemies):
        digdug_x, digdug_y = digdug
        for enemy in enemies:
            if enemy["name"] == "Fygar" and "fire" in enemy:
                fygar_pos = enemy["pos"]
                fygar_direction = Fire.previous_fygar_position(fygar_pos)
                
                # Check if Fygar is moving to the left or right
                if fygar_direction[0] == -1 and digdug_y == fygar_pos[1]:  # Fygar is moving left
                    return fygar_pos[0] >= digdug[0] and fygar_pos[0] - digdug[0] <= 6.0
                elif fygar_direction[0] == 1 and digdug_y == fygar_pos[1]:  # Fygar is moving right
                    return fygar_pos[0] <= digdug[0] and digdug[0] - fygar_pos[0] <= 6.0
                elif fygar_direction[0] == 0 and digdug_y == fygar_pos[1]:  # Fygar está parado
                    return abs(digdug[0] - fygar_pos[0]) <= 5.0

        return False
    
    @staticmethod
    def avoid_fire(digdug, enemies):
        digdug_x, digdug_y = digdug
        enemy_x, enemy_y = enemies[0]["pos"]

        if digdug_y == enemy_y:                        # If DigDug is in the same Y as the Enemy
            return "s"
        elif digdug_y != enemy_y:                        # If DigDug is not in the same Y as the Enemy
            if enemy_x > digdug_x:                          # If Enemy is to the Right of DigDug, Move Left
                return "a"
            elif enemy_x < digdug_x:                        # If Enemy is to the Left of DigDug, Move Right
                return "d"
        else:
            print("\n AVOID FIRE FAIL \n")
            return None




# ██     ██  █████  ██      ██      ██████   █████  ███████ ███████ ██ ███    ██  ██████  
# ██     ██ ██   ██ ██      ██      ██   ██ ██   ██ ██      ██      ██ ████   ██ ██       
# ██  █  ██ ███████ ██      ██      ██████  ███████ ███████ ███████ ██ ██ ██  ██ ██   ███ 
# ██ ███ ██ ██   ██ ██      ██      ██      ██   ██      ██      ██ ██ ██  ██ ██ ██    ██ 
#  ███ ███  ██   ██ ███████ ███████ ██      ██   ██ ███████ ███████ ██ ██   ████  ██████  
                                                                                       

class Wallpassing:
    @staticmethod
    def pooka_wallpassing(digdug, enemies):
        for enemy in enemies:
            if enemy["name"] == "Pooka" and "traverse" in enemy:
                return Distance.calculate_distance(digdug, enemy["pos"]) <= 5.0
        return False

    @staticmethod
    def avoid_wallpassing(digdug, enemies):
        digdug_x, digdug_y = digdug
        enemy_x, enemy_y = enemies[0]["pos"]

        if enemy_x > digdug_x:                          # If Enemy is to the Right of DigDug, Move Left
            return "a"
        elif enemy_x < digdug_x:                        # If Enemy is to the Left of DigDug, Move Right
            return "d"
        elif enemy_y > digdug_y:                        # If Enemy is Below DigDug, Move UP
            return "w"
        elif enemy_y < digdug_y:                        # If Enemy is Above DigDug, Move Down
            return "s"
        else:
            print("\n AVOID WALLPASSING FAIL \n")
            return None




#  █████  ████████ ████████  █████   ██████ ██   ██ 
# ██   ██    ██       ██    ██   ██ ██      ██  ██  
# ███████    ██       ██    ███████ ██      █████   
# ██   ██    ██       ██    ██   ██ ██      ██  ██  
# ██   ██    ██       ██    ██   ██  ██████ ██   ██ 


class Attack:
    @staticmethod
    def attack_enemy(digdug, enemy_pos, enemy_name):
        if enemy_name == "Fygar":
            return Attack.attack_fygar(digdug, enemy_pos)                   # Fygar Attack
        elif enemy_name == "Pooka":
            return Attack.attack_pooka(digdug, enemy_pos)                   # Pooka Attack
        else:
            return Attack.default_attack                                    # Default Attack
    
    @staticmethod
    def attack_pooka(digdug, enemy_pos):
        digdug_x, digdug_y = digdug
        enemy_x, enemy_y = enemy_pos

        if FixDirection.correct_direction(digdug, enemy_pos):                       # If DigDug is facing the wrong direction, fix it
            return FixDirection.fix_attack_direction(digdug, enemy_pos)
            
        return "A"                                      # Pooka Attack
    
    @staticmethod
    def attack_fygar(digdug, enemy_pos):
        digdug_x, digdug_y = digdug
        enemy_x, enemy_y = enemy_pos
        
        if FixDirection.correct_direction(digdug, enemy_pos):                       # If DigDug is facing the wrong direction, fix it
            return FixDirection.fix_attack_direction(digdug, enemy_pos)
            
        return "A"                                      # Fygar Attack

    @staticmethod
    def default_attack():
        return "A"                                      # Default Attack




# ███████ ██ ██   ██     ██████  ██ ██████  ███████  ██████ ████████ ██  ██████  ███    ██ 
# ██      ██  ██ ██      ██   ██ ██ ██   ██ ██      ██         ██    ██ ██    ██ ████   ██ 
# █████   ██   ███       ██   ██ ██ ██████  █████   ██         ██    ██ ██    ██ ██ ██  ██ 
# ██      ██  ██ ██      ██   ██ ██ ██   ██ ██      ██         ██    ██ ██    ██ ██  ██ ██ 
# ██      ██ ██   ██     ██████  ██ ██   ██ ███████  ██████    ██    ██  ██████  ██   ████ 


class FixDirection:
    previous_digdug_positions = []
    previous_pos = None
    previous_digdug_directions = []

    @staticmethod
    def update_previous_digdug_positions(digdug):
        FixDirection.previous_pos = FixDirection.get_previous_position()
        FixDirection.previous_digdug_positions.append(tuple(digdug))

    @staticmethod
    def get_previous_position():
        if not FixDirection.previous_digdug_positions:
            return None
        return FixDirection.previous_digdug_positions[-1]
    
    @staticmethod
    def previous_digdug_direction(digdug):
        if digdug is None:
            return (9, 9)  # No movement

        current_pos = digdug

        if FixDirection.previous_pos is None:
            return (9, 9)  # Default to (0, 0) if not found

        dx = current_pos[0] - FixDirection.previous_pos[0]
        dy = current_pos[1] - FixDirection.previous_pos[1]

        if (dx, dy) != (0, 0):
            FixDirection.previous_digdug_directions.append(tuple((dx, dy)))

    @staticmethod
    def correct_direction(digdug, enemy_pos):
        digdug_x, digdug_y = digdug
        enemy_x, enemy_y = enemy_pos

        FixDirection.previous_digdug_direction(digdug)
        if FixDirection.previous_digdug_directions:
            last_direction = FixDirection.previous_digdug_directions[-1]

            if last_direction is not None:
                # Check if the last movement direction is consistent with the direction towards the enemy
                if enemy_y - digdug_y in [-1,-2,-3] and not last_direction == (0, -1) and enemy_x == digdug_x:  # Moving up
                    return True
                elif enemy_y - digdug_y in [1,2,3] and not last_direction == (0, 1) and enemy_x == digdug_x:  # Moving down
                    return True
                elif enemy_x - digdug_x in [-1,-2,-3] and not last_direction == (-1, 0) and enemy_y == digdug_y:  # Moving left
                    return True
                elif enemy_x - digdug_x in [1,2,3] and not last_direction == (1, 0) and enemy_y == digdug_y:  # Moving right
                    return True
            else:
                return False # No fix needed    
        else:
            return False
            
    
    @staticmethod
    def fix_attack_direction(digdug, enemy_pos):
        digdug_x, digdug_y = digdug
        enemy_x, enemy_y = enemy_pos

        if Borders.check_borders(digdug):
            return Borders.fix_borders(digdug)
        else:
            if enemy_y - digdug_y in [-1,-2,-3] :
                # Moving up towards the enemy
                return "s" # Move down 
            elif enemy_y - digdug_y in [1,2,3] :
                # Moving down towards the enemy
                return "w" # Move up
            elif enemy_x - digdug_x in [-1,-2,-3] :
                # Moving left towards the enemy
                return "d"  # Move right
            elif enemy_x - digdug_x in [1,2,3] :
                # Moving right towards the enemy
                return "a"  # Move left
            else:
                print("\n FIX DIRECTION FAIL \n")
                return []  # No fix needed
        



# ██████   ██████  ██████  ██████  ███████ ██████  ███████ 
# ██   ██ ██    ██ ██   ██ ██   ██ ██      ██   ██ ██      
# ██████  ██    ██ ██████  ██   ██ █████   ██████  ███████ 
# ██   ██ ██    ██ ██   ██ ██   ██ ██      ██   ██      ██ 
# ██████   ██████  ██   ██ ██████  ███████ ██   ██ ███████


class Borders:
    @staticmethod
    def check_borders(digdug):
        digdug_x, digdug_y = digdug
        if digdug_x == 0 and digdug_y == 0:
            return False
        elif digdug_x == 0:                            # If DigDug is at the Left Border
            return True
        elif digdug_x == 47:                         # If DigDug is at the Right Border
            return True
        elif digdug_y == 0:                          # If DigDug is at the Top Border
            return True
        elif digdug_y == 23:                         # If DigDug is at the Bottom Border, Move Up
            return True
        else:
            return False                             # If DigDug is not at any Border, Stay
        
    @staticmethod
    def fix_borders(digdug):
        digdug_x, digdug_y = digdug
        if digdug_x == 0:                            # If DigDug is at the Left Border
            Move_Twice.move_right = True
            return "s"
        elif digdug_x == 47:                         # If DigDug is at the Right Border
            Move_Twice.move_left = True
            return "w"
        elif digdug_y == 0:                          # If DigDug is at the Top Border
            Move_Twice.move_down = True
            return "a"
        elif digdug_y == 23:                         # If DigDug is at the Bottom Border
            Move_Twice.move_up = True
            return "d"
        else:
            return []                                # If DigDug is not at any Border, Stay
        



# ███    ███  ██████  ██    ██ ███████     ████████ ██     ██ ██  ██████ ███████ 
# ████  ████ ██    ██ ██    ██ ██             ██    ██     ██ ██ ██      ██      
# ██ ████ ██ ██    ██ ██    ██ █████          ██    ██  █  ██ ██ ██      █████   
# ██  ██  ██ ██    ██  ██  ██  ██             ██    ██ ███ ██ ██ ██      ██      
# ██      ██  ██████    ████   ███████        ██     ███ ███  ██  ██████ ███████


class Move_Twice:
    move_right = False
    move_left = False
    move_up = False
    move_down = False

    @staticmethod
    def check_move_twice():
        if Move_Twice.move_right == True:
            return True
        elif Move_Twice.move_left == True:
            return True
        elif Move_Twice.move_up == True:
            return True
        elif Move_Twice.move_down == True:
            return True
        else:
            return False

    @staticmethod
    def second_move():
        if Move_Twice.move_right == True:
            Move_Twice.move_right = False
            return "d"
        elif Move_Twice.move_left == True:
            Move_Twice.move_left = False
            return "a"
        elif Move_Twice.move_up == True:
            Move_Twice.move_up = False
            return "w"
        elif Move_Twice.move_down == True:
            Move_Twice.move_down = False
            return "s"
        else:
            return False




# ███    ███  ██████  ██    ██ ███████     ████████ ██   ██ ██████  ███████ ███████ 
# ████  ████ ██    ██ ██    ██ ██             ██    ██   ██ ██   ██ ██      ██      
# ██ ████ ██ ██    ██ ██    ██ █████          ██    ███████ ██████  █████   █████   
# ██  ██  ██ ██    ██  ██  ██  ██             ██    ██   ██ ██   ██ ██      ██      
# ██      ██  ██████    ████   ███████        ██    ██   ██ ██   ██ ███████ ███████ 


class Move_Three:
    move_up = False

    @staticmethod
    def check_move_three():
        if Move_Three.move_up == True:
            return True
        else:
            return False

    @staticmethod
    def third_move():
        if Move_Three.move_up == True:
            Move_Three.move_up = False
            print("\n MOVE THREE \n")
            return "w"
        else:
            print("\n MOVE THREE FAIL \n")
            return False




#  ██████  █████  ███    ███ ██████  ██ ███    ██  ██████  
# ██      ██   ██ ████  ████ ██   ██ ██ ████   ██ ██       
# ██      ███████ ██ ████ ██ ██████  ██ ██ ██  ██ ██   ███ 
# ██      ██   ██ ██  ██  ██ ██      ██ ██  ██ ██ ██    ██ 
#  ██████ ██   ██ ██      ██ ██      ██ ██   ████  ██████ 


class Camping:
    all_enemy_positions = {}

    @staticmethod
    def add_enemy_positions(enemies):
        for enemy in enemies:
            enemy_id = enemy["id"]
            enemy_pos = tuple(enemy["pos"])  # Convert list to tuple

            # Check if the enemy is already in the dictionary
            if enemy_id in Camping.all_enemy_positions:
                # Append the current position to the existing list
                Camping.all_enemy_positions[enemy_id].append(enemy_pos)
            else:
                # Create a new list with the current position
                Camping.all_enemy_positions[enemy_id] = [enemy_pos]

            # Keep only the last positions
            if len(Camping.all_enemy_positions[enemy_id]) > 70:
                Camping.all_enemy_positions[enemy_id] = Camping.all_enemy_positions[enemy_id][-70:]

    @staticmethod
    def check_enemy_positions(digdug, enemy_id):
        # Get the last 70 positions of the enemy
        last_70_positions = Camping.all_enemy_positions.get(enemy_id, [])[-70:]
        
        # Count the occurrences of each position in the last 70 positions
        position_counts = Counter(last_70_positions)

        if len(last_70_positions) < 70:
            return False
        elif len(last_70_positions) == 70:
            # Check if any position has occurred at least 3 times
            for count in position_counts.values():
                if count >= 3:
                    Camping.create_camping_spot(digdug, enemy_id)
                    return True  # At least one enemy has at least 3 identical positions in the last 70 positions
        else:
            return False  # No enemy has at least 3 identical positions in the last 70 positions
        
    @staticmethod
    def create_camping_spot(digdug, enemy_id):
        digdug_x, digdug_y = digdug
        last_70_positions = Camping.all_enemy_positions.get(enemy_id, [])[-70:]

        if len(last_70_positions) == 70:
        # Check if all positions are in the same horizontal or vertical line
            is_horizontal = all(pos[1] == last_70_positions[0][1] for pos in last_70_positions)
            is_vertical = all(pos[0] == last_70_positions[0][0] for pos in last_70_positions)
        else:
            return None # Not enough positions to determine if horizontal or vertical

        min_x = min(pos[0] for pos in last_70_positions)
        min_y = min(pos[1] for pos in last_70_positions)
        max_x = max(pos[0] for pos in last_70_positions)
        max_y = max(pos[1] for pos in last_70_positions)

        if is_horizontal:
            if digdug_x <= min_x:
                if digdug_y < min_y:
                    camping_spot = (min_x, min_y-1)
                    return camping_spot
                elif digdug_y > min_y:
                    camping_spot = (min_x, min_y+1)
                    return camping_spot
                elif digdug_y == min_y:
                    camping_spot = (min_x-1, digdug_y)
                    return camping_spot
            elif digdug_x > min_x:
                if digdug_y < max_y:
                    camping_spot = (max_x, max_y-1)
                    return camping_spot
                elif digdug_y > max_y:
                    camping_spot = (max_x, max_y+1)
                    return camping_spot
                elif digdug_y == max_y:
                    camping_spot = (max_x+1, digdug_y)
                    return camping_spot
        elif is_vertical:
            if digdug_y < min_y:
                camping_spot = (min_x, min_y-1)
                return camping_spot
            elif digdug_y > max_y:
                camping_spot = (max_x, max_y+1)
                return camping_spot
            else:
                if digdug_x < min_x:
                    camping_spot = (min_x-1, digdug_y)
                    return camping_spot
                elif digdug_x > max_x:
                    camping_spot = (min_x+1, digdug_y)
                    return camping_spot
                elif digdug_x == max_x:
                    if digdug_y < min_y:
                        camping_spot = (min_x, min_y-1)
                        return camping_spot
                    elif digdug_y > min_y:
                        camping_spot = (min_x, max_y+1)
                        return camping_spot
        else:
            return None  # No camping spot found
    
    @staticmethod
    def move_to_camping_spot(digdug, enemy_id, enemy_pos, enemy_name):
        digdug_x, digdug_y = digdug
        camping_spot = Camping.create_camping_spot(digdug, enemy_id)

        if camping_spot is not None:
            spot_x, spot_y = camping_spot
            if spot_x > digdug_x:    # If Camping Spot is to the Right of DigDug, Move Right
                return "d"
            elif spot_x < digdug_x:  # If Camping Spot is to the Left of DigDug, Move Left
                return "a"
            elif spot_y > digdug_y:  # If Camping Spot is Below DigDug, Move Down
                return "s"
            elif spot_y < digdug_y:  # If Camping Spot is Above DigDug, Move Up
                return "w"
            elif spot_x == digdug_x and spot_y == digdug_y:
                return Camping.is_in_camping_spot(digdug, enemy_id)
        else:
            return None              # If no Camping Spot, Stay

    
    @staticmethod
    def is_in_camping_spot(digdug, enemy_id):
        digdug_x, digdug_y = digdug
        camping_spot = Camping.create_camping_spot(digdug, enemy_id)

        if camping_spot is not None:
            spot_x, spot_y = camping_spot

            if spot_x == digdug_x and spot_y == digdug_y:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def rock_in_camp_spot(rock, digdug, enemy_id):
        rock_x, rock_y = rock
        camping_spot = Camping.create_camping_spot(digdug, enemy_id)

        if camping_spot is not None:
            spot_x, spot_y = camping_spot

            if spot_x == rock_x and (spot_y == rock_y or spot_y == rock_y + 1) :
                return True
            else:
                return False
        else:
            return False




# ███████ ███    ██ ███████ ███    ███ ██    ██     ███████ ████████ ██    ██  ██████ ██   ██ 
# ██      ████   ██ ██      ████  ████  ██  ██      ██         ██    ██    ██ ██      ██  ██  
# █████   ██ ██  ██ █████   ██ ████ ██   ████       ███████    ██    ██    ██ ██      █████   
# ██      ██  ██ ██ ██      ██  ██  ██    ██             ██    ██    ██    ██ ██      ██  ██  
# ███████ ██   ████ ███████ ██      ██    ██        ███████    ██     ██████   ██████ ██   ██


class EnemyStuck:
    @staticmethod
    def check_enemy_stuck(enemy_id):
        last_70_positions = Camping.all_enemy_positions.get(enemy_id, [])[-70:]

        if len(last_70_positions) < 70:
            return False
        elif len(set(last_70_positions)) <= 3:
        # Se houver 1 ou 2 valores únicos nas últimas 70 posições
            print("ENEMY STUCK")
            return True
        else:
            return False
    
    @staticmethod
    def close_attack(enemy_name):
        if enemy_name == "Fygar":
            attack_range = 1.0                      # Fygar Attack range
        elif enemy_name == "Pooka":
            attack_range = 1.0                      # Pooka Attack Range
        else:
            attack_range = 2.0                      # Default Attack Range

        return attack_range

    def stuck_enemy_in_range(digdug, enemy_pos, enemy_name):
        attack_range = EnemyStuck.close_attack(enemy_name)

        distance = Distance.calculate_distance(digdug, enemy_pos)
        return distance <= attack_range

    @staticmethod
    def move_toward_stuck_enemy(digdug, enemy):
        digdug_x, digdug_y = digdug
        enemy_x, enemy_y = enemy

        if enemy_x > digdug_x:                          # If Enemy is to the Right of DigDug, Move Right
            return "d"
        elif enemy_x < digdug_x:                        # If Enemy is to the Left of DigDug, Move Left
            return "a"
        elif enemy_y > digdug_y:                        # If Enemy is Below DigDug, Move Down
            return "s"
        elif enemy_y < digdug_y:                        # If Enemy is Above DigDug, Move Up
            return "w"
        else:
            print("\n MOVE TOWARD ENEMY FAIL \n")
            return None