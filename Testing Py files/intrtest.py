import machine
import time

# Define the reset button pin
reset_button_pin = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

# Initialize variables
long_press_duration = 4  # 5 seconds

try:
    while True:
        # Check if the reset button is pressed for 5 seconds consecutively
        start_time = time.time()
        pressed_count = 0
        while time.time() - start_time < long_press_duration:
            if reset_button_pin.value() == 0:
                pressed_count += 1
                if pressed_count >= long_press_duration * 10:  # Sampling every 0.1 seconds
                    print("Reset button pressed for 5 seconds consecutively!")
                    break
            else:
                pressed_count = 0
            time.sleep(0.1)  # Sampling interval
except KeyboardInterrupt:
    print("Program terminated.")