from FindCase import FindCase
from RPi import GPIO # type: ignore
import MATTsSENSORPROGRAMME # type: ignore

# Initialise values - rSensor: list[int], movPhase: str, turnOne: bool, pickDropFlag: bool, turnTwo: bool, forkFlag: bool
#                     MATTsSENSORPROGRAMME, b          , c            , d                 , e            , f

b, c, d, e, f = 'phaseFork', 0, 0, 0, 0


try:
    while True:
        FindCase(MATTsSENSORPROGRAMME, b, c, d, e, f)
except:
    GPIO.cleanup()