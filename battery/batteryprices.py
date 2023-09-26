from settings.constants import *
from settings.variables import *

import math
import random

# With this function, a planning for the operation (i.e. control actions) can be implemented
def batteryprices(battery, prices, co2, profile):
    
    # result parameter:
    price_dict = {}
    planning = [0] * len(profile)   # Initialise empty planning
    for i in range(0, len(prices)):
        price_dict[i] = prices[i]
    
    price_dict = sorted(price_dict.items(), key=lambda x:x[1])

    intervals_by_price = []         # List of all intervals, sorted by price from lowest to highest
    for i in price_dict:
        intervals_by_price.append(i[0])

    # Battery parameters can be obtained as follows
    # battery.batsoc        # State of Charge in kWh
    # battery.batminsoc     # Minimum State of Charge
    # battery.batcapacity   # Capacity of the battery in kWh
    # battery.batpmin       # Minimum power in W (Negative value)
    # battery.batpmax       # Maximum power in W

    # Other input
    # prices, co2, and profile are vectors (lists) with equal length

    # intervals_by_price = '1'
    while(len(intervals_by_price) > 1):
        # calculate soc for each interval
        soc = [battery.batsoc]
        for i in range(0, len(planning)):
            soc.append(soc[i] + (planning[i] * cfg_sim['tau']))
        
        # lowest price is during interval intervals_by_price[0]
        # highest price is during interal intevals_by_price[-1]
        cheap_interval = intervals_by_price.pop(0)
        planning[cheap_interval] = confine_p(battery.batpmax, battery, soc[cheap_interval])
        expensive_interval = intervals_by_price.pop(-1)
        planning[expensive_interval] = confine_p(battery.batpmin, battery, soc[expensive_interval])


    return planning

def confine_p(p_desired, battery, soc): # Make sure p is within battery limits (both p and soc)
    p = p_desired
    if p < battery.batpmin:
        p = battery.batpmin
    elif p > battery.batpmax:
        p = battery.batpmax
    
    soc_next = soc + p * cfg_sim['tau']
    if soc_next < battery.batminsoc:
        p = (battery.batminsoc - soc)/cfg_sim['tau']
        soc_next = battery.batminsoc
    elif soc_next > battery.batcapacity:
        p = (battery.batcapacity - soc)/cfg_sim['tau']
        soc_next = battery.batcapacity

    return p