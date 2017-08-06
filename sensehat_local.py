#
# Manages any interaction with Sensehat
#
# Author: Ravern Koh
# Created At: 20 July 2017
#

from math import ceil

# Color constants
RED = '#'
GREEN = '@'
BLACK = '.'

# Sensehat constants
DISPLAY_SIZE = 8

# Sets the battery display on the Sensehat
def set_battery_display(batt):
    # Find the number of pixels to be set
    num_pixels = ceil(batt / 2)
    # Loop 8x8 times to fill up display
    for i in range(0, DISPLAY_SIZE**2):
        if i % DISPLAY_SIZE == 0:
            print()
        # Check if even or odd or 0, and
        # fill up the colors accordingly.
        if i < num_pixels - 1:
            print(GREEN, end='')
        elif i == num_pixels - 1:
            if batt % 2 == 1:
                # If the battery is odd
                print(RED, end='')
            else:
                # If the battery is even
                print(GREEN, end='')
        else:
            # Zero
            print(BLACK, end='')
# END FUNCTION

# Return the pitch, roll, yaw in a list
prev = 180
def get_pitch_roll_yaw():
    global prev
    prev += 7
    return [prev, prev, prev]

# Return the temperature
prev_t = 30.5
def get_temperature():
    global prev_t
    prev_t += 0.5
    return prev_t
