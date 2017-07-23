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

# Set this to True in order to debug state
DEBUG = False
# Import the pretty printer for debugging if need be
if DEBUG:
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pprint = pp.pprint

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
        purchase_date = input(PROMPT_PURCHASE_DATE)
        bike_data_file = open(bike_file_name(state), 'a')
        return add_bike(bike_no, purchase_date, bike_data_file, state)

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

# Raises an exception if bike file has not been read
def requires_bike_file(state):
    if not bike_file_name(state):
        raise BikeFileNotReadException

# Raises an exception if ride file has not been read
def requires_ride_file(state):
    if not ride_file_name(state):
        raise RideFileNotReadException

# Execute the program
main_loop()
