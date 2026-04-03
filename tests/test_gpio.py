import time
import Jetson.GPIO as GPIO

def main():
    import time
    import Jetson.GPIO as GPIO

    IN1 = 7
    IN2 = 11
    IN3 = 13
    IN4 = 15

    GPIO.setmode(GPIO.BOARD)
    for pin in [IN1, IN2, IN3, IN4]:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    try:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        time.sleep(10)
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()