# stepper.py
import RPi.GPIO as GPIO
import time
import threading

class StepperMotor:
    def __init__(self, pins, steps_per_rev=512):
        self.pins = pins
        self.steps_per_rev = steps_per_rev
        self.lock = threading.Lock()
        self.sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]

        GPIO.setmode(GPIO.BCM)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

    def move(self, degrees, delay=0.002):
        steps = int(self.steps_per_rev * abs(degrees) / 360)
        direction = 1 if degrees > 0 else -1
        sequence = self.sequence if direction > 0 else list(reversed(self.sequence))

        for _ in range(steps):
            for step in sequence:
                for pin, val in zip(self.pins, step):
                    GPIO.output(pin, val)
                time.sleep(delay)

        self.release()

    def release(self):
        for pin in self.pins:
            GPIO.output(pin, 0)

    def rotate_and_return(self, angle):
        def task():
            with self.lock:
                self.move(angle)
                time.sleep(5)
                self.move(-angle)
        threading.Thread(target=task, daemon=True).start()

    def cleanup(self):
        GPIO.cleanup()
