from RPi import GPIO # type: ignore

class Motor:

    def __init__(self, in1Pin, in2Pin) -> None:
        self.in1Pin = in1Pin
        self.in2Pin = in2Pin

        self.in1 = GPIO.PWM(self.in1Pin, 1000) # decorator?
        self.in2 = GPIO.PWM(self.in2Pin, 1000)


    
    def forward(self) -> None: 
        match reflectSense:
            case _:
                ...


    def backward(self) -> None: 
        match reflectSense:
            case _:
                ...


    def left(self) -> None: 
        match reflectSense:
            case _:
                ...


    def right(self) -> None: 
        match reflectSense:
            case _:
                ...


    def stop(self) -> None: 
        match reflectSense:
            case _:
                ...

        


