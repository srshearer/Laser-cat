
## Cat Laser Tower for Circuit Python

Pseudo-randomly moves a servo tower (on X and Y axis) and lights up a laser. Re-written into Python in order to support [Circuit Python](https://learn.adafruit.com/welcome-to-circuitpython/overview).  

Watch the original working : [https://www.youtube.com/watch?v=hHIrxL0giJQ](https://www.youtube.com/watch?v=hHIrxL0giJQ)


## Set up
x_servo is attached to pin 9 (and +5V and GND) and moves in the X plane.

y_servo is attached to pin 6 (and +5V and GND) and moves in the Y plane.

Laser is attached to pin 13 (and GND).

Download the code.py file, copy it to a board that runs Circuit Python, and reset the board. 

## How it works : 
The program randomly choose a new position for the laser inside a square you can define in the variables.
It verifies the new position is different from the old one by at least "minimal_movement".
It moves the tower to the new position and stays still for a time between min_freeze and max_freeze 
(this aims to reproduce the behaviour of an insect landing somewhere for a bit and then flying off, 
that's the variable you need to increase if your cat is fat...) and starts the process over and over again. 


_Originally created 30 Sep 2016 by Lucas Berbesson for La Fabrique DIY_  
_Re-written for Circuit Python 30 Dec 2018 by Steven Shearer_

