import time
import Jetson.GPIO as GPIO

import logging

logger = logging.getLogger(__name__)

class MotorController:
    """
    Controls the motors using GPIO to create motion
    """
    pins = (7, 11, 13, 15)

    def __init__(self, gpio):
        self.gpio = gpio
        gpio.setmode(gpio.BOARD)

        for pin in self.pins:
            gpio.setup(pin, gpio.OUT, initial=gpio.LOW)

    def pulse_motors(self, motor_states: tuple) -> None:
        """
        Pulse the motors in a certain direction
        """
        for pin, state in zip(self.pins, motor_states):
            GPIO.output(pin, state)

    def stop(self):
        """
        Stops all pins and stops motors
        """
        for pin in self.pins:
            self.gpio.output(pin, self.gpio.LOW)

    def move_forward(self):
        """
        Set pins 7 and 13 to high go forward
        """
        logger.info("Pulsing motors forward...")

        forward_pin_state = (GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW)

        self.pulse_motors(forward_pin_state)

    def move_backward(self):
        """
        Set pins 11 and 15 to high go backward
        """
        logger.info("Pulsing motors backward...")
        
        backward_pin_state = (GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.HIGH)

        self.pulse_motors(backward_pin_state)

    def turn_left(self):
        """
        Set pins 7 and 13 to high go forward
        """
        logger.info("Pulsing motors forward...")
        
        forward_pin_state = (GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW)

        self.pulse_motors(forward_pin_state)

    def turn_right(self):
        """
        Set pins 7 and 13 to high go forward
        """
        logger.info("Pulsing motors forward...")
        
        forward_pin_state = (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH)

        self.pulse_motors(forward_pin_state)

if __name__ == "__main__":

    mc = MotorController(GPIO)
    time.sleep(1)
    mc.stop()

    time.sleep(1)
    mc.move_forward()

    time.sleep(1)
    mc.move_backward()

    time.sleep(1)
    mc.stop()