# Adapted from
# https://github.com/adafruit/Adafruit_CircuitPython_Crickit/blob/master/examples/crickit_neopixel_simpletest.py
# Crickit library demo - NeoPixel terminal
# Note: On CPX Crickit, NeoPixel pin is normally connected to A1, not to seesaw,
# so this demo would not control the NeoPixel terminal.
# On the Crickit FeatherWing, the NeoPixel terminal is controlled by seesaw.

# pylint can't figure out "np" can be indexed.
# pylint: disable=unsupported-assignment-operation

import time
from adafruit_crickit import crickit

# Strip or ring of 2 NeoPixels
crickit.init_neopixel(2)

crickit.neopixel.fill(0)

# Assign to a variable to get a short name and to save time.
np = crickit.neopixel

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Show a sequence of red, green, blue.
np.fill(0)
time.sleep(1)
np.fill(RED)
time.sleep(1)
np.fill(0)
time.sleep(1)
np.fill(GREEN)
time.sleep(1)
np.fill(0)
time.sleep(1)
np.fill(BLUE)
time.sleep(1)
np.fill(0)
