import time
import Jetson.GPIO as GPIO

IN1, IN2, IN3, IN4 = 7, 11, 13, 15
PINS = (IN1, IN2, IN3, IN4)
battery_disconnected = False

def set_outputs(states):
    for pin, state in zip(PINS, states):
        GPIO.output(pin, state)

def stop():
    set_outputs((GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW))

def pulse(label, states):
    print(f"\n{label} — running for 1 second")
    set_outputs(states)
    time.sleep(1)
    stop()
    print("STOP")
    time.sleep(1)

GPIO.setmode(GPIO.BOARD)
for pin in PINS:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

try:
    stop()
    input(
        "\nAll inputs are LOW. Connect the motor battery, "
        "keep the tracks raised, then press Enter..."
    )

    pulse("Motor A — FORWARD", (GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW))
    pulse("Motor A — BACKWARD", (GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.HIGH))
    pulse("Motor B — LEFT", (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
    pulse("Motor B — RIGHT", (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))

    stop()
    input("\nTests finished. Disconnect the motor battery, then press Enter...")
    battery_disconnected = True
finally:
    stop()
    if not battery_disconnected:
        input("\nSTOP asserted. Disconnect the motor battery, then press Enter...")
    GPIO.cleanup()
    print("GPIO cleaned up safely.")