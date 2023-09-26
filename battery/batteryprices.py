from settings.constants import *
from settings.variables import *

import math
import random

# With this function, a planning for the operation (i.e. control actions) can be implemented
def batteryprices(battery, prices, co2, profile):
    planning = []
    num_of_intervals = len(profile)
    segment_size = 32
    num_of_segments = num_of_intervals // segment_size
    prices_copy = prices.copy()
    while(len(prices_copy) > segment_size):
        prices_segment = prices_copy[:segment_size]
        del prices_copy[:segment_size]
        planning += plan_segment(battery, prices_segment)
    planning += plan_segment(battery, prices_copy)
    
    return planning

def plan_segment(battery, prices):
    segment = [0] * len(prices)

    price_dict = {}
    segment = [0] * len(prices)   # Initialise empty segment
    for i in range(0, len(prices)):
        price_dict[i] = prices[i]
    
    price_dict = sorted(price_dict.items(), key=lambda x:x[1])

    intervals_by_price = []         # List of all intervals, sorted by price from lowest to highest
    for i in price_dict:
        intervals_by_price.append(i[0])

    while(len(intervals_by_price) > 1):
    # calculate soc for each interval
        soc = [battery.batsoc]
        for i in range(0, len(segment)):
            soc.append(soc[i] + (segment[i] * cfg_sim['tau']))
        
        # lowest price is during interval intervals_by_price[0]
        # highest price is during interal intevals_by_price[-1]
        cheap_interval = intervals_by_price.pop(0)
        segment[cheap_interval] = battery.batpmax
        expensive_interval = intervals_by_price.pop(-1)
        segment[expensive_interval] = battery.batpmin

    return segment