import time


class IDLE(): # The initial state

    def userWait(self) -> None:
        while True:
            match input('Type "Start" to begin programme. \n').lower():
                case 'start' | 's':
                    break
                case _:
                    print('Invalid, try again \n')

    def switch(self, nextState) -> None:
        if nextState == 'l':
            return LISTENING()
        return self
    

class LISTENING(): # calls Machine Vision, starts timer
    def switch(self, nextState) -> None:
        if nextState == 'm':
            return MOVING()
        return self
        
    def findPath(self) -> list[bool]:
        return ...
        

class MOVING(): # calls motor programme (motor programme will call sensor programme), should have children classes that act as the phases
    def switch(self, nextState) -> None:
        if nextState == 'a':
            return ACTION()
        elif nextState == 'p':
            return PARKING()
        return self
        

class ACTION(): 
    def switch(self, nextState) -> None:
        if nextState == 'm':
            return MOVING()
        return self
        

class PARKING(): 
    def switch(self, nextState) -> None:
        if nextState == 'c':
            return COMPLETE()
        return self


class COMPLETE(): # The final state
    def switch(self, nextState) -> None:
        return self
    
    
class SAV: # The Object
    def __init__(self) -> None:
        self.state = IDLE()
    
    def switch(self, nextState) -> None: 
        self.state = self.state.switch(nextState)
        print(f'We are in the {self.state.__class__.__name__} state')

jamal = SAV()

jamal.state.userWait()
jamal.switch('l')
jamal.switch('m')
jamal.switch('a')
jamal.switch('m')
jamal.switch('a')
jamal.switch('m')
jamal.switch('p')
jamal.switch('c')
