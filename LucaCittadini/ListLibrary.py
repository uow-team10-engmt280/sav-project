from SystemLogic import movPhase, forkFlag, pickDropFlag, mergeFlag

global placeHolder
global rSensor
def FindCase() -> list[int]:
        match rSensor: 
            case [0, 0, 0, 1, 1, 1, 0, 0, 0]:
                return [1, 50, 1, 50]
            case [0, 0, 0, 0, 0, 0, 0, 0, 0]:
                return [0, 0, 0, 0]
            case [1, 1, 1, 1, 1, 1, 1, 1, 1]:
                return [0, 0, 0, 0]
            
            case [0, 0, 0, 0, 1, 1, 1, 0, 0]:
                return [1, 50, 1, 45]
            case [0, 0, 0, 0, 0, 1, 1, 1, 0]:
                return [1, 45, 1, 35]
            case [0, 0, 0, 0, 0, 0, 1, 1, 1]:
                return [1, 40, 1, 25]
            case [0, 0, 0, 0, 0, 0, 0, 1, 1]:
                return [1, 35, 1, 15]
            case [0, 0, 0, 0, 0, 0, 0, 0, 1]:
                return [1, 30, 1, 5]
            
            case [0, 0, 1, 1, 1, 0, 0, 0, 0]:
                return [1, 50, 1, 45]
            case [0, 1, 1, 1, 0, 0, 0, 0, 0]:
                return [1, 45, 1, 35]
            case [1, 1, 1, 0, 0, 0, 0, 0, 0]:
                return [1, 40, 1, 25]
            case [1, 1, 0, 0, 0, 0, 0, 0, 0]:
                return [1, 35, 1, 15]
            case [1, 0, 0, 0, 0, 0, 0, 0, 0]:
                return [1, 30, 1, 5]
            
            case _:
                match movPhase: 
                    case 'phaseFork':
                        if forkFlag == False: 
                            match rSensor:
                                case [0, 0, 1, 1, 1, 1, 0, 0, 0] | [0, 0, 1, 1, 1, 1, 1, 0, 0] | [0, 0, 1, 1, 1, 0, 1, 1, 1] | [0, 0, 1, 1, 1, 0, 0, 1, 1] | [0, 0, 1, 1, 1, 0, 0, 0, 1]: 
                                    return [1, 45, 1, 50]
                                case [0, 1, 1, 1, 1, 0, 0, 0, 0] | [0, 0, 0, 1, 1, 1, 1, 1, 0]: 
                                    return [1, 40, 1, 50]
                                case [1, 1, 1, 1, 0, 0, 0, 0, 0]: 
                                    return [1, 30, 1, 45]
                                case [0, 0, 0, 1, 1, 1, 1, 0, 0]: # NOTE can use
                                    return [1, 50, 1, 50]
                                case [0, 0, 0, 0, 1, 1, 1, 1, 0]: 
                                    return [1, 50, 1, 45]
                                case [0, 0, 0, 0, 0, 1, 1, 1, 1]: 
                                    return[1, 50, 1, 40]
                         
                                case [0, 0, 0, 0, 1, 1, 1, 1, 1]: 
                                    return [1, 30, 1, 5]
                                case [0, 1, 1, 1, 1, 1, 0, 0, 0]: 
                                    return [1, 50, 1, 40]
                                case [1, 1, 1, 1, 1, 0, 0, 0, 0]: 
                                    return [1, 45, 1, 30]
                                
                                case [0, 1, 1, 1, 0, 1, 1, 1, 0]: # TODO need to ssee if these 
                                    return [1, 40, 1, 50]
                                case [1, 1, 1, 0, 0, 0, 1, 1, 1]:
                                    return [1, 30, 1, 45]
                                case [1, 1, 0, 0, 0, 0, 0, 1, 1]: 
                                    return [1, 20, 1, 45]
                                case [1, 0, 0, 0, 0, 0, 0, 0, 1]:
                                    return [1, 10, 1, 35]  
                                
                                case [0, 0, 0, 1, 1, 1, 0, 1, 1]: # NOTE
                                    return [1, 50, 1, 50]
                                case [0, 0, 0, 0, 1, 1, 1, 0, 1]: 
                                    return [1, 50, 1, 40]
                                case [0, 0, 0, 1, 1, 1, 0, 0, 1]: # NOTE
                                    return [1, 50, 1, 50]
                              
                                
                                case _:
                                    return [1, 50, 1, 50]
                        else:
                            ...
                    case 'phasePickDrop':
                        if pickDropFlag == False: 
                            ...
                        else:
                            ...
                    case 'phaseMerge':
                        if mergeFlag == False:
                            pickDropFlag = True
                        else:
                            ...
                    case 'phasePark': # We get to this phase after the last merge as we are moving up to the parking spot
                        ...

# Base speed should be equal for both motors, we can test and see what speed is best (try 50% to start with)
# NOTE our motor driver needs a few different things: 
# TODO Needs a mode, depending upon the mode (we will use PHASE/ENABLE), the next inputs will be different

[0, 0, 0, 1, 1, 1, 0, 0, 0] # IN THE MIDDLE                 - Should have motors equal

[0, 0, 0, 0, 0, 0, 0, 0, 0] # FULLY OFF TRACK               - Should be stopped, zero to motors

    [1, 1, 1, 1, 1, 1, 1, 1, 1] # ABSOLUTELY FUCKED (DERAILED)  - Should be stopped, zero to motors

# STRAYING LEFT
    [0, 0, 0, 0, 1, 1, 1, 0, 0] # STRAYING TO THE LEFT SLIGHTY  - Right motor should decrease slightly (-5%)

    [0, 0, 0, 0, 0, 1, 1, 1, 0] # STRAYING TO THE LEFT          - Left motor should decrease slightly (-5%), Right motor should decrease (-15%)

    [0, 0, 0, 0, 0, 0, 1, 1, 1] # STRAYING TO THE LEFT CONSIDERABLY         - Left motor should decrease (-10%), Right motor should decrease considerably (-25%)

    [0, 0, 0, 0, 0, 0, 0, 1, 1] # STRAYING VERY FAR TO THE LEFT             - Left motor should decrease considerably (-15%), Right motor should decrease further (-35%)

    [0, 0, 0, 0, 0, 0, 0, 0, 1] # COMPLETELY TO THE LEFT, ALMOST OFF TRACK  - Left motor should decrease further (-20%), Right motor should be barely running (-45%)

# STRAYING RIGHT
    [0, 0, 1, 1, 1, 0, 0, 0, 0] # STRAYING TO THE RIGHT SLIGHTY  - Left motor should decrease slightly (-5%)
    
    [0, 1, 1, 1, 0, 0, 0, 0, 0] # STRAYING TO THE RIGHT          - Right motor should decrease slightly (-5%), Left motor should decrease (-15%) 
    
    [1, 1, 1, 0, 0, 0, 0, 0, 0] # STRAYING TO THE RIGHT CONSIDERABLY         - Right motor should decrease (-10%), Left motor should decrease considerably (-25%)
    
    [1, 1, 0, 0, 0, 0, 0, 0, 0] # STRAYING VERY FAR TO THE RIGHT             - Right motor should decrease considerably (-15%), Left motor should decrease further (-35%)

    [1, 0, 0, 0, 0, 0, 0, 0, 0] # COMPLETELY TO THE RIGHT, ALMOST OFF TRACK  - Right motor should decrease further (-20%), Left motor should be barely running (-45%)

# COMING UP TO FORK
# TODO version 1 (turning left)
    [0, 0, 1, 1, 1, 1, 0, 0, 0] # COMING UP TO FORK BUT STRAYING SLIGHTLY RIGHT - Left motor should decrease slightly (-5%)

    [0, 1, 1, 1, 1, 0, 0, 0, 0] # COMING UP TO FORK BUT STRAYING RIGHT          - Left motor should decrease (-10%)

    [1, 1, 1, 1, 0, 0, 0, 0, 0] # COMING UP TO FORK BUT STRAYING RIGHT CONSIDERABLY - Left motor should decrease considerably (-20%), Right motor should decrease slightly (-5%)


    [0, 0, 0, 1, 1, 1, 1, 0, 0] # COMING UP TO FORK BUT STRAYING SLIGHTLY LEFT 

    [0, 0, 0, 0, 1, 1, 1, 1, 0] # COMING UP TO FORK BUT STRAYING LEFT               - Right motor should decrease slightly (-5%)

    [0, 0, 0, 0, 0, 1, 1, 1, 1] # COMING UP TO FORK BUT STRAYING LEFT CONSIDERABLY  - Right motor should decrease (-10%)


# TODO version 2 (turning right)

    [0, 0, 0, 1, 1, 1, 1, 0, 0] # COMING UP TO FORK BUT STRAYING SLIGHTLY LEFT - Right motor should decrease slightly (-5%)

    [0, 0, 0, 0, 1, 1, 1, 1, 0] # COMING UP TO FORK BUT STRAYING LEFT          - Right motor should decrease (-10%)

    [0, 0, 0, 0, 0, 1, 1, 1, 1] # COMING UP TO FORK BUT STRAYING LEFT CONSIDERABLY  - Right motor should decrease considerably (-20%), Left motor should decrease slightly (-5%)


    [0, 0, 1, 1, 1, 1, 0, 0, 0] # COMING UP TO FORK BUT STRAYING SLIGHTLY RIGHT 

    [0, 1, 1, 1, 1, 0, 0, 0, 0] # COMING UP TO FORK BUT STRAYING RIGHT              - Left motor should decrease slightly (-5%)

    [1, 1, 1, 1, 0, 0, 0, 0, 0] # COMING UP TO FORK BUT STRAYING RIGHT CONSIDERABLY - Left motor should decrease (-10%)


# LEAVING THE MERGE NOTE shouldn't matter what side we're coming from
# TODO, SAME FOR BOTH SIDES?
    [0, 0, 1, 1, 1, 1, 0, 0, 0] # LEAVING THE MERGE BUT STRAYING SLIGHTLY RIGHT

    [0, 1, 1, 1, 1, 0, 0, 0, 0] # LEAVING THE MERGE BUT STRAYING RIGHT              - Left motor should decrease (-10%)

    [1, 1, 1, 1, 0, 0, 0, 0, 0] # COMING UP TO FORK BUT STRAYING RIGHT CONSIDERABLY - Left motor should decrease considerably (-20%), Right motor should decrease slightly (-5%)


    [0, 0, 0, 1, 1, 1, 1, 0, 0] # LEAVING THE MERGE BUT STRAYING SLIGHTLY LEFT

    [0, 0, 0, 0, 1, 1, 1, 1, 0] # COMING UP TO FORK BUT STRAYING LEFT               - Right motor should decrease (-10%)

    [0, 0, 0, 0, 0, 1, 1, 1, 1] # COMING UP TO FORK BUT STRAYING LEFT CONSIDERABLY  - Right motor should decrease considerably (-20%), Left motot should increase slightly (-5%)





# ON THE FORK 
# TODO version 1 (turning left)

    [0, 0, 1, 1, 1, 1, 1, 0, 0] # DIRECTLY ON THE FORK                            - Left motor should decrease slightly (-5%)
    

    [0, 0, 0, 1, 1, 1, 1, 1, 0] # DIRECTLY ON THE FORK BUT STRAYING SLIGHTLY LEFT - Left motor should decrease (-10%)
    
    [0, 0, 0, 0, 1, 1, 1, 1, 1] # DIRECTLY ON THE FORK BUT STRAYING LEFT          - Left motor should decrease considerably (-20%), Right motor should decrease slightly (-5%)
    

    [0, 1, 1, 1, 1, 1, 0, 0, 0] # DIRECTLY ON THE FORK BUT STRAYING SLIGHTLY RIGHT - Right motor should decrease (-10%)
    
    [1, 1, 1, 1, 1, 0, 0, 0, 0] # DIRECTLY ON THE FORK BUT STRAYING RIGHT          - Right motor should decrease considerably (-20%), Left motor should decrease slightly (-5%)

# TODO version 2 (turning right)
    [0, 0, 1, 1, 1, 1, 1, 0, 0] # DIRECTLY ON THE FORK - Right motor should decrease slightly (-5%)
    

    [0, 0, 0, 1, 1, 1, 1, 1, 0] # DIRECTLY ON THE FORK BUT STRAYING SLIGHTLY LEFT  - Left motor should decrease (-10%)
    
    [0, 0, 0, 0, 1, 1, 1, 1, 1] # DIRECTLY ON THE FORK BUT STRAYING LEFT           - Left motor should decrease considerably (-20%), Right motor should decrease slightly (-5%)
    

    [0, 1, 1, 1, 1, 1, 0, 0, 0] # DIRECTLY ON THE FORK BUT STRAYING SLIGHTLY RIGHT - Right motor should decrease (-10%)
    
    [1, 1, 1, 1, 1, 0, 0, 0, 0] # DIRECTLY ON THE FORK BUT STRAYING RIGHT          - Right motor should decrease considerably (-20%), Left motor should decrease slightly (-5%)

# ON THE MERGE NOTE shouldn't matter what side we're coming from

    [0, 0, 1, 1, 1, 1, 1, 0, 0] # DIRECTLY ON THE MERGE
    

    [0, 0, 0, 1, 1, 1, 1, 1, 0] # DIRECTLY ON THE MERGE BUT STRAYING SLIGHTLY LEFT   - Left motor should decrease slightly (-5%)
    
    [0, 0, 0, 0, 1, 1, 1, 1, 1] # DIRECTLY ON THE FORK BUT STRAYING LEFT             - Left motor should decrease (-10%)
    

    [0, 1, 1, 1, 1, 1, 0, 0, 0] # DIRECTLY ON THE FORK BUT STRAYING SLIGHTLY RIGHT   - Right motor should decrease slightly (-5%)
    
    [1, 1, 1, 1, 1, 0, 0, 0, 0] # DIRECTLY ON THE FORK BUT STRAYING RIGHT            - Right motor should decrease (-10%)


# GOING PAST THE FORK
# TODO version 1 (turning left)
    [0, 1, 1, 1, 0, 1, 1, 1, 0] # CENTERED ON FORK BUT SLIGHTLY PAST  - Left motor should decrease (-10%)

    [1, 1, 1, 0, 0, 0, 1, 1, 1] # CENTERED ON FORK BUT PAST           - Left motor should decrease considerably (-20%), Right motor should decrease slightly (-5%)
    
    [1, 1, 0, 0, 0, 0, 0, 1, 1] # CENTERED ON FORK BUT PAST CONSIDERABLY - Left motor should decrease majorly (-30%), Right motor should decrease (-10%)
    
    [1, 0, 0, 0, 0, 0, 0, 0, 1] # CENTERED ON FORK BUT VERY FAR PAST     - Left motor should decrease massively (-40%), Right motor should decrease more (-15%)

# TODO version 2 (turning right)
    [0, 1, 1, 1, 0, 1, 1, 1, 0] # CENTERED ON FORK BUT SLIGHTLY PAST  - Right motor should decrease (-10%)

    [1, 1, 1, 0, 0, 0, 1, 1, 1] # CENTERED ON FORK BUT PAST           - Right motor should decrease considerably (-20%), Left motor should decrease slightly (-5%)
    
    [1, 1, 0, 0, 0, 0, 0, 1, 1] # CENTERED ON FORK BUT PAST CONSIDERABLY - Right motor should decrease majorly (-30%), Left motor should decrease (-10%)
    
    [1, 0, 0, 0, 0, 0, 0, 0, 1] # CENTERED ON FORK BUT VERY FAR PAST     - Right motor should decrease massively (-40%), Left motor should decrease more (-15%)


# FOLLOWING THE FORK - TURNING LEFT 
# TODO version 1 (turning left)
    [0, 0, 1, 1, 1, 0, 1, 1, 1] # FOLLOWING FORK LEFT 1, STRAYING SLIGHTLY RIGHT - Left motor should decrease slightly (-5%)
    
    [0, 0, 0, 1, 1, 1, 0, 1, 1] # FOLLOWING FORK LEFT 1, ON POINT
    
    [0, 0, 0, 0, 1, 1, 1, 0, 1] # FOLLOWING FORK LEFT 1, STRAYING SLIGHTLY TOO FAR LEFT - Right motor should decrease (-10%)


    [0, 0, 1, 1, 1, 0, 0, 1, 1] # FOLLOWING FORK LEFT 2, STRAYING SLIGHTLY RIGHT - Left motor should decrease slightly (-5%)

    [0, 0, 0, 1, 1, 1, 0, 0, 1] # FOLLOWING FORK LEFT 2, ON POINT


    [0, 0, 1, 1, 1, 0, 0, 0, 1] # FOLLOWING FORK LEFT 3, STRAYING SLIGHTLY RIGHT - Left motor should decrease slightly (-5%)


# COMING UP TO THE MERGE - FROM LEFT
# TODO version 1 (coming from left)
    [0, 0, 1, 1, 1, 0, 1, 1, 1] # MERGING FROM LEFT 1, STRAYING SLIGHTLY RIGHT - Right motor should decrease slightly (-5%)
    
    [0, 0, 0, 1, 1, 1, 0, 1, 1] # MERGING FROM LEFT 1, ON POINT
    
    [0, 0, 0, 0, 1, 1, 1, 0, 1] # MERGING FROM LEFT 1, STRAYING SLIGHTLY TOO FAR LEFT - Left motor should decrease slightly (-5%)


    [0, 0, 1, 1, 1, 0, 0, 1, 1] # MERGING FROM LEFT 2, STRAYING SLIGHTLY RIGHT - Right motor should decrease slightly (-5%)

    [0, 0, 0, 1, 1, 1, 0, 0, 1] # MERGING FROM 2, ON POINT


    [0, 0, 1, 1, 1, 0, 0, 0, 1] # MERGING FROM LEFT 3, STRAYING SLIGHTLY RIGHT - Right motor should decrease slightly (-5%)
    
# FOLLOWING THE FORK - TURNING RIGHT
# TODO version 2 (turning right)
    [1, 1, 1, 0, 1, 1, 1, 0, 0] # FOLLOWING FORK RIGHT 1, STRAYING SLIGHTLY LEFT - Right motor should decrease slightly (-5%)
    
    [1, 1, 0, 1, 1, 1, 0, 0, 0] # FOLLOWING FORK RIGHT 1, ON POINT 
    
    [1, 0, 1, 1, 1, 0, 0, 0, 0] # FOLLOWING FORK RIGHT 1, STRAYING SLIGHTLY TOO FAR RIGHT - Left motor should decrease slightly (-5%)


    [1, 1, 0, 0, 1, 1, 1, 0, 0] # FOLLOWING FORK RIGHT 2, STRAYING SLIGHTLY LEFT - Right motor should decrease slightly (-5%)
    
    [1, 0, 0, 1, 1, 1, 0, 0, 0] # FOLLOWING FORK RIGHT 2, ON POINT 


    [1, 0, 0, 0, 1, 1, 1, 0, 0] # FOLLOWING FORK RIGHT 3, STRAYING SLIGHTLY LEFT - Right motor should decrease slightly (-5%)

# COMING UP TO THE MERGE - FROM RIGHT
# TODO version 2 (coming from right)
    [1, 1, 1, 0, 1, 1, 1, 0, 0] # MERGING FROM RIGHT 1, STRAYING SLIGHTLY LEFT - Left motor should decrease slightly (-5%)
    
    [1, 1, 0, 1, 1, 1, 0, 0, 0] # MERGING FROM RIGHT 1, ON POINT 
    
    [1, 0, 1, 1, 1, 0, 0, 0, 0] # MERGING FROM RIGHT 1, STRAYING SLIGHTLY TOO FAR RIGHT - Right motor should decrease slightly (-5%)


    [1, 1, 0, 0, 1, 1, 1, 0, 0] # MERGING FROM RIGHT 2, STRAYING SLIGHTLY LEFT - Left motor should decrease slightly (-5%)
    
    [1, 0, 0, 1, 1, 1, 0, 0, 0] # MERGING FROM RIGHT 2, ON POINT 


    [1, 0, 0, 0, 1, 1, 1, 0, 0] # MERGING FROM RIGHT 3, STRAYING SLIGHTLY LEFT - Left motor should decrease slightly (-5%)

# TODO PARKING MARKINGS

