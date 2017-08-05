#
# Manages any interaction with Sensehat
#
# Author: Ravern Koh
# Created At: 20 July 2017
#

# Color constants
RED = '#'
GREEN = '@'
BLACK = '.'

# Sensehat constants
DISPLAY_SIZE = 8

# Sets the battery display on the Sensehat
def set_battery_display(batt):
    num_batt = batt // 2
    for y in range(0, DISPLAY_SIZE):
        for x in range(0, DISPLAY_SIZE):
            idx = x + y * DISPLAY_SIZE
            if idx > num_batt:
                if idx % 2 == 0:
                    print(RED, end='')
                else:
                    print(GREEN, end='')
            else:
                print(BLACK, end='')
        print()
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
