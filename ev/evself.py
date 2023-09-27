from settings.constants import *
from settings.variables import *

import math
import random

# With this function, a planning for the operation (i.e. control actions) can be implemented
def evself(ev, prices, co2, profile):
    # FIXME: This is a placeholder that needs to be implemented

    # result parameter:
    planning = []
    soc = ev.evsoc

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

    # What is already given is to determine if the EV is connected to the charging station (at home) or not (driving)
    intervals_per_day = (3600 / cfg_sim['timebase']) * 24
    intervals_per_hour = (3600 / cfg_sim['timebase'])

    # Other input
    # prices, co2, and profile are vectors (lists) with equal length
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

        if i >= arrival_interval and i < departure_interval:
            # Interval that the EV is connected (available)

            p = (-profile[i]) # take negative house profile as p. Negative values are handled by evsim

            soc_needed = ev.evcapacity - soc
            soc_per_interval = ev.evpmax * cfg_sim['tau']
            intervals_needed = math.ceil(soc_needed/soc_per_interval)
            if intervals_needed > (departure_interval - i) - 4:
                p = ev.evpmax

            soc_next = soc + p*cfg_sim['tau']   # calculate predicted soc after this interval


            if soc_next > ev.evcapacity:        # check for battery capacity
                p = (ev.evcapacity - soc)/cfg_sim['tau']
            
            planning.append(p)

            soc_next = soc + p*cfg_sim['tau']   # calculate soc after interval with corrected p
            soc = soc_next
            pass    

        else:
            # Interval that the EV is disconnected (unavailable)
            planning.append(0)
            pass
    return planning