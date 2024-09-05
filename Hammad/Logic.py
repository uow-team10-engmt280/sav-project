# Read line Sensor info, moves or turns accordingly

# Whilst moving if the distance sensor gpio goes high stop and turn servo and pickup object, then give the line sensor a timeout, allowing the sav to move even if its high for a time period. 
# Motor controller sets speed higher when moving normally, and for turning its slower

# Once line Sensor detects binary for parking, the sav stops moving

# States are in while loop
#
