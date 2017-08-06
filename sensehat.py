#
# Manages any interaction with Sensehat
#
# Author: Ravern Koh
# Created At: 20 July 2017
#

# Import Sensehat in order to use it
from sense_hat import SenseHat

# Need to use ceil to round up the
# battery percentage
from math import ceil

# Color constants
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLACK = [0, 0, 0]

# Sensehat constants
DISPLAY_SIZE = 8

# Initialize sensehat. Use low-light to avoid
# burning my eyes.
s = SenseHat()
s.low_light = True

# Sets the battery display on the Sensehat
def set_battery_display(batt):
    # Return value accumulator
    pixels = []
    # Find the number of pixels to be set
    num_pixels = ceil(batt / 2)
    # Loop 8x8 times to fill up display
    for i in range(0, DISPLAY_SIZE**2):
        # Check if even or odd or 0, and
        # fill up the colors accordingly.
        if i < num_pixels - 1:
            pixels.append(GREEN)
        elif i == num_pixels - 1:
            if batt % 2 == 1:
                # If the battery is odd
                pixels.append(RED)
            else:
                # If the battery is even
                pixels.append(GREEN)
        else:
            # Zero
            pixels.append(BLACK)
    # Set the pixels on Sensehat
    s.set_pixels(pixels)
# END FUNCTION

# Return the pitch, roll, yaw in a list
def get_pitch_roll_yaw():
    return list(map(lambda x: round(x), s.get_orientation().values()))

# Return the temperature
def get_temperature():
    return round(s.get_temperature(), 1)
