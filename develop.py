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
    max_x = 180

    min_y = 0
    max_y = 180

    # set speed and time range to stop in each position
    min_freeze = 0
    max_freeze = 0
    min_movement = 5
    min_move_time = 3
    max_move_time = 3
    move_loop_time = 0.01

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
        # x_new_pos = random_int(min_x, max_x)
        # y_new_pos = random_int(min_y, max_y)
        x_new_pos = random_float(min_x, max_x)
        y_new_pos = random_float(min_y, max_y)

        random_delay = random_float(min_freeze, max_freeze)
        move_time = random_float(min_move_time, max_move_time, 3)

        # adjust for minimum movement deltas
        if x_new_pos > x_old_pos and (x_new_pos - x_old_pos) < min_movement:
                x_new_pos = x_new_pos + min_movement
        elif x_new_pos < x_old_pos and (x_new_pos - x_old_pos) < min_movement:
                x_new_pos = x_new_pos - min_movement

        if y_new_pos > y_old_pos and (y_new_pos - y_old_pos) < min_movement:
                y_new_pos = y_new_pos + min_movement
        elif y_new_pos < y_old_pos and (y_new_pos - y_old_pos) < min_movement:
                y_new_pos = y_new_pos - min_movement

        # verify servo positions are within min/max ranges
        if x_new_pos < min_x:
            x_new_pos = min_x
        elif x_new_pos > max_x:
            x_new_pos = max_x

        if y_new_pos < min_y:
            y_new_pos = min_y
        elif y_new_pos > max_y:
            y_new_pos = max_y

        # determine angle change per loop based on travel distance and time
        x_delta = abs(x_old_pos - x_new_pos)
        x_steps = (move_time / move_loop_time)
        x_step = (x_delta / x_steps)
        if x_step == 0:
            x_step = 1
        if x_new_pos < x_old_pos:
            x_step = (x_step * -1)

        y_delta = abs(y_old_pos - y_new_pos)
        y_steps = (move_time / move_loop_time)
        y_step = (y_delta / y_steps)
        if y_step == 0:
            y_step = 1
        if y_new_pos < y_old_pos:
            y_step = (x_step * -1)

        # console output: useful for adjusting room size
        print('\n- - - - -')
        print('delay:\t{}'.format(random_delay))
        print('move_time:\t{}'.format(move_time))
        print('x:\t{}\t(old: {})\t(delta: {})\t(step: {})'.format(
            x_old_pos, x_new_pos, x_delta, x_step))
        print('y:\t{}\t(old: {})\t(delta: {})\t(step: {})'.format(
            y_old_pos, y_new_pos, y_delta, y_step))
        print('- - - - -')

        # move servos into position
        print('x_angle:\t{}\t/\ty_angle:\t{} (START)'.format(
            x_servo.angle, y_servo.angle))

        for x_angle, y_angle in zip(
                range(x_old_pos, x_new_pos, x_step),
                range(y_old_pos, y_new_pos, y_step)
        ):
            x_servo.angle = x_angle
            y_servo.angle = y_angle
            print('x_angle:\t{}\t/\ty_angle:\t{}'.format(
                x_servo.angle, y_servo.angle))
            time.sleep(move_loop_time)

        x_servo.angle = x_new_pos
        y_servo.angle = y_new_pos
        print('x_angle:\t{}\t/\ty_angle:\t{} (END)\n- - - - -'.format(
            x_servo.angle, y_servo.angle))

        # set new positions as old for the next loop
        x_old_pos = x_new_pos
        y_old_pos = y_new_pos

        # keep servos in position for set random amount of time
        time.sleep(random_delay)


if __name__ == '__main__':
    main()
