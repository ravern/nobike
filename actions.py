#
# All actions are defined in this file
#
# Author: Ravern Koh
# Created At: 20 July 2017
#

# Import state functions and strings
from strings import *
from state import *

# Reads data from both the files and dumps them
# into the state
def read_data(bike_data_file, ride_data_file, state):

    # Copy the state
    new_state = state.copy()

    # Read bike data file, validating the first line
    raw_lines = bike_data_file.readlines()
    if not raw_lines[0] == ','.join(BIKE_KEYS) + '\n':
        raise InvalidFileFormatException
    bike_data_lines = raw_lines[1:]

    # Loop and add each one as a record into the state
    for line in bike_data_lines:
        cells = line.replace('\n', '').split(',')
        new_state = create_bike(cells, new_state)
    # END FOR

    # Read ride data file, validating the first line
    raw_lines = ride_data_file.readlines()
    if not raw_lines[0] == ','.join(RIDE_KEYS) + '\n':
        raise InvalidFileFormatException
    ride_data_lines = raw_lines[1:]

    # Loop and add each one as a record into the state
    for line in ride_data_lines:
        cells = line.replace('\n', '').split(',')
        new_state = create_ride(cells, new_state)
    # END FOR

    # Display the number of bikes read
    num_bikes_read_str = MISC_NUM_BIKES_READ + str(len(bike_data_lines))
    return display(num_bikes_read_str, new_state)

# END FUNCTION

# Service? key generator
def service_generator(bike):
    # Run it through the reason generator
    reasons = reason_generator(bike)
    # If no reasons return 'N' else 'Y'
    return 'N' if not reasons else 'Y'
# END FUNCTION

# Reason key generator
def reason_generator(bike):

    # Get the index of required keys
    last_maint_idx = BIKE_KEYS.index('Last Maintenance')
    km_since_idx = BIKE_KEYS.index('KM since Last')
    battery_idx = BIKE_KEYS.index('Batt %')

    # More convenience vars
    last_maint_date = string_to_date(bike[last_maint_idx])
    km_since_last = float(bike[km_since_idx])
    battery = int(bike[battery_idx])
    today = string_to_date(today_str())

    # Declare reason accumulator
    reasons = []

    # Checks. Append reasons where checks fail
    if not within_time_delta(last_maint_date, today, 365 / 12 * 6):
        reasons.append('Month')
    if battery < 10:
        reasons.append('Batt')
    if km_since_last > 50:
        reasons.append('KM')

    # If no reasons, return False
    if len(reasons) == 0: return False

    # Otherwise return the reasons as a string
    return ' & '.join(reasons)

# END FUNCTION

# Validates a bike number
def validate_bike_no(bike_no, state):
    # Check if it looks correct
    if not bike_no[0] == 'T':
        raise InvalidBikeNoException
    # Check if it already exists
    try:
        get_bike(bike_no, state)
        raise BikeAlreadyExistsException
    except BikeNotFoundException:
        pass
# END FUNCTION


# Displays the bike data
def display_bike_data(state):
    # Get bikes content
    bikes = list_bikes([service_generator], state)
    # Render table to a string
    data = display_table(BIKE_KEYS + ['Service?'], bikes)
    # Display the data to the screen
    return display(data, state)
# END FUNCTION

# Displays a list of bicycles that require
# servicing, and their reaons
def display_bike_data_with_reasons(state):
    # Create headers
    headers = BIKE_KEYS.copy()
    headers.remove('Purchase Date')
    # Get bikes content
    bikes = list_bikes_with_fields([reason_generator], headers, state)
    # Filter out the bikes with no reasons
    require_service = lambda bike: bike[len(bike) - 1]
    bikes = list(filter(require_service, bikes))
    # Render the table into a string
    data = display_table(headers + ['Reason/s'], bikes)
    # Display the data to the screen
    return display(data, state)
# END FUNCTION

# Displays a list of biycles that do not
# require servicing
def display_bike_data_no_servicing(state):
    # Create headers
    headers = BIKE_KEYS.copy()
    headers.remove('Last Maintenance')
    headers.remove('Purchase Date')
    # Get bikes content
    bikes = list_bikes_with_fields([service_generator], headers, state)
    # Filter out bikes needing service
    doesnt_require_service = lambda bike: bike[len(bike) - 1] == 'N'
    bikes = list(filter(doesnt_require_service, bikes))
    # Render the table into a string
    data = display_table(headers, bikes)
    # Display the data to the screen
    return display(data, state)
# END FUNCTION

# Displays the ride data of the selected bike
def display_ride_data(bike_no, state):
    # Get ride content
    rides = list_rides(bike_no, state)
    # Render the table into a string
    data = display_table(RIDE_KEYS, rides)
    # Display the data to the screen
    return display(data, state)
# END FUNCTION

# Displays a table of info based on array of headers
# and array of content
def display_table(headers, contents):

    # Initialize the accumulator
    lines = []

    # Write the header content first
    lines.append(' '.join(headers))

    # Write the dividers
    # map explaination: 'Bike No.' => '--------'
    dividers = list(map(lambda key: '-' * len(key), headers))
    lines.append(' '.join(dividers))

    # Write the content
    for content in contents:

        # Zip the keys and values
        # zip explaination: zip([1, 2], [3, 4]) == [{1, 2}, {3, 4}]
        content_with_keys = zip(headers, content)

        # Map over the rides with their keys and format
        format_string = lambda raw: '{:<{length}}'.format(raw[1], length=len(raw[0]))
        cells = list(map(format_string, content_with_keys))

        # Add them to data
        lines.append(' '.join(cells))

    # END FOR

    # This is a hack. I will fix this if
    # I have time
    # Find the longest line
    header_length = len(lines[0])
    content_max_length = max(list(map(len, lines[2:])))
    extra_length = max(content_max_length - header_length, 0)

    # Add all the extra '-'s
    lines[1] += '-' * extra_length

    # Return the accumulator
    return '\n'.join(lines) + '\n'

# END FUNCTION

# Adds a bicycle by appending it to the
# state and to the file
def add_bike(bike_no, purchase_date, state):
    # Create the content in memory
    state = create_custom_bike(bike_no, purchase_date, state)
    # Return the new state
    return state
# END FUNCTION

# Appends a new row of ride data to the
# ride_data passed in. Returns new ride
# data
def add_ride_data(temp_to_charge, temperature, orientation, ride_data, prev_orient, prev_batt):

    # Get the previous data
    if prev_orient is None:
        last_ride = ride_data[len(ride_data) - 1]
        prev_orient = last_ride[:3]
        prev_batt = last_ride[len(last_ride) - 2]
        prev_km = last_ride[len(last_ride) - 1]
    else:
        prev_km = 0

    # Create new vars
    new_batt = prev_batt
    new_km = prev_km

    # Validate if movement or not
    if calc_cum_change(prev_orient, orientation) > 20:
        movement = True
    else:
        movement = False

    # Lose battery if no movement
    if not movement:
        new_batt -= 1

    # If conditions fulfilled, add to km and batt
    if movement and temperature > temp_to_charge:
        new_batt += 1
        new_km += 0.01

    # Copy ride data
    new_ride_data = ride_data.copy()

    # Append the new ride data
    new_ride_data.append(orientation + [str(movement), temperature, new_batt, new_km])

    # Return the new ride data
    return new_ride_data

# END FUNCTION

# Creates a ride record based on some ride data
def create_ride_record(bike_no, ride_data, state):
    # Generate ride info
    ride = [
        bike_no,
        str(15),
        '{:.2f}'.format(float(ride_data[len(ride_data) - 1])),
        str(ride_data[len(ride_data) - 2])
    ]
    # Add it to state
    new_state = create_ride(ride, state)
    # Return the new state
    return new_state
# END FUNCTION

# Calculate absolute change between 2 lists of 3
def calc_cum_change(lhs, rhs):
    # Zip the two lists together
    zipped = zip(lhs, rhs)
    # Map over zipped and return the
    # abs(lhs - rhs)
    return sum(map(lambda x: abs(x[0] - x[1]), zipped))
