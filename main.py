#
# The main file where the main loop runs
#
# Author: Ravern Koh
# Created At: 20 July 2017
#

# Import everything [all the strings and errors]
# from within these files
from strings import *
from exceptions import *
from state import *
from actions import *
from time import sleep

# Set this to True in order to debug state
DEBUG = False
# Import the pretty printer for debugging if need be
if DEBUG:
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pprint = pp.pprint

# Set this to True to use SensehatLocal
SENSEHAT_LOCAL = True
if SENSEHAT_LOCAL:
    from sensehat_local import *
else:
    from sensehat import *

# Set this to True to emulate files
EMULATE_FILES = False

# The main loop. Within this is the entire program execution
def main_loop():

    # Cleanliness
    print(MISC_DIVIDER)

    # The actual loop lol
    state = initial_state()
    while True:

        # Surround everything in the loop within
        # a try except. This allows all error handling
        # to be done at the top level, making the code
        # very clean
        try:

            # Print the menu
            str_option = input(PROMPT_MENU)
            print(MISC_DIVIDER) # Cleanliness

            # Ensure option is valid integer
            if not str_option.isdigit():
                raise InvalidOptionException

            # Cast option to an int
            option = int(str_option)

            # Check if int_option is valid
            if not 0 <= option < len(TITLES):
                raise InvalidOptionException

            # Print option title
            print(TITLES[option], end='\n\n')

            # Process the options
            state = process_options(option, state)

            # Check the quit flag
            if has_quit(state): break

            # Print and clear the display
            display_data = get_display(state)
            if display_data:
                print(display_data)
            state = display(False, state)

        # Catch all possible exceptions and print
        except InvalidOptionException:
            print(ERROR_INVALID_OPTION)
        except InvalidDateException:
            print(ERROR_INVALID_DATE)
        except InvalidFileFormatException:
            print(ERROR_INVALID_FILE_FORMAT)
        except BikeFileNotReadException:
            print(ERROR_BIKE_FILE_NOT_READ)
        except RideFileNotReadException:
            print(ERROR_RIDE_FILE_NOT_READ)
        except CancelledException:
            print(ERROR_ACTION_CANCELLED)
        except BikeNotFoundException:
            print(ERROR_BIKE_NOT_FOUND)
        except BikeAlreadyExistsException:
            print(ERROR_BIKE_ALREADY_EXISTS)
        except FileHasBeenReadException:
            print(ERROR_FILE_HAS_BEEN_READ)

        # No matter what happens, do the following steps
        finally:

            # If in debugging mode, print the state
            if DEBUG:
                print(DEBUG_HEADER)
                pprint(state)
                print(DEBUG_FOOTER)

            # Print the divider
            print()
            input(PROMPT_CONTINUE)
            print(MISC_DIVIDER)

        # END TRY
    # END WHILE
# END FUNCTION

# Function that processes the options
# This function takes in the option and the state,
# and it will return the state. Side effects are
# handled here as much as possible.
def process_options(option, state):

    # Bye option. Quit the program
    if option == 0:
        print(MISC_BYE)
        return quit(state)

    # Read from file
    elif option == 1:

        # If file has been read, raise exception
        if bike_file_name(state) or ride_file_name(state):
            raise FileHasBeenReadException

        # Emulate files by hardcoding a dict
        if EMULATE_FILES:
            # Hardcoded state
            return {   'BIKES': [   ['T101', '10/04/2016', '55', '10/01/2017', '25.08'], ['T102', '01/07/2016', '10', '15/05/2017', '30.94'], ['T103', '15/11/2016', '94', '13/06/2017', '83.16'], ['T104', '25/04/2017', '58', '10/01/2017', '25.08'], ['T105', '24/05/2017', '5', '20/06/2017', '93.80']], 'BIKE_FILE': 'data/1.csv', 'DISPLAY': False, 'QUIT?': False, 'RIDES': [   ['T101', '74', '0.27', '78'], ['T105', '40', '0.14', '5'], ['T101', '930', '2.70', '63'], ['T101', '30', '0.07', '55']], 'RIDE_FILE': 'data/2.csv'}
        else:
            # Set the bike_file_name and ride_file_name in the state
            bike_data_file = input_file_name(PROMPT_BIKE_DATA_FILE, 'r')
            state = set_bike_file_name(bike_data_file.name, state)
            ride_data_file = input_file_name(PROMPT_RIDE_DATA_FILE, 'r')
            state = set_ride_file_name(ride_data_file.name, state)
            return read_data(bike_data_file, ride_data_file, state)

    # Display bikes data
    elif option == 2:
        requires_bike_file(state)
        return display_bike_data(state)

    # Display ride data
    elif option == 3:
        requires_ride_file(state)
        bike_no = input(PROMPT_BIKE_NO)
        return display_ride_data(bike_no, state)

    # Add a new bike
    elif option == 4:
        requires_bike_file(state)
        bike_no = input(PROMPT_BIKE_NO_SHORT)
        validate_bike_no(bike_no, state)
        purchase_date = input(PROMPT_PURCHASE_DATE)
        validate_date(purchase_date)
        state = add_bike(bike_no, purchase_date, state)

        # Write data to bike file
        write_bike_data(state)

        # Print success message
        print(MISC_BIKE_ADD_SUCCESS)

        # Return the new state
        return state

    # Service an existing bike
    elif option == 5:

        requires_bike_file(state)

        # Display the bicycles that require servicing
        state = display_bike_data_with_reasons(state)
        display_data = get_display(state)
        print(display_data)

        # Prompt until valid bike returned
        while True:
            try:

                # Prompt for bike no
                bike_no = input(PROMPT_BIKE_NO_SHORT)

                # Service the bike
                new_state = service_bike(bike_no, state)

                # Ensure bike requires servicing
                # This is a small hack that I find
                # is acceptable, given how this app is
                # structured
                if not bike_no in display_data:
                    raise ServicingNotDueException

                # Write to file
                write_bike_data(new_state)

                # Print success message
                print(MISC_BICYCLE_SERVICED)

                # Break since everything went well
                state = new_state
                break

            # Print the errors
            except BikeNotFoundException:
                print(ERROR_BIKE_NOT_FOUND_SHORT)
            except ServicingNotDueException:
                print(ERROR_SERVICING_NOT_DUE)

        # END WHILE

        # Cleanliness
        print()

        # Display the data again
        return display_bike_data_with_reasons(state)

    # Ride a bike
    elif option == 6:

        requires_bike_file(state)

        # Display the bicycles that require servicing
        state = display_bike_data_no_servicing(state)
        display_data = get_display(state)
        print(display_data)
        state = display('', state)

        # Prompt until valid bike returned
        while True:
            try:

                # Prompt for bike no
                bike_no = input(PROMPT_BIKE_NO_SHORT)

                # Ensure bike exists
                bike = get_bike(bike_no, state)

                # Get battery of bike
                battery = bike[BIKE_KEYS.index('Batt %')]
                set_battery_display(int(battery))

                # Ensure bike does not require servicing
                # This is a small hack that I find
                # is acceptable, given how this app is
                # structured
                if not bike_no in display_data:
                    raise ServicingDueException

                # Notify riding bike
                print(MISC_RIDING_BICYCLE.format(bike_no))

                # Get the temperature and orientation
                orientation = get_pitch_roll_yaw()
                temperature = get_temperature()
                temp_to_charge = temperature + 0.5

                # Print the data
                print_orientation_and_temp(orientation, temperature)

                # Cleanliness
                print()

                # Accumulator of the ride data
                ride_data = []

                # Start the loop
                for i in range(0, 15 // 3):

                    # Sleep for 3 seconds
                    sleep(3)

                    # Check if ride data has a record
                    if len(ride_data) == 0:
                        prev_orientation = orientation
                    else:
                        prev_orientation = None

                    # Get the temperature and orientation
                    orientation = get_pitch_roll_yaw()
                    temperature = get_temperature()

                    # Add the ride data to the accum
                    ride_data = add_ride_data(
                        temp_to_charge,
                        temperature,
                        orientation,
                        ride_data,
                        prev_orientation,
                        int(battery)
                    )

                    # Set the SenseHat pixels
                    last_ride_data = ride_data[len(ride_data) - 1]
                    set_battery_display(last_ride_data[len(last_ride_data) - 2])

                # END FOR

                # Print the ride data
                display_data = display_table(HEADERS_RIDE_DATA, ride_data)
                print(display_data)

                # Create a ride record
                last_ride_data = ride_data[len(ride_data) - 1]
                new_state = create_ride_record(bike_no, last_ride_data, state)

                # Update the bike record
                battery = last_ride_data[len(last_ride_data) - 2]
                distance = last_ride_data[len(last_ride_data) - 1]
                new_state = update_bike(bike_no, battery, distance, new_state)

                # Print details
                print(MISC_TRIP_ENDED)
                print()
                print(MISC_TRAVEL_DETAILS.format(distance))
                print(MISC_THANKS)

                # Write the new data to file
                write_bike_data(new_state)
                write_ride_data(new_state)

                # Clear display
                set_battery_display(0)

                # Break since everything went well
                state = new_state
                break

            # Print the errors
            except BikeNotFoundException:
                print(ERROR_BIKE_NOT_FOUND_SHORT)
            except ServicingDueException:
                print(ERROR_SERVICING_DUE)

        # END WHILE

        # Return the state
        return state

    # Print the option not implemented
    else:
        print(MISC_OPTION_NOT_IMPL)
        return state

    # END IFELSE
# END FUNCTION

# Repeats a file name prompt until a
# valid file name is entered. Returns
# the file object
def input_file_name(message, mode):
    print(MISC_CANCEL_HELP)
    file = 0
    while file == 0:
        try:
            file_name = input(message)
            if file_name == MISC_CANCEL:
                raise CancelledException
            # END IF

            # Open the file with read and append permissions
            file = open('data/' + file_name, mode)
        except (FileNotFoundError, IsADirectoryError):
            print(ERROR_INVALID_FILE_NAME)
        # END TRY
    # END WHILE

    # Return the file object
    return file
# END FUNCTION

# Writes the state to bike data file
def write_bike_data(state):
    # Read the file
    file = open(bike_file_name(state), 'w')
    # Get all the bike data and headers
    data = [BIKE_KEYS] + list_bikes([], state)
    # Write line by line
    for bike in data:
        file.write(','.join(bike) + '\n')
# END FUNCTION

def write_ride_data(state):
    # Read the file
    file = open(ride_file_name(state), 'w')
    # Get all the bike data and headers
    data = [RIDE_KEYS] + list_all_rides(state)
    # Write line by line
    for ride in data:
        file.write(','.join(ride) + '\n')
# END FUNCTION


# Raises an exception if bike file has not been read
def requires_bike_file(state):
    if not bike_file_name(state):
        raise BikeFileNotReadException
# END FUNCTION

# Raises an exception if ride file has not been read
def requires_ride_file(state):
    if not ride_file_name(state):
        raise RideFileNotReadException
# END FUNCTION

# Prints the roll, pitch, yaw and temp to the console
def print_orientation_and_temp(data, temp):
    # Print the stuff
    data.append(temp)
    print('Pitch: {}; Roll: {}; Yaw: {}; Temp: {:.1f}'.format(*data))

# Execute the program
main_loop()
