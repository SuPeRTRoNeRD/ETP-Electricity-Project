from settings.constants import *
from settings.variables import *

import math
import random

# This function simulates the behaviour of the device
def evsim(ev, planning):
    # result parameter:
    profile = []

    # NOTE: The following parameters are best used READ-ONLY!
    # ev parameters can be obtained as follows
    # ev.evsoc              # State of Charge of the EV in kWh
    # ev.evminsoc           # Minimum State of Charge of the EV in kWh
    # ev.evcapacity         # Capacity of the EV in kWh
    # ev.evpmin             # Minimum power of the EV in W
    # ev.evpmax             # Maximum power of the EV in W
    # ev.evenergy           # Energy consumption of the EV over one driving session

    # NOTE: The following parameters are best used READ-ONLY!
    # Timing variables:
    # ev.evminsoc  	        # Minimum SoC to reach after each session (because of driving)
    # ev.evconnectiontime   # Hours the EV is connected
    # ev.evarrivalhour      # Hour of arrival of the EV each day

    # NOTE: The EV needs to be fully charged (i.e., reach maximum SoC) when departing

    # Other input
    # planning, which is the planning created for the device with desired control (power) actions
    # You should use this planning as input for the simulation of the device
    # Adapt the values of the planning in case the device is not able to comply with the control command
    # Make sure the profile variable is populated and has the same length as the planning input

    # Running the simulation of the device

    # What is already given is to determine if the EV is connected to the charging station (at home) or not (driving)
    intervals_per_day = (3600 / cfg_sim['timebase']) * 24
    intervals_per_hour = (3600 / cfg_sim['timebase'])

    # Looping through the provided planning vector
    for i in range(0, len(planning)):
        # Note that this for-statement would essentially step through the profile as if it were a discrete time simulation
        # check availability:
        arrival_day = math.floor(i/intervals_per_day)
        arrival_interval = int(arrival_day*intervals_per_day + ev.evarrivalhour * intervals_per_hour)
        departure_interval = int(arrival_interval + ev.evconnectiontime * intervals_per_hour)

        # Check for overruns:
        if ev.evarrivalhour+ev.evconnectiontime >= 24:
            if departure_interval - (24 * (3600 / cfg_sim['timebase'])) > i and arrival_interval - (24 * (3600 / cfg_sim['timebase'])) > 0:
                departure_interval -= int(24 * (3600 / cfg_sim['timebase']))
                arrival_interval -= int(24 * (3600 / cfg_sim['timebase']))

        # FIXME Here you will need to implement the behaviour of the electric vehicle
        # You do not necessarily need to use all if-constructs, but htey are defined for your confenience if you wish to make use of them
        # Keep the "pass" if you do not want to use one of the if-constructs.
        if i == arrival_interval:
            # Moment at which the EV arrives
            pass

        if i >= arrival_interval and i < departure_interval:
            # Interval that the EV is connected (available)
            pass

        else:
            # Interval that the EV is disconnected (unavailable)
            pass

        if i == departure_interval:
            # Moment at which the EV departs
            pass

    # Finally, the resulting power profile for the device must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input planning list

    # For each interval i, these can be set by adding the correction value to the profile list, i.e.:
    # profile.append(<your_value>)

    return profile
