# Imports
from adafruit_crickit import crickit
from random import choice, randint
from time import

# Global constants
METER_MIN = 0
METER_MAX = 10
# The following is a dictionary that corresponds meter levels to servo angles, 
# e.g. level 5 is at angle 90.  Adjust this if you want to change the layout of the meter.
SERVO_ANGLES = {0:0, 1:18, 2:36, 3:54, 4:72, 5:90, 6:108, 7:126, 8:144, 9:162, 10:180}
# Folder names for music groups:
MUSIC_GROUP_1_PATH = "/home/pi/love-meter/group1/"
MUSIC_GROUP_2_PATH = "/home/pi/love-meter/group2/"
MUSIC_GROUP_3_PATH = "/home/pi/love-meter/group3/"
# Assuming servo is connected to servo1 connector.  Change this if using a different port.
METER_SERVO = crickit.servo1

# Global variables
# Start with a random love level from 5 to 8.
# This is the level the meter *will* show when the handle is pulled, 
# it doesn't set the meter's current position.
love_level = randint(5, 8)

# Functions
def play_music(file):
    """ Play the music file via the system sound. """
    pass

def meter_increment(love):
    """ Add one to level, but keep within meter range. """
    return min(love + 1, METER_MAX)

def set_meter(level):
    """ Set servo to corresponding meter level, as specified by SERVO_ANGLES. """
    # Check we've received an appropriate level first:
    if level in SERVO_ANGLES:
        METER_SERVO.angle = SERVO_ANGLES[level]

# Main code.

    


