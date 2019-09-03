# Imports
from adafruit_crickit import crickit
from random import choice, randint
from time import time, sleep
from os import listdir
import pygame

# Global constants
# Range of meter
METER_MIN = 0
METER_MAX = 9
# This is the max love you can get, by pushing touchpad 4:
LOVE_MAX = 9
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
LED.fill(0)
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
# Number of intervals to use for animation of meter.  More intervals = smoother animation.
ANIMATION_INTERVALS = 1000
# Initialize the pygame mixer.
pygame.mixer.init()
PLAYER = pygame.mixer.music

# Global variables
# Range for the random love level.
love_level_min = 5
love_level_max = 8

# Functions
def random_love_level():
    """ Choose a random level within the set range.  """
    return randint(love_level_min, love_level_max)

def play_music(folder):
    """ Play a random mp3 from the given folder. """
    # Get a list of songs in the folder:
    songs = [file for file in listdir(folder) if file.endswith(".mp3")]
    # If there are songs in the folder, choose one at random.  
    if songs:
        chosen_song = choice(songs)
        print("Playing " + folder + chosen_song)
        # Load and play the song
        PLAYER.load(folder + chosen_song)
        # Pygame mixer will play in a background thread, 
        # which means program execution will continue while music
        # is playing.
        PLAYER.play()
    else:
        print("No mp3's found in " + folder)

def meter_increment(love):
    """ Add one to level, but keep within meter range. """
    return min(love + 1, METER_MAX)

def set_meter(level, duration=0):
    """ 
    Set servo to corresponding meter level, as specified by SERVO_ANGLES. Do so over 
    specified time duration. Assume meter starts at minimum.
    """
    print("Setting meter to level", level)
    # Check we've received an appropriate level first. If not, do nothing.
    if level in SERVO_ANGLES:
        # Get the corresponding angle for the desired meter level:
        target_angle = SERVO_ANGLES[level]
        current_angle = SERVO_ANGLES[METER_MIN]
        # Chop the animation into intervals:
        time_increment = duration / ANIMATION_INTERVALS
        angle_increment = (target_angle - current_angle) / ANIMATION_INTERVALS
        # Animate a little bit at each interval:
        for x in range(ANIMATION_INTERVALS):
            METER_SERVO.angle = current_angle + (x + 1) * angle_increment
            sleep(time_increment)

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
    """ Check if device is touched. """
    return device.value

def measure_love():
    """ Activate the love meter. """
    LED.fill(YELLOW)
    play_music(GROUP1_PATH)
    set_meter(love_level, METER_DURATION)
    LED.fill(GREEN)
    sleep(RESET_DELAY)
    reset()
    # If user is still touching handle, wait until they let go:
    while HANDLE.value:
        pass

# Main code.
# Signal we're ready.  This is useful when auto-running, because bootup can take a while.
ready()
# Set a random love level.
love_level = random_love_level()
# A 'bonus' is any of the touchpads 2 through 4.  If these haven't been touched,
# we'll generate a new random love level. 
bonus_touched = False
# TODO(?): avoid handle-pad-handle-pad-handle
while True:
    if is_touched(HANDLE):
        if not bonus_touched:
            love_level = random_love_level()
        measure_love()
        bonus_touched = False
    elif is_touched(TOUCH2):
        # Avoid flutter and avoid registering multiple touchpads in a row: 
        if not bonus_touched:
            bonus_touched = True
            play_music(GROUP2_PATH)
    elif is_touched(TOUCH3):
        if not bonus_touched:
            bonus_touched = True
            play_music(GROUP3_PATH)
            love_level = meter_increment(love_level)
    elif is_touched(TOUCH4):
        if not bonus_touched:
            bonus_touched = True
            love_level = LOVE_MAX
            play_music(GROUP4_PATH)
            