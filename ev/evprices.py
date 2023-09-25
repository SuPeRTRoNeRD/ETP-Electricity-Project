from settings.constants import *
from settings.variables import *

import math
import random

# With this function, a planning for the operation (i.e. control actions) can be implemented
def evprices(ev, prices, co2, profile):
    # FIXME: This is a placeholder that needs to be implemented

    # result parameter:
    planning = [0] * len(profile) # initialise as empty list
    soc = ev.evsoc

    available_intervals = {} # define as dictionary

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
            # Moment at which the EV arrives
            soc = soc - ev.evenergy
            for j in range(i, departure_interval):
                available_intervals[j] = prices[j]

            available_intervals = sorted(available_intervals.items(), key=lambda x:x[1])
            soc_needed = ev.evcapacity - soc
            soc_per_interval = ev.evpmax * cfg_sim['tau']
            intervals_needed = math.ceil(soc_needed/soc_per_interval)

            for i in range(0, intervals_needed):
                interval = available_intervals[i]
                planning[interval[0]] = ev.evpmax
            pass

        if i == departure_interval: #(this statement is unreachable)
            # Moment at which the EV departs
            available_intervals = {}
            pass
    

        # print(planning[interval[0]])

    return planning