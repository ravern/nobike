#
# Defines all the strings used within this program,
# for the sake of cleanliness
#
# Author: Ravern Koh
# Created At: 20 July 2017
#

# Debug
DEBUG_HEADER = """
======================== DEBUG ========================
"""
DEBUG_FOOTER = """
====================== END DEBUG ======================
"""

# Misc.
MISC_DIVIDER = """
-------------------------------------------------------
"""
MISC_BYE = "Bye!"
MISC_CANCEL_HELP = "You may enter 'cancel' to end this action."
MISC_CANCEL = "cancel"
MISC_NUM_BIKES_READ = "Number of bicycles read: "
MISC_OPTION_NOT_IMPL = "This option has not been implemented."
MISC_BICYCLE_SERVICED = "Bicycle serviced."
MISC_RIDING_BICYCLE = "Riding Bike No. {}..."

# Prompts
PROMPT_MENU = """\
ADMIN MENU
==========
[1] Read bicycle info from file
[2] Display all bicycle info with servicing indication
[3] Display selected bicycle info
[4] Add a bicycle
[5] Perform bicycle maintenance

RIDER MENU
==========
[6]  Ride a bicycle

[0]  Exit
Enter your option: \
"""
PROMPT_BIKE_DATA_FILE = "Enter the name of the bike data file: "
PROMPT_RIDE_DATA_FILE = "Enter the name of the ride data file: "
PROMPT_BIKE_NO = "Enter a bike no.: "
PROMPT_CONTINUE = "Press enter to continue"
PROMPT_BIKE_NO_SHORT = "Bike No.: "
PROMPT_PURCHASE_DATE = "Purchase Date: "
PROMPT_BIKE_DATA_FILE_WRITE = "Enter the name of the bike data file to write to: "

# Titles
TITLES = [
    "Option 0: Quit",
    "Option 1: Read bicycle info from file",
    "Option 2: Display all bicycle info with servicing indication",
    "Option 3: Display selected bicycle info",
    "Option 4: Add a bicycle",
    "Option 5: Perform bicycle maintenance",
    "Option 6: Ride a bicycle"
]

# Errors
ERROR_INVALID_OPTION = "Your chosen option does not exist."
ERROR_INVALID_FILE_FORMAT = "The file does not have the correct file format."
ERROR_BIKE_FILE_NOT_READ = "You need to read in the bike data file first."
ERROR_RIDE_FILE_NOT_READ = "You need to read in the ride data file first."
ERROR_ACTION_CANCELLED = "You have cancelled the action."
ERROR_INVALID_FILE_NAME = "The file does not exist."
ERROR_BIKE_NOT_FOUND = "The bike you entered could not be found."
ERROR_BIKE_ALREADY_EXISTS = "The bike you entered already exists."
ERROR_SERVICING_NOT_DUE = "Bike is not due for servicing."
ERROR_BIKE_NOT_FOUND_SHORT = "No such bicycle"
