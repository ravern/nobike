#
# Defines all the error classes used
# within this program
#
# Author: Ravern Koh
# Created At: 20 July 2017
#

class InvalidOptionException(Exception): pass
class BikeFileNotReadException(Exception): pass
class RideFileNotReadException(Exception): pass
class FileHasBeenReadException(Exception): pass
class InvalidFileFormatException(Exception): pass
class InvalidDateException(Exception): pass
class InvalidBikeNoException(Exception): pass
class CancelledException(Exception): pass
class BikeNotFoundException(Exception): pass
class BikeAlreadyExistsException(Exception): pass
class ServicingNotDueException(Exception): pass
class ServicingDueException(Exception): pass
