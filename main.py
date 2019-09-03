# Imports
from adafruit_crickit import crickit
from random import choice, randint
from time import time, sleep
from os import listdir

# Global constants
# Range of meter
METER_MIN = 0
METER_MAX = 10
# The following is a dictionary that corresponds meter levels to servo angles, 
# e.g. level 5 is at angle 90.  Adjust this if you want to change the layout of the meter
# or to match the orientation of the servo.
SERVO_ANGLES = {0:180, 1:162, 2:144, 3:126, 4:108, 5:90, 6:72, 7:54, 8:36, 9:18, 10:0}
# Previous version:
# SERVO_ANGLES = {0:0, 1:18, 2:36, 3:54, 4:72, 5:90, 6:108, 7:126, 8:144, 9:162, 10:180}

# Folder names for music groups:
GROUP1_PATH = "/home/pi/love-meter/group1/"
GROUP2_PATH = "/home/pi/love-meter/group2/"
GROUP3_PATH = "/home/pi/love-meter/group3/"
GROUP4_PATH = "/home/pi/love-meter/group4/"
# Assuming servo is connected to servo1 connector.  Change this if using a different port.
METER_SERVO = crickit.servo_1
# Initialize LED connected to neopixel port.
crickit.init_neopixel(2)
LED = crickit.neopixel
# Color definitions
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
OFF = 0
# Time interval that touchpads need to be touched in order to be triggered, in seconds (decimals allowed):
TOUCHPAD_SENSITIVITY = 1.0
# This next one isn't currently used.
# HANDLE_SENSITIVITY = TOUCHPAD_SENSITIVITY
# Input devices
HANDLE = crickit.touch_1
TOUCH2 = crickit.touch_2
TOUCH3 = crickit.touch_3
TOUCH4 = crickit.touch_4
# Time in seconds to delay after the meter is set, until resetting it.
RESET_DELAY = 3
# Time in seconds for meter to go from 0 to love_level.
METER_DURATION = 8

# Global variables
# Start with a random love level from 5 to 8.
# This is the level the meter *will* show when the handle is pulled, 
# it doesn't set the meter's current position.
love_level = randint(5, 8)

# Functions
def play_music(folder):
    """ Play a random mp3 from the given folder. """
    # Get a list of songs in the folder:
    songs = [file for file in listdir(folder) if file.endswith(".mp3")]
    # If there are songs in the folder, choose one at random.  
    if songs:
        chosen_song = choice(songs)
        # TODO: Implement a music player.
        print("Playing music from " + folder)
        print("Playing song " + chosen_song)

def meter_increment(love):
    """ Add one to level, but keep within meter range. """
    return min(love + 1, METER_MAX)

def set_meter(level, duration=0):
    """ 
    Set servo to corresponding meter level, as specified by SERVO_ANGLES. Do so over 
    specified time duration. 
    """
    print("Setting meter to level", level)
    # Check we've received an appropriate level first. If not, do nothing.
    if level in SERVO_ANGLES:
        # Get the corresponding angle for the desired meter level:
        target_angle = SERVO_ANGLES[level]
        # TODO: implement time duration
        METER_SERVO.angle = target_angle

def ready():
    """ Flash green light to indicate ready. """
    for i in range(5):
        LED.fill(GREEN)
        sleep(0.5)
        LED.fill(OFF)
        sleep(0.5)
    print("Ready")

def reset():
    """ Reset meter and LED's. """
    print("Reset:")
    print("LED off.")
    LED.fill(OFF)
    set_meter(METER_MIN)

def is_touched(device):
    """ Check if device is touched for sufficient time. """
    start_time = time()
    # Wait until handle is no longer touched.
    while device.value == True:
        pass
    # Check if elapsed time exceeds sensitivity:
    if time() - start_time > TOUCHPAD_SENSITIVITY:
        return True
    else:
        return False

def measure_love():
    LED.fill(YELLOW)
    set_meter(love_level)
    LED.fill(GREEN)
    sleep(RESET_DELAY)
    reset()

# Main code.
ready()
while True:
    if is_touched(HANDLE):
        measure_love()
    elif is_touched(TOUCH2):
        play_music(GROUP2_PATH)
    elif is_touched(TOUCH3):
        play_music(GROUP3_PATH)
        love_level = meter_increment(love_level)
    elif is_touched(TOUCH4):
        play_music(GROUP4_PATH)
        love_level = METER_MAX
    
