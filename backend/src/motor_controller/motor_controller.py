import time

import logging

logger = logging.getLogger(__name__)

class MotorController:
    """
    Controls the motors using self.gpio to create motion
    """
    pins = (7, 11, 13, 15)

    def __init__(self):
        self.gpio = self.get_gpio()
        if self.gpio:
            self.gpio.setmode(self.gpio.BOARD)

            for pin in self.pins:
                self.gpio.setup(pin, self.gpio.OUT, initial=self.gpio.LOW)

    @staticmethod
    def get_gpio() -> None:
        """
        Lazily import self.gpio - we not be able to on mac
        """
        print("importing gpio")
        try:
            import Jetson.GPIO as GPIO
            print("self.gpio import available, setting self.gpio")
            return GPIO
        except Exception as e:
            print(f"No self.gpio available, error: {e}")
            

    def parse_ws_event(self, event: str) -> None:
        """
        This function consumes websocket events from the server.
        It checks if the movement is a stop command, then checks if the 
        command is one of the directions we support.
        If it's not supported, we throw a warning and stop.
        The ws should send a stop command on button up - so we should get 
        away with just setting the self.gpio values and waiting for the stop command
        """

        if event["type"] == "stop_movement":
            self.stop()
            return
        
        commands = {
            "forward" : self.move_forward,
            "backward" : self.move_backward,
            "right" : self.turn_right,
            "left" : self.turn_left
        }

        try:
            commands[event["direction"]]()
        except:
            self.stop()
            logger.warning(f"Unregistered direction command parsed from websocket: {event["direction"]}")




    def pulse_motors(self, motor_states: tuple) -> None:
        """
        Pulse the motors in a certain direction
        """
        for pin, state in zip(self.pins, motor_states):
            self.gpio.output(pin, state)

    def stop(self):
        """
        Stops all pins and stops motors
        """
        print("Stopping motors...")
        if self.gpio:
            for pin in self.pins:
                self.gpio.output(pin, self.gpio.LOW)

    def move_forward(self):
        """
        Set pins 7 and 13 to high go forward
        """
        print("Pulsing motors forward...")

        if self.gpio:
            forward_pin_state = (self.gpio.HIGH, self.gpio.LOW, self.gpio.HIGH, self.gpio.LOW)

            self.pulse_motors(forward_pin_state)

    def move_backward(self):
        """
        Set pins 11 and 15 to high go backward
        """
        logger.info("Pulsing motors backward...")
        print("Pulsing motors backward...")
        
        if self.gpio:
            backward_pin_state = (self.gpio.LOW, self.gpio.HIGH, self.gpio.LOW, self.gpio.HIGH)

            self.pulse_motors(backward_pin_state)

    def turn_left(self):
        """
        Set pins 7 and 13 to high go forward
        """
        logger.info("Pulsing motors left...")
        print("Pulsing motors left...")

        if self.gpio:
            left_pin_state = (self.gpio.LOW, self.gpio.HIGH, self.gpio.HIGH, self.gpio.LOW)

            self.pulse_motors(left_pin_state)

    def turn_right(self):
        """
        Set pins 7 and 13 to high go forward
        """
        logger.info("Pulsing motors forward...")
        
        if self.gpio:
            right_pin_state = (self.gpio.HIGH, self.gpio.LOW, self.gpio.LOW, self.gpio.HIGH)

            self.pulse_motors(right_pin_state)

if __name__ == "__main__":

    mc = MotorController()
    time.sleep(1)
    mc.stop()

    time.sleep(1)
    mc.move_forward()

    time.sleep(1)
    mc.move_backward()

    time.sleep(1)
    mc.turn_left()

    time.sleep(1)
    mc.turn_right()

    time.sleep(1)
    mc.stop()