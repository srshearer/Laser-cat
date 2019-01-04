import time
import random
import board
import pulseio
from adafruit_motor import servo
from digitalio import DigitalInOut, Direction, Pull


def random_float(x, y, decimals=2):
    return round(random.uniform(x, y), decimals)


def random_int(x, y):
    return random.randint(x, y)


def main():
    # adjust for room size
    min_x = 20
    max_x = 105
    min_y = 70
    max_y = 110

    # set time range to stop in each position
    min_freeze = 0.05
    max_freeze = 3
    minimal_movement = 5


    ## YOU SHOULD NOT HAVE TO MODIFY THE CODE BELOW THIS LINE ##

    ## initialize laser and servos
    # x servo at pin D13
    laser = DigitalInOut(board.D13)
    laser.direction = Direction.OUTPUT

    # x servo at pin D9
    pwm_x = pulseio.PWMOut(board.D9, frequency=50)
    x_servo = servo.Servo(pwm_x, min_pulse=750, max_pulse=2250)

    # y servo at pin D6
    pwm_y = pulseio.PWMOut(board.D6, frequency=50)
    y_servo = servo.Servo(pwm_y, min_pulse=750, max_pulse=2250)

    # finding center of square for starting point
    x_pos = int(min_x + (max_x - min_x) / 2)
    y_pos = int(min_y + (max_y - min_y) / 2)
    x_old_pos = x_pos
    y_old_pos = y_pos

    while True:
        ## movement loop

        # laser on
        laser.value = True

        # get random values x & y position, and delay
        random_delay = random_float(min_freeze, max_freeze)
        x_new_pos = random_int(min_x, max_x)
        y_new_pos = random_int(min_y, max_y)

        # adjust for minimum movement deltas
        if y_new_pos > y_old_pos and (y_new_pos - y_old_pos) < 5:
            y_new_pos = y_new_pos + minimal_movement
        elif y_new_pos < y_old_pos and (y_new_pos - y_old_pos) < 5:
            y_new_pos = y_new_pos - minimal_movement

        if x_new_pos > x_old_pos and (x_new_pos - x_old_pos) < 5:
            x_new_pos = x_new_pos + minimal_movement
        elif x_new_pos < x_old_pos and (x_new_pos - x_old_pos) < 5:
            x_new_pos = x_new_pos - minimal_movement

        # console output: useful for adjusting room size
        print('random_delay: {}'.format(random_delay))
        print('x_old_pos: {}'.format(x_old_pos))
        print('y_old_pos: {}'.format(y_old_pos))
        print('x_new_pos: {}'.format(x_new_pos))
        print('y_new_pos: {}\n'.format(y_new_pos))

        # move servos into position
        x_servo.angle = x_new_pos
        y_servo.angle = y_new_pos

        # set new positions as old for the next loop
        x_old_pos = x_new_pos
        y_old_pos = y_new_pos

        # keep servos in position for set random amount of time
        time.sleep(random_delay)


if __name__ == '__main__':
    main()
