import time
import Jetson.GPIO as GPIO

def main():
    pins = [7, 11, 13, 15]
    GPIO.setmode(GPIO.BOARD)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    try:
        while True:
            for pin in pins:
                print(f"Pin {pin} HIGH")
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(1)
                print(f"Pin {pin} LOW")
                GPIO.output(pin, GPIO.LOW)
                time.sleep(1)
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()