from settings.constants import *
from settings.variables import *

import math
import random

# This function simulates the behaviour of the device
def batterysim(battery, planning):
    # result parameter to be filled:
    profile = []
    soc = battery.batsoc
    for p in planning:
        if p < battery.batpmin:
            p = battery.batpmin
        if p > battery.batpmax:
            p = battery.batpmax
        soc_next = soc + p*cfg_sim['tau']
        if soc_next < battery.batminsoc:
            p = (battery.batminsoc - soc)/cfg_sim['tau']
            soc_next = battery.batminsoc
        elif soc_next > battery.batcapacity:
            p = (battery.batcapacity - soc)/cfg_sim['tau']
            soc_next = battery.batcapacity
        soc = soc_next
        profile.append(p)

    # NOTE: The following parameters are best used READ-ONLY!
    # Battery parameters can be obtained as follows
    # battery.batsoc        # State of Charge in kWh
    # battery.batminsoc     # Minimum State of Charge
    # battery.batcapacity   # Capacity of the battery in kWh
    # battery.batpmin       # Maximum power in W
    # battery.batpmax       # Minimum power in W

    # Other input
    # planning, which is the planning created for the device with desired control (power) actions
    # You should use this planning as input for the simulation of the device
    # Adapt the values of the planning in case the device is not able to comply with the control command
    # Make sure the profile variable is populated and has the same length as the planning input

    # Running the simulation of the device

    # Here you will need to implement your simulation code
    # Create the resulting by filling the profile list
    # This can be done by e.g. profile.append(value)

    # Finally, the resulting power profile for the device must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input planning list

    # You can loop through the planning that is provided using e.g.,
    # for i in range(0, len(planning)):
    # Note that this for-statement would essentially step through the profile as if it were a discrete time simulation

    # Also, you could print(planning) to see what it looks like.

    # For each interval i, these can be set by adding the correction value to the profile list, i.e.:
    # profile.append(<your_value>)


    return profile