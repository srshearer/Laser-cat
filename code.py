import time
import random
import board
import pulseio
from adafruit_motor import servo
from digitalio import DigitalInOut, Direction


def random_float(x, y, decimals=2):
    return round(random.uniform(x, y), decimals)


def random_int(x, y):
    return random.randint(x, y)


def main():
    # adjust for room size
    min_x = 0
    max_x = 70
    min_y = 150  # keep this at 35 or above
    max_y = 180  # keep this at 165 or below

    # set time range to stop in each position
    min_freeze = 0.03
    max_freeze = 6
    minimal_movement = 5

    ''' initialize laser and servos '''
    # laser at pin D13
    laser = DigitalInOut(board.D13)
    laser.direction = Direction.OUTPUT

    # x servo pin
    pwm_x = pulseio.PWMOut(board.D12, frequency=50)
    x_servo = servo.Servo(pwm_x, min_pulse=750, max_pulse=1500)

    # y servo pin
    pwm_y = pulseio.PWMOut(board.D11, frequency=50)
    y_servo = servo.Servo(pwm_y, min_pulse=750, max_pulse=1500)

    ''' YOU SHOULD NOT HAVE TO MODIFY THE CODE BELOW THIS LINE '''

    # finding center of square for starting point
    x_pos = int(min_x + (max_x - min_x) / 2)
    y_pos = int(min_y + (max_y - min_y) / 2)
    x_old_pos = x_pos
    y_old_pos = y_pos

    x_servo.angle = x_pos
    y_servo.angle = y_pos

    while True:
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

        # verify servo positions are within min/max ranges
        if x_new_pos < min_x:
            x_new_pos = min_x
        elif x_new_pos > max_x:
            x_new_pos = max_x

        if y_new_pos < min_y:
            y_new_pos = min_y
        elif y_new_pos > max_y:
            y_new_pos = max_y

        # console output: useful for adjusting room size
        print('delay:\t{}'.format(random_delay))
        print('x:\t{}\t(old: {})'.format(x_old_pos, x_new_pos))
        print('y:\t{}\t(old: {})\n'.format(y_old_pos, y_new_pos))

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
