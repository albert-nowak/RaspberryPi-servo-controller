#!/usr/bin/python
import time
import RPi.GPIO as GPIO

# Constans Vars
FILENAME = ""
WAIT_TIME = 5 			# 5 seconds


class Servo:
    pwm_pin = 18
    delay_period = 0.02
    in_progress = False

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, 100)
        self.pwm.start(0)
        self.in_progress = True
        self.pwm.ChangeDutyCycle(2.5)
        self.in_progress = False

    def update(self, angle):
        self.in_progress = True
        self.pwm.ChangeDutyCycle(self.countAngle(angle))
        self.in_progress = False

    def clean(self):
        if not self.in_progress:
            self.pwm.ChangeDutyCycle(2.5)
            self.pwm.stop()
            GPIO.cleanup()

    def greeting(self):
        self.in_progress = True
        time.sleep(1)
        for angle in range(0, 180, 1):
            self.pwm.ChangeDutyCycle(self.countAngle(angle))
            time.sleep(self.delay_period)
        time.sleep(0.01)
        for angle in range(150, 0, -1):
            self.pwm.ChangeDutyCycle(self.countAngle(angle))
            time.sleep(self.delay_period)
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(self.countAngle(90))
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(self.countAngle(0))
        time.sleep(0.5)
        self.in_progress = False

    def countAngle(self, angle):
        return float(angle) / 10.0 + 2.5


def main():

    servo = Servo()
    servo.greeting()

    max_value = 0
    prevous_line = ""
    curr_degree = 0

    with open(FILENAME, 'r') as file:
        for line in file:
            line = line[:-1]
            servo.update(curr_degree)
            time.sleep(3)

            if float(line) > max_value:
                max_value = float(line)
            else:
                max_value = float(prevous_line)
                curr_degree -= 10
                time.sleep(5)

                while(curr_degree <= 180):
                    servo.update(curr_degree)
                    time.sleep(WAIT_TIME)
                    curr_degree += 10

                servo.update(0)
                time.sleep(2)
                servo.clean()
                break

            curr_degree += 10
            prevous_line = line


if __name__ == "__main__":
    main()
