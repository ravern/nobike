#
# All of this programs state is accessed
# and modified from this file
#
# Author: Ravern Koh
# Created At: 20 July 2017
#

# Import date operations and errors
from date_helpers import *
from exceptions import *

# The constants used internally
BIKE_FILE_KEY = "BIKE_FILE"
RIDE_FILE_KEY = "RIDE_FILE"
QUIT_KEY = 'QUIT?'
DISPLAY_KEY = "DISPLAY"
BIKES_KEY = 'BIKES'
RIDES_KEY = 'RIDES'
BIKE_KEYS = ['Bike No.', 'Purchase Date', 'Batt %', 'Last Maintenance', 'KM since Last']
RIDE_KEYS = ['Bike No.', 'Ride duration', 'Ride distance', 'Battery %']

# The initial state of this program
def initial_state():
    return {
        BIKES_KEY: [],
        RIDES_KEY: [],
        QUIT_KEY: False,
        DISPLAY_KEY: False,
        BIKE_FILE_KEY: False,
        RIDE_FILE_KEY: False
    }
# END FUNCTION

# Creates a bike record within the state
def create_bike(data, state):
    # Add the data to the new state
    new_bikes = state[BIKES_KEY].copy()
    new_bikes.append(data)
    return set_state(BIKES_KEY, new_bikes, state)
# END FUNCTION

# Creates a custom bike (for option 4)
def create_custom_bike(bike_no, purchase_date, state):

    # Check whether bike already exists. If
    # it does, raise BikeAlreadyExistsException
    try:
        get_bike(bike_no, state)
        raise BikeAlreadyExistsException
    except BikeNotFoundException: pass
    # END TRY

    # Add the data to the state, with the
    # default values in place
    new_bikes = state[BIKES_KEY].copy()
    new_bikes.append([bike_no, purchase_date, "100", today_str(), "0.00"])
    return set_state(BIKES_KEY, new_bikes, state)

# END FUNCTION

# Services an existing bike
# Raises BikeNotFoundException if not found
def service_bike(bike_no, state):

    # Get the index of the bike no. key
    bike_no_idx = BIKE_KEYS.index('Bike No.')

    # Copy the bikes
    new_bikes = state[BIKES_KEY].copy()

    # Loop to find the bike
    new_bike_idx = -1
    new_bike = False
    for i in range(0, len(new_bikes)):
        bike = new_bikes[i]
        if bike[bike_no_idx] == bike_no:
            new_bike_idx = i
            new_bike = bike.copy()

    # Raise exception if bike hasn't been found
    if not new_bike: raise BikeNotFoundException

    # Otherwise set the new bike's data and set it
    # in the array
    new_bike = [new_bike[0], new_bike[1], "100", today_str(), "0.00"]
    new_bikes[new_bike_idx] = new_bike

    # Set the value in the state
    return set_state(BIKES_KEY, new_bikes, state)

# END FUNCTION

# Get data of all the bikes, with extra fields as
# requested
def list_bikes(generators, state):

    # Convenience var to access current bikes
    state_bikes = state[BIKES_KEY]

    # Return value accumulator
    bikes = []

    # Loop through the list
    for state_bike in state_bikes:

        # Copy the existing data
        bike = state_bike.copy()

        # Add new fields
        for generator in generators:
            # Use the generator to create the data
            # then add it to the bike
            bike.append(generator(bike))
        # END FOR

        # Add this bike object to the main bikes array
        bikes.append(bike)

    # END FOR

    # Return the accumulator
    return bikes

# END FUNCTION

# Get data, excluding certain fields
def list_bikes_with_fields(generators, fields, state):

    # Get the list of bikes first
    state_bikes = list_bikes(generators, state)

    # Return value accumulator
    # Create empty array same size as `state_bikes`
    bikes = list(map(lambda x: [], state_bikes))

    # Loop through excluded fields
    for field in fields:

        # Get index of field
        try: index = BIKE_KEYS.index(field)
        except ValueError: continue

        # Loop through all the bikes and append value
        for i in range(0, len(state_bikes)):
            bikes[i].append(state_bikes[i][index])
        # END FOR

    # END FOR

    # Append the generator fields at the back
    for k in range(0, len(generators)):
        j = len(generators) - k
        # Loop through all the bikes and append value
        for i in range(0, len(state_bikes)):
            bikes[i].append(state_bikes[i][len(state_bikes[i]) - j])
        # END FOR

    # Return the list of bikes
    return bikes

# END FUNCTION

# Get a bike by its Bike No.
# Raises a BikeNotFoundException if the bike is
# not found
def get_bike(bike_no, state):

    # Get the index of bike no. key
    bike_no_idx = BIKE_KEYS.index('Bike No.')

    # Filter in all the bikes whose
    # bike no. == `bike_no`
    filtered_bikes = []
    for bike in state[BIKES_KEY]:
        # `bike[key_idx]` get the bike no.
        if bike[bike_no_idx] == bike_no:
            filtered_bikes.append(bike)

    # Raise exception if not found
    if len(filtered_bikes) == 0:
        raise BikeNotFoundException

    # Return the data of the first bike
    return filtered_bikes[0]

# END FUNCTION

# Creates a ride record within the state
def create_ride(data, state):
    # Add the data to the new state
    new_rides = state[RIDES_KEY].copy()
    new_rides.append(data)
    return set_state(RIDES_KEY, new_rides, state)
# END FUNCTION

# List all rides.
def list_rides(state):
    return state[RIDES_KEY]
# END FUNCTION

# Get the ride data of a certain bike.
# Raises BikeNotFoundException if not found
def list_rides(bike_no, state):

    # Get the index of bike no. key
    bike_no_idx = RIDE_KEYS.index('Bike No.')

    # Filter in all the bikes whose
    # bike no. == `bike_no`
    filtered_rides = []
    for ride in state[RIDES_KEY]:
        # `ride[key_idx]` get the bike no.
        if ride[bike_no_idx] == bike_no:
            filtered_rides.append(ride)

    # Raise exception if not found
    if len(filtered_rides) == 0:
        raise BikeNotFoundException

    # Return the ride data
    return filtered_rides

# END FUNCTION

# Sets quit flag to true
def quit(state):
    # Set the quit flag
    return set_state(QUIT_KEY, True, state)
# END FUNCTION

# Return whether the quit flag has been set
def has_quit(state): return state[QUIT_KEY]

# Sets the bike file name
def set_bike_file_name(file_name, state):
    # Set the bike_file_name
    return set_state(BIKE_FILE_KEY, file_name, state)
# END FUNCTION

# Return the name of the bike file
def bike_file_name(state): return state[BIKE_FILE_KEY]

# Sets the ride file name
def set_ride_file_name(file_name, state):
    # Set the ride_file_name
    return set_state(RIDE_FILE_KEY, file_name, state)
# END FUNCTION

# Return the name of the ride file
def ride_file_name(state): return state[RIDE_FILE_KEY]

# Sets the display data to the param provided
def display(data, state):
    # Set the display data
    return set_state(DISPLAY_KEY, data, state)
# END FUNCTION

# Returns the display data
def get_display(state): return state[DISPLAY_KEY]

# Utilty function to do quick state sets
def set_state(key, value, state):
    # Copy the old state
    new_state = state.copy()
    # Set the value
    new_state[key] = value
    # Return the resulting state
    return new_state
# END FUNCTION
