
def determine_position(sensor_list, direction):
    if sensor_list == [1, 1, 1, 1, 1, 1, 1, 1, 1] or sensor_list == [0, 0, 0, 0, 0, 0, 0, 0, 0]:
        return "Derailed - Motors stopped"

    if detect_fork(sensor_list) == True:
        # if we are turning right
        if direction == True:
            fork_list = [0, 0, 0, 0, 1, 1, 1, 1, 0]  
        # we must be turning left then
        else:
            fork_list = [0, 1, 1, 1, 1, 0, 0, 0, 0] 
        print("At fork")
    elif detect_fork(sensor_list) == False:
        fork_list = sensor_list
    print("forklist: ", fork_list)

    # Basic movement cases
    movement_patterns = {
        (0, 0, 0, 1, 1, 1, 0, 0, 0): "In the middle - Motors equal",
    }
    
    # Straying left
    straying_left_patterns = {
        (0, 0, 0, 0, 1, 1, 1, 0, 0): "Straying left slightly)",
        (0, 0, 0, 1, 1, 1, 1, 0, 0): "Straying left slightly",

        (0, 0, 0, 0, 0, 1, 1, 1, 0): "Straying left",
        (0, 0, 0, 0, 1, 1, 1, 1, 0): "Straying left",

        (0, 0, 0, 0, 0, 0, 1, 1, 1): "Straying left considerably",
        (0, 0, 0, 0, 0, 1, 1, 1, 1): "Straying left considerably",

        (0, 0, 0, 0, 0, 0, 0, 1, 1): "Straying very far left",
        (0, 0, 0, 0, 0, 0, 0, 0, 1): "Almost off track left",
    }
    
    # Straying right
    straying_right_patterns = {
        (0, 0, 1, 1, 1, 0, 0, 0, 0): "Straying right slightly",
        (0, 0, 1, 1, 1, 1, 0, 0, 0): "Straying right slightly",

        (0, 1, 1, 1, 0, 0, 0, 0, 0): "Straying right",
        (0, 1, 1, 1, 1, 0, 0, 0, 0): "Straying right",

        (1, 1, 1, 0, 0, 0, 0, 0, 0): "Straying right considerably",
        (1, 1, 1, 1, 0, 0, 0, 0, 0): "Straying right considerably",

        (1, 1, 0, 0, 0, 0, 0, 0, 0): "Straying very far right",
        (1, 0, 0, 0, 0, 0, 0, 0, 0): "Almost off track right"
    }

    # Check movement patterns
    if tuple(fork_list) in movement_patterns:
        return movement_patterns[tuple(fork_list)]

    # Check straying left patterns
    if tuple(fork_list) in straying_left_patterns:
        return straying_left_patterns[tuple(fork_list)]

    # Check straying right patterns
    if tuple(fork_list) in straying_right_patterns:
        return straying_right_patterns[tuple(fork_list)]

    # If no pattern matches
    return "Unknown sensor pattern - No action defined"

def detect_fork(sensor_list):
    left_fork_sum = sum(sensor_list[:3])
    right_fork_sum = sum(sensor_list[-3:])
    line_sum = sum(sensor_list) 

    # Approaching the fork
    if sensor_list[4] == 0 and left_fork_sum > 0 and right_fork_sum > 0: # [1, 1, 0, 0, 0, 1, 1, 1, 1]
        return True
    elif line_sum >= 5 and (sensor_list[0] == 0 or sensor_list[8] == 0): # [0, 1, 1, 1, 1, 1, 0, 0, 0]
        return True
    else:
        return False
