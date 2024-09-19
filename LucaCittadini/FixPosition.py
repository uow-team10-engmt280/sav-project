import RPi.GPIO as GPIO # type: ignore
import time
import SOMEARRAY # type: ignore


# NOTE Might not need this


def fixPosition() -> None:

    # First we should reverse slightly to give some room to drive forward and fix
    
    match SOMEARRAY: # type: ignore
        case [0 , 0, 1, 1, 1, 0, 0, 0, 0]:
            ...