import time
import random
import board
import pulseio
from adafruit_motor import servo
from digitalio import DigitalInOut, Direction, Pull


def random_float(x, y, decimals=2):
    return round(random.uniform(x, y), decimals)


def random_int(x, y, decimals=2):
    return random.randint(x, y)


def main():
    cont = 0

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

    # finding center of square for starting point
    x_pos = int(min_x + (max_x - min_x) / 2)
    y_pos = int(min_y + (max_y - min_y) / 2)
    x_old_pos = x_pos
    y_old_pos = y_pos

    ## init laser and servos
    laser = DigitalInOut(board.D13)
    laser.direction = Direction.OUTPUT

    # x servo at pin A2
    pwm_x = pulseio.PWMOut(board.D9, frequency=50)
    x_servo = servo.Servo(pwm_x, min_pulse=750, max_pulse=2250)

    # y servo at pin A4
    pwm_y = pulseio.PWMOut(board.D6, frequency=50)
    y_servo = servo.Servo(pwm_y, min_pulse=750, max_pulse=2250)

    while True: # cont < 30:
        laser.value = True

        random_delay = random_float(min_freeze, max_freeze)
        x_new_pos = random_int(min_x + minimal_movement, max_x - minimal_movement)
        y_new_pos = random_int(min_y + minimal_movement, max_y - minimal_movement)

        if y_new_pos > y_old_pos and (y_new_pos - y_old_pos) < 5:
            y_new_pos = y_new_pos + minimal_movement
        elif y_new_pos < y_old_pos and (y_new_pos - y_old_pos) < 5:
            y_new_pos = y_new_pos - minimal_movement

        if x_new_pos > x_old_pos and (x_new_pos - x_old_pos) < 5:
            x_new_pos = x_new_pos + minimal_movement
        elif x_new_pos < x_old_pos and (x_new_pos - x_old_pos) < 5:
            x_new_pos = x_new_pos - minimal_movement

        print('random_delay: {}'.format(random_delay))
        print('x_old_pos: {}'.format(x_old_pos))
        print('y_old_pos: {}'.format(y_old_pos))
        print('x_new_pos: {}'.format(x_new_pos))
        print('y_new_pos: {}'.format(y_new_pos))
        print('')

        x_servo.angle = x_new_pos
        y_servo.angle = y_new_pos

        x_old_pos = x_new_pos
        y_old_pos = y_new_pos

        time.sleep(random_delay)

        cont += 1


    laser.value = True


if __name__ == '__main__':
    main()
