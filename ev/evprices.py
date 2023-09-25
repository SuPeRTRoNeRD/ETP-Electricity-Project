from settings.constants import *
from settings.variables import *

import math
import random

# With this function, a planning for the operation (i.e. control actions) can be implemented
def evprices(ev, prices, co2, profile):
    # FIXME: This is a placeholder that needs to be implemented

    # result parameter:
    planning = [0] * len(profile)
    soc = ev.evsoc

    available_intervals = {}

    for i in prices:
        pass
        
        # What is already given is to determine if the EV is connected to the charging station (at home) or not (driving)
    intervals_per_day = (3600 / cfg_sim['timebase']) * 24
    intervals_per_hour = (3600 / cfg_sim['timebase'])

    # Looping through the provided planning vector
    for i in range(0, len(profile)):
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


        if i == arrival_interval:
            soc = soc - ev.evenergy
            for j in range(i, departure_interval):
                available_intervals[j] = prices[j]

            intervals_until_departure = departure_interval - i
            available_intervals = sorted(available_intervals.items(), key=lambda x:x[1])
            soc_needed = ev.evcapacity - soc
            soc_per_interval = ev.evpmax * cfg_sim['tau']
            intervals_needed = math.ceil(soc_needed/soc_per_interval)

            for i in range(0, intervals_needed):
                interval = available_intervals[i]
                planning[interval[0]] = ev.evpmax
            pass

            # Moment at which the EV arrives

        if i >= arrival_interval and i < departure_interval:
            # Interval that the EV is connected (available)
            pass

        else:
            # Interval that the EV is disconnected (unavailable)
            pass

        if i == departure_interval: #(this statement is unreachable)
            # Moment at which the EV departs
            available_intervals = {}
            pass
    

        # print(planning[interval[0]])

    # print(planning)
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
    # for i in range(0, len(profile)):
    #     planning.append(ev.evpmax)

    # Finally, the resulting planning for the device must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input vectors (i.e., prices, co2 and profile)

    # For each interval i, these can be set by adding the correction value to the planning list, i.e.:
    # planning.append(<your_value>)
    return planning