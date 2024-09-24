from SystemLogic import movPhase, turnOne, pickDropFlag, turnTwo, forkFlag

# TODO Make some kind of sequence detector to recognise when we have gone past the fork or merge


# FIXME the return percent, not dutycycle --- Actually this might be fine


def FindCase(rSensor: list[int]) -> list[int]:
        match rSensor: 
    # Base movement, forward and stop
            case [0, 0, 0, 1, 1, 1, 0, 0, 0]:
                print('forward')
                return [1, 50, 1, 50]
            case [0, 0, 0, 0, 0, 0, 0, 0, 0]:
                print('stop')
                return [0, 0, 0, 0]
            case [1, 1, 1, 1, 1, 1, 1, 1, 1]:
                print('stop')
                return [0, 0, 0, 0]
    # Basic turning for staying on track
            case [0, 0, 0, 0, 1, 1, 1, 0, 0]:
                print('right')
                return [1, 50, 1, 45]
            case [0, 0, 0, 0, 0, 1, 1, 1, 0]:
                print('righter')
                return [1, 45, 1, 35]
            case [0, 0, 0, 0, 0, 0, 1, 1, 1]:
                print('righterer')
                return [1, 40, 1, 25]
            case [0, 0, 0, 0, 0, 0, 0, 1, 1]:
                print('rightererer')
                return [1, 35, 1, 15]
            case [0, 0, 0, 0, 0, 0, 0, 0, 1]:
                print('rightest')
                return [1, 30, 1, 5]
            case [0, 0, 1, 1, 1, 0, 0, 0, 0]:
                print('left')
                return [1, 45, 1, 50]
            case [0, 1, 1, 1, 0, 0, 0, 0, 0]:
                print('lefter')
                return [1, 35, 1, 45]
            case [1, 1, 1, 0, 0, 0, 0, 0, 0]:
                print('lefterer')
                return [1, 25, 1, 40]
            case [1, 1, 0, 0, 0, 0, 0, 0, 0]:
                print('leftererer')
                return [1, 15, 1, 35]
            case [1, 0, 0, 0, 0, 0, 0, 0, 0]:
                print('leftest')
                return [1, 5, 1, 30]
            
            case _:
                match movPhase: 
                    case 'phaseFork':
                        if forkFlag == False: # IF FALSE THEN WE ARE AT FORK ONE
                            if turnOne == False: 
                                match rSensor: # TURNING LEFT
                                    case [0, 0, 1, 1, 1, 1, 0, 0, 0] | [0, 0, 1, 1, 1, 1, 1, 0, 0] | [0, 0, 1, 1, 1, 0, 1, 1, 1] | [0, 0, 1, 1, 1, 0, 0, 1, 1] | [0, 0, 1, 1, 1, 0, 0, 0, 1]: 
                                        print('left')
                                        return [1, 45, 1, 50]
                                    case [0, 1, 1, 1, 1, 0, 0, 0, 0] | [0, 1, 1, 1, 1, 1, 0, 0, 0] | [0, 1, 1, 1, 0, 1, 1, 1, 0]: 
                                        print('lefter')
                                        return [1, 40, 1, 50]
                                    case [0, 0, 0, 0, 1, 1, 1, 1, 0] | [0, 0, 0, 0, 1, 1, 1, 0, 1]: 
                                        print('right')
                                        return [1, 50, 1, 45]
                                    case [1, 1, 1, 1, 0, 0, 0, 0, 0] | [1, 1, 1, 0, 0, 0, 1, 1, 1] | [1, 1, 1, 1, 1, 0, 0, 0, 0]: 
                                        print('lefterer')
                                        return [1, 30, 1, 45]
                                    case [1, 1, 0, 0, 0, 0, 0, 1, 1]: 
                                        print('leftererer')
                                        return [1, 20, 1, 45]
                                    case [0, 0, 0, 0, 0, 1, 1, 1, 1] | [0, 0, 0, 1, 1, 1, 1, 1, 0]:
                                        print('righter')
                                        return [1, 50, 1, 40]
                                    case [1, 0, 0, 0, 0, 0, 0, 0, 1]:
                                        print('leftest')
                                        return [1, 10, 1, 35]
                                    case [0, 0, 0, 0, 1, 1, 1, 1, 1]: 
                                        print('righter')
                                        return [1, 45, 1, 30]
                                    case _:
                                        print('forward')
                                        return [1, 50, 1, 50]
                            else:
                                match rSensor: # TURNING RIGHT
                                    case [0, 0, 0, 1, 1, 1, 1, 0, 0] | [0, 0, 1, 1, 1, 1, 1, 0, 0] | [1, 1, 1, 0, 1, 1, 1, 0, 0] | [1, 1, 0, 0, 1, 1, 1, 0, 0] | [1, 0, 0, 0, 1, 1, 1, 0, 0]: 
                                        print('right')
                                        return [1, 50, 1, 45]
                                    case [0, 0, 0, 0, 1, 1, 1, 1, 0] | [0, 1, 1, 1, 1, 1, 0, 0, 0] | [0, 1, 1, 1, 0, 1, 1, 1, 0]: 
                                        print('righter')
                                        return [1, 50, 1, 40]
                                    case [0, 1, 1, 1, 1, 0, 0, 0, 0] | [1, 0, 1, 1, 1, 0, 0, 0, 0]: 
                                        print('left')
                                        return [1, 45, 1, 50]
                                    case [0, 0, 0, 0, 1, 1, 1, 1, 1] | [1, 1, 1, 0, 0, 0, 1, 1, 1] | [0, 0, 0, 0, 0, 1, 1, 1, 1]: 
                                        print('righterer')
                                        return [1, 45, 1, 30]
                                    case [1, 1, 1, 1, 0, 0, 0, 0, 0] | [0, 0, 0, 1, 1, 1, 1, 1, 0]: 
                                        print('lefter')
                                        return [1, 40, 1, 50]
                                    case [1, 1, 0, 0, 0, 0, 0, 1, 1]: 
                                        print('rightererer')
                                        return [1, 40, 1, 20]
                                    case [1, 0, 0, 0, 0, 0, 0, 0, 1]: 
                                        print('rightest')
                                        return [1, 35, 1, 10]
                                    case [1, 1, 1, 1, 1, 0, 0, 0, 0]: 
                                        print('lefterer')
                                        return [1, 30, 1, 45]
                                    case _:
                                        print('forward')
                                        return [1, 50, 1, 50]
                        else:
                            if turnTwo == False: 
                                match rSensor: # TURNING LEFT
                                    case [0, 0, 1, 1, 1, 1, 0, 0, 0] | [0, 0, 1, 1, 1, 1, 1, 0, 0] | [0, 0, 1, 1, 1, 0, 1, 1, 1] | [0, 0, 1, 1, 1, 0, 0, 1, 1] | [0, 0, 1, 1, 1, 0, 0, 0, 1]: 
                                        print('left')
                                        return [1, 45, 1, 50]
                                    case [0, 1, 1, 1, 1, 0, 0, 0, 0] | [0, 1, 1, 1, 1, 1, 0, 0, 0] | [0, 1, 1, 1, 0, 1, 1, 1, 0]: 
                                        print('lefter')
                                        return [1, 40, 1, 50]
                                    case [0, 0, 0, 0, 1, 1, 1, 1, 0] | [0, 0, 0, 0, 1, 1, 1, 0, 1]: 
                                        print('right')
                                        return [1, 50, 1, 45]
                                    case [1, 1, 1, 1, 0, 0, 0, 0, 0] | [1, 1, 1, 0, 0, 0, 1, 1, 1] | [1, 1, 1, 1, 1, 0, 0, 0, 0]: 
                                        print('lefterer')
                                        return [1, 30, 1, 45]
                                    case [1, 1, 0, 0, 0, 0, 0, 1, 1]: 
                                        print('leftererer')
                                        return [1, 20, 1, 45]
                                    case [0, 0, 0, 0, 0, 1, 1, 1, 1] | [0, 0, 0, 1, 1, 1, 1, 1, 0]:
                                        print('righter')
                                        return [1, 50, 1, 40]
                                    case [1, 0, 0, 0, 0, 0, 0, 0, 1]:
                                        print('leftest')
                                        return [1, 10, 1, 35]
                                    case [0, 0, 0, 0, 1, 1, 1, 1, 1]: 
                                        print('righterer')
                                        return [1, 45, 1, 30]
                                    case _:
                                        print('forward')
                                        return [1, 50, 1, 50]
                            else:
                                match rSensor: # TURNING RIGHT
                                    case [0, 0, 0, 1, 1, 1, 1, 0, 0] | [0, 0, 1, 1, 1, 1, 1, 0, 0] | [1, 1, 1, 0, 1, 1, 1, 0, 0] | [1, 1, 0, 0, 1, 1, 1, 0, 0] | [1, 0, 0, 0, 1, 1, 1, 0, 0]: 
                                        print('right')
                                        return [1, 50, 1, 45]
                                    case [0, 0, 0, 0, 1, 1, 1, 1, 0] | [0, 1, 1, 1, 1, 1, 0, 0, 0] | [0, 1, 1, 1, 0, 1, 1, 1, 0]: 
                                        print('righter')
                                        return [1, 50, 1, 40]
                                    case [0, 1, 1, 1, 1, 0, 0, 0, 0] | [1, 0, 1, 1, 1, 0, 0, 0, 0]: 
                                        print('left')
                                        return [1, 45, 1, 50]
                                    case [0, 0, 0, 0, 1, 1, 1, 1, 1] | [1, 1, 1, 0, 0, 0, 1, 1, 1] | [0, 0, 0, 0, 0, 1, 1, 1, 1]: 
                                        print('righterer')
                                        return [1, 45, 1, 30]
                                    case [1, 1, 1, 1, 0, 0, 0, 0, 0] | [0, 0, 0, 1, 1, 1, 1, 1, 0]: 
                                        print('lefter')
                                        return [1, 40, 1, 50]
                                    case [1, 1, 0, 0, 0, 0, 0, 1, 1]: 
                                        print('rightererer')
                                        return [1, 40, 1, 20]
                                    case [1, 0, 0, 0, 0, 0, 0, 0, 1]: 
                                        print('rightest')
                                        return [1, 35, 1, 10]
                                    case [1, 1, 1, 1, 1, 0, 0, 0, 0]: 
                                        print('lefterer')
                                        return [1, 30, 1, 45]
                                    case _:
                                        print('forward')
                                        return [1, 50, 1, 50]
                    case 'phaseMerge':
                        match rSensor:
                            case [0, 0, 1, 1, 1, 1, 0, 0, 0] | [0, 0, 0, 1, 1, 1, 1, 0, 0] | [0, 0, 1, 1, 1, 1, 1, 0, 0]:
                                print('forward')
                                return [1, 50, 1, 50]
                            case [0, 1, 1, 1, 1, 0, 0, 0, 0] | [1, 1, 1, 1, 1, 0, 0, 0, 0]: 
                                print('lefter')
                                return [1, 40, 1, 50]
                            case [1, 1, 1, 1, 0, 0, 0, 0, 0]: 
                                print('lefterer')
                                return [1, 30, 1, 45]
                            case [0, 0, 0, 0, 1, 1, 1, 1, 0] | [0, 0, 0, 0, 1, 1, 1, 1, 1]: 
                                print('righter')
                                return [1, 50, 1, 40]
                            case [0, 0, 0, 0, 0, 1, 1, 1, 1]: 
                                print('rightererer')
                                return [1, 45, 1, 20]
                            case [0, 0, 0, 1, 1, 1, 1, 1, 0]: 
                                print('right')
                                return [1, 50, 1, 45]
                            case [0, 1, 1, 1, 1, 1, 0, 0, 0]: 
                                print('left')
                                return [1, 45, 1, 50]
                            case _:
                                if pickDropFlag == False: 
                                    if turnOne == False: 
                                        match rSensor:
                                            case [0, 0, 0, 1, 1, 1, 0, 1, 1] | [0, 0, 0, 1, 1, 1, 0, 0, 1]:
                                                print('forward')
                                                return [1, 50, 1, 50] 
                                            case [0, 0, 1, 1, 1, 0, 1, 1, 1] | [0, 0, 1, 1, 1, 0, 0, 1, 1] | [0, 0, 1, 1, 1, 0, 0, 0, 1]:
                                                print('left')
                                                return [1, 45, 1, 50] 
                                            case [0, 0, 0, 0, 1, 1, 1, 0, 1]:
                                                print('right')
                                                return [1, 50, 1, 45] 
                                    else:
                                        match rSensor:
                                            case [1, 1, 0, 1, 1, 1, 0, 0, 0] | [1, 0, 0, 1, 1, 1, 0, 0, 0]:
                                                print('forward')
                                                return [1, 50, 1, 50]
                                            case [1, 1, 1, 0, 1, 1, 1, 0, 0] | [1, 1, 0, 0, 1, 1, 1, 0, 0] | [1, 0, 0, 0, 1, 1, 1, 0, 0]: 
                                                print('left')
                                                return [1, 45, 1, 50]
                                            case [1, 0, 1, 1, 1, 0, 0, 0, 0]: 
                                                print('right')
                                                return [1, 50, 1, 45]
                                else:
                                    if turnTwo == False:
                                        match rSensor:
                                            case [0, 0, 0, 1, 1, 1, 0, 1, 1] | [0, 0, 0, 1, 1, 1, 0, 0, 1]:
                                                print('forward')
                                                return [1, 50, 1, 50] 
                                            case [0, 0, 1, 1, 1, 0, 1, 1, 1] | [0, 0, 1, 1, 1, 0, 0, 1, 1] | [0, 0, 1, 1, 1, 0, 0, 0, 1]:
                                                print('left')
                                                return [1, 45, 1, 50] 
                                            case [0, 0, 0, 0, 1, 1, 1, 0, 1]:
                                                print('right')
                                                return [1, 50, 1, 45] 
                                    else:
                                        match rSensor:
                                            case [1, 1, 0, 1, 1, 1, 0, 0, 0] | [1, 0, 0, 1, 1, 1, 0, 0, 0]:
                                                print('forward')
                                                return [1, 50, 1, 50]
                                            case [1, 1, 1, 0, 1, 1, 1, 0, 0] | [1, 1, 0, 0, 1, 1, 1, 0, 0] | [1, 0, 0, 0, 1, 1, 1, 0, 0]: 
                                                print('left')
                                                return [1, 45, 1, 50]
                                            case [1, 0, 1, 1, 1, 0, 0, 0, 0]: 
                                                print('right')
                                                return [1, 50, 1, 45]
