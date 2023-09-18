from settings.constants import *
from settings.variables import *

import math
import random

# With this function, a planning for the operation (i.e. control actions) can be implemented
def batterygreedy(battery, prices, co2, profile):
    # result parameter:
    planning = []

    # Battery parameters can be obtained as follows
    # battery.batsoc        # State of Charge in kWh
    # battery.batminsoc     # Minimum State of Charge
    # battery.batcapacity   # Capacity of the battery in kWh
    # battery.batpmin       # Maximum power in W
    # battery.batpmax       # Minimum power in W

    # Other input
    # prices, co2, and profile are vectors (lists) with equal length

    for i in range(0, len(profile)):
        planning.append(-profile[i])


    # Finally, the resulting planning for the device must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input vectprs (i.e., prices, co2 and profile)

    # For each interval i, these can be set by adding the correction value to the planning list, i.e.:
    # planning.append(<your_value>)
    return planning