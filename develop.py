import time
import random
import itertools
# import board
# import pulseio
# from adafruit_motor import servo
# from digitalio import DigitalInOut, Direction


class Servo(object):
    def __init__(self, controller, min_pulse=1000, max_pulse=2000):
        self.controller = controller,
        self.min_pulse = min_pulse,
        self.max_pulse = max_pulse,
        self.angle = None


class CatServo(Servo):
    def __init__(self, *args, **kwargs):
        super(Servo, self).__init__(*args, **kwargs)
        self.move_range = {'min': None, 'max': None}
        self.freeze_range = {'min': None, 'max': None}
        self.speed_range = {'min': None, 'max': None}
        self.minimal_movement = 5
        self.speed_step = 3
        self.position = None
        self.old_position = None
        self.new_position = None


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

    # set speed and time range to stop in each position
    min_freeze = 0
    max_freeze = 0
    minimal_movement = 5
    step = 3
    min_speed = 0.005
    max_speed = 0.3

    ''' initialize laser and servos '''
    # laser at pin D13
    laser = None  # DigitalInOut(board.D13)
    # laser.direction = Direction.OUTPUT

    # x servo pin
    # pwm_x = pulseio.PWMOut(board.D12, frequency=50)
    # x_servo = servo.Servo(pwm_x, min_pulse=750, max_pulse=1500)
    pwm_x = 'x_controller'
    x_servo = Servo(pwm_x, min_pulse=750, max_pulse=1500)

    # y servo pin
    # pwm_y = pulseio.PWMOut(board.D11, frequency=50)
    # y_servo = servo.Servo(pwm_y, min_pulse=750, max_pulse=1500)
    pwm_y = 'y_controller'
    y_servo = Servo(pwm_y, min_pulse=750, max_pulse=1500)

    ''' YOU SHOULD NOT HAVE TO MODIFY THE CODE BELOW THIS LINE '''

    # finding center of square for starting point
    x_pos = int(min_x + (max_x - min_x) / 2)
    y_pos = int(min_y + (max_y - min_y) / 2)
    x_old_pos = x_pos
    y_old_pos = y_pos

    x_servo.angle = x_pos
    y_servo.angle = y_pos

    # laser on
    # laser.value = True

    while True:
        # get random values x & y position, speed, and delay
        x_new_pos = random_int(min_x, max_x)
        y_new_pos = random_int(min_y, max_y)

        random_delay = random_float(min_freeze, max_freeze)
        speed = random_float(min_speed, max_speed, 3)

        # adjust for minimum movement deltas
        if x_new_pos > x_old_pos:
            x_step = step
            if (x_new_pos - x_old_pos) < minimal_movement:
                x_new_pos = x_new_pos + minimal_movement
        elif x_new_pos < x_old_pos:
            x_step = (step * -1)
            if (x_new_pos - x_old_pos) < minimal_movement:
                x_new_pos = x_new_pos - minimal_movement

        if y_new_pos > y_old_pos:
            y_step = step
            if (y_new_pos - y_old_pos) < minimal_movement:
                y_new_pos = y_new_pos + minimal_movement
        elif y_new_pos < y_old_pos:
            y_step = (step * -1)
            if (y_new_pos - y_old_pos) < minimal_movement:
                y_new_pos = y_new_pos - minimal_movement

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
        print('\n- - - - -')
        print('delay:\t{}'.format(random_delay))
        print('speed:\t{}'.format(speed))
        print('x:\t{}\t(old: {})'.format(x_old_pos, x_new_pos))
        print('y:\t{}\t(old: {})'.format(y_old_pos, y_new_pos))
        print('- - - - -')

        # move servos into position
        print('x_angle:\t{}\ty_angle:\t{} (START)'.format(
            x_servo.angle, y_servo.angle))

        for x_angle, y_angle in itertools.product(
                range(x_old_pos, x_new_pos, x_step),
                range(y_old_pos, y_new_pos, y_step)
        ):
            x_servo.angle = x_angle
            y_servo.angle = y_angle
            print('x_angle:\t{}\ty_angle:\t{}'.format(
                x_servo.angle, y_servo.angle))
            time.sleep(speed)

        x_servo.angle = x_new_pos
        y_servo.angle = y_new_pos
        print('x_angle:\t{}\ty_angle:\t{} (END)\n- - - - -'.format(
            x_servo.angle, y_servo.angle))

        # set new positions as old for the next loop
        x_old_pos = x_new_pos
        y_old_pos = y_new_pos

        # keep servos in position for set random amount of time
        time.sleep(random_delay)


if __name__ == '__main__':
    main()
