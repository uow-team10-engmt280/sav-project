from time import time, sleep
from MachineVisionLuca import MV
# from ServoFunctions import servoAction



class IDLE(): # The initial state

    def userWait(self) -> None:
        while True:
            match input(f'Type "Start" to begin programme. \n').lower():
                case 'start' | 's':
                    break
                case _:
                    print(f'Invalid, try again \n')

    def switch(self, nextState) -> None:
        if nextState == 'l': # I feel like there's an easier way to do this but not sure what
            print(f'Going to the LISTENING state. \n')
            return LISTENING()
        return self
    

class LISTENING(): # calls Machine Vision, starts timer
        
    def findPath(self, directionNum) -> list[bool]:
        self.instance.directions = MV(directionNum)
        print(f'Your first turn is {self.instance.directions[0]} and you are picking up on {self.instance.directions[1]}! \n')
    
    def timerStart(self):
        self.instance.startTime = time()
        print(f'Starting timer... \n')

    def switch(self, nextState) -> None:
        if nextState == 'm':
            print(f'Going to the MOVING state. \n')
            return MOVING()
        return self
        

class MOVING(): # calls motor programme (motor programme will call sensor programme), should have children classes that act as the phases (actually might not need to)
    
    def motorControl(self) -> None: # The function/method that this calls should deal with the reading of the reflectance sensors, the writing to the motor driver, as well as checking the range sensor to break out of a while loop
        for i in range(0, 5): 
            print(f'Moving... \n')
            sleep(1)
    
    def switch(self, nextState) -> None:
        if nextState == 'a':
            print(f'Going to the ACTION state. \n')
            return ACTION()
        elif nextState == 'p':
            print(f'Going to the PARKING state. \n')
            return PARKING()
        return self
        

class ACTION(): 
    
    def fixPosition(self) -> None: ... # Probably just calls a function from somewhere else


    def activateServos(self) -> None:
        # self.turn = self.instance.directions[0]
        # self.side = self.instance.directions[1]
        # servoAction(self.turn, self.side)
        print(f'Moving Servos... \n')
        sleep(5)

    def switch(self, nextState) -> None:
        if nextState == 'm':
            print(f'Going to the MOVING state. \n')
            return MOVING()
        return self
        

class PARKING(): 

    def parkUp(self) -> None: # Not sure if this is neccessary or not
        print(f'Parking... \n')
        sleep(3)

    def switch(self, nextState) -> None:
        if nextState == 'c':
            print(f'Going to COMPLETE state. \n')
            return COMPLETE()
        return self


class COMPLETE(): # The final state

    def timerStop(self) -> None:
        self.endTime = time() - self.instance.startTime
        print(f'You took {self.endTime} to complete the Race')

    def switch(self, nextState) -> None:
        return self
    
    
class SAV: # The Object

    def __init__(self) -> None: # Here we will initialise all used data as empty values, then when the data is altered, each state can see the alteration. NOTE that you only need to initialise data if it needs to be accessed by multiple states
        self.state = IDLE()
        self.directions = None
        self.startTime = None # stored in the instance 
    
    def switch(self, nextState) -> None: 
        self.state = self.state.switch(nextState)
        self.state.instance = self 
        print(f'We are in the {self.state.__class__.__name__} state')



jamal = SAV()

jamal.state.userWait() # jamal = SAV, state = IDLE, userWait is a method within the IDLE state
jamal.switch('l')


jamal.state.findPath(0)
jamal.state.timerStart()
jamal.switch('m')


jamal.state.motorControl()
jamal.switch('a')


jamal.state.activateServos()
jamal.switch('m') # Might want to jump to listening state first to get the second lot of instructions


jamal.state.motorControl()
jamal.switch('a')


jamal.state.activateServos()
jamal.switch('m')

jamal.state.motorControl()
jamal.switch('p')


jamal.switch('c')

jamal.state.timerStop()