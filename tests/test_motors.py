import time
import Jetson.GPIO as GPIO

ENA = 29
IN1 = 7
IN2 = 11
IN3 = 13
IN4 = 15
ENB = 31

PINS = [ENA, IN1, IN2, IN3, IN4, ENB]


def stop_all():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


def enable_motors():
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(ENB, GPIO.HIGH)


def disable_motors():
    GPIO.output(ENA, GPIO.LOW)
    GPIO.output(ENB, GPIO.LOW)


def left_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)


def left_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)


def right_forward():
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)


def right_backward():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)


def main():
    GPIO.setmode(GPIO.BOARD)

    for pin in PINS:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    try:
        print("Enable motors")
        enable_motors()

        print("STOP")
        stop_all()
        time.sleep(2)

        print("LEFT FORWARD")
        stop_all()
        left_forward()
        time.sleep(3)

        print("STOP")
        stop_all()
        time.sleep(2)

        print("RIGHT FORWARD")
        stop_all()
        right_forward()
        time.sleep(3)

        print("STOP")
        stop_all()
        time.sleep(2)

        print("BOTH FORWARD")
        stop_all()
        left_forward()
        right_forward()
        time.sleep(3)

        print("STOP")
        stop_all()
        time.sleep(2)

        print("LEFT BACKWARD")
        stop_all()
        left_backward()
        time.sleep(3)

        print("STOP")
        stop_all()
        time.sleep(2)

        print("RIGHT BACKWARD")
        stop_all()
        right_backward()
        time.sleep(3)

        print("STOP")
        stop_all()
        time.sleep(2)

        print("BOTH BACKWARD")
        stop_all()
        left_backward()
        right_backward()
        time.sleep(3)

        print("FINAL STOP")
        stop_all()
        disable_motors()

    finally:
        stop_all()
        disable_motors()
        GPIO.cleanup()


if __name__ == "__main__":
    main()