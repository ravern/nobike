#
# Helpers for date operations
#
# Author: Ravern Koh
# Created At: 20 July 2017
#

# Import datetime, duh.
from datetime import *
from exceptions import *

# Returns todays date as a string
# formatted like "DD/MM/YY"
def today_str():
    return date_to_string(datetime.now())
# END FUNCTION

# Convert date to string
def date_to_string(date):
    return date.strftime('%d/%m/%Y')
# END FUNCTION

# Convert string to date
def string_to_date(str):
    return datetime.strptime(str, '%d/%m/%Y').date()
# END FUNCTION

# Validates a date input
def validate_date(str):
    try:
        datetime.strptime(str, '%d/%m/%Y').date()
    except ValueError:
        raise InvalidDateException
# END FUNCTION

# Checks if the two given dates are
# within `time_delta` of each other
def within_time_delta(lhs, rhs, time_delta):
    return lhs + timedelta(time_delta) > rhs
# END FUNCTION
