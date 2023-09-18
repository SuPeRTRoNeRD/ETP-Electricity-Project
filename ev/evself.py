from settings.constants import *
from settings.variables import *

import math
import random

# With this function, a planning for the operation (i.e. control actions) can be implemented
def evself(ev, prices, co2, profile):
    # FIXME: This is a placeholder that needs to be implemented

    # result parameter:
    planning = []

    # NOTE: The following parameters are best used READ-ONLY!
    # ev parameters can be obtained as follows
    # ev.evsoc              # State of Charge of the EV in kWh
    # ev.evminsoc           # Minimum State of Charge of the EV in kWh
    # ev.evcapacity         # Capacity of the EV in kWh
    # ev.evpmin             # Minimum power of the EV in W
    # ev.evpmax             # Maximum power of the EV in W

    # NOTE: The following parameters are best used READ-ONLY!
    # Timing variables:
    # ev.evminsoc  	        # Minimum SoC to reach after each session (because of driving)
    # ev.evconnectiontime   # Hours the EV is connected
    # ev.evarrivalhour      # Hour of arrival of the EV each day

    # NOTE: The EV needs to be fully charged (i.e., reach maximum SoC) when departing

    # Other input
    # prices, co2, and profile are vectors (lists) with equal length

    # Fallback implementation: Greedy:
    for i in range(0, len(profile)):
        planning.append(ev.evpmax)

    # Finally, the resulting planning for the device must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input vectors (i.e., prices, co2 and profile)

    # For each interval i, these can be set by adding the correction value to the planning list, i.e.:
    # planning.append(<your_value>)
    return planning