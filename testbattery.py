from settings.constants import *
from settings.variables import *
from helpers.helpers import *

# external classes
from battery.batterysim import *

import math
import random

# Test cases
pmax   = [ 1000,  1000,  1000,  1000,  100,    0,    0,  300,  100000]
pmin   = [-1000, -1000, -1000, -1000, -1000,    0, -100,    0, -100000]
bcap   = [    3,     3,     0,     3,    3,    3,    3,  0.5,     100]
soc    = [    0,   1.5,     0,     1,    0,    0,    2,  0.5,       0]
minsoc = [    0,     1,     0,     1,    0,    0,    2,  0.1,       0]


class Battery():
    def __init__(self, pmax, pmin, bcap, soc, minsoc):
        self.batsoc = soc
        self.batminsoc = minsoc
        self.batcapacity = bcap
        self.batpmin = pmin
        self.batpmax = pmax

        print('------------------------------------------------------------------------------')
        print('-  Battery parameters: pmin='+str(pmin)+', pmax='+str(pmax)+', soc='+str(soc)+', minsoc='+str(minsoc)+', capacity='+str(bcap))
        print('------------------------------------------------------------------------------')

  
        # Run all test cases
        # Test constant charging
        print('Testing constant charging')
        for p in [10,1000,2000,4000,8000,20000]:
            planning = [p] * 100
            self.execute(planning)

        # Test constant discharging
        print('Testing constant discharging')
        for p in [10,1000,2000,4000,8000,20000]:
            planning = [-p]*100
            self.execute(planning)

        # Charge and discharge cycles
        print('Testing periodic charging/discharging')
        for T in range(1,10):
            planning = []
            for i in range(0, cfg_sim['intervals'] ):
                planning.append(T*1000*math.sin(((i*T)/cfg_sim['intervals'])*2*math.pi))
            self.execute(planning)

        # Random charging
        print('Testing random profile; independent')
        for n in range(0, 20):
            planning = []
            for i in range(0, 1000):
                planning.append(1000 * random.random())
            self.execute(planning)

        # Random charging (with memory)
        print('Testing random profile; dependent')
        for n in range(0, 20):
            planning = []
            s = 0
            for i in range(0, 1000):
                planning.append(s + (100 * random.random()))
                s = planning[-1]
            self.execute(planning)


    # Simulation code
    def execute(self, planning):
        # pre validation
        if not self.verify_input():
            print("The input parameters for device are invalid! Aborting! Most likely you have not added (enough) values to the profile list using profile.append(<value>).")
            exit()

        # Perform the simulation
        returnprofile = self.simulate(planning)
        if not self.verify_result(returnprofile, planning):
            print("The simulation of device failed! Aborting! Most likely you are violating our constraints. Carefully read the error log above and the comments in the code that caused the crash.")
            exit()


    # Simulation code
    def simulate(self, planning=[]):
        return batterysim(self, planning)

    # Function to verify the created planning by the optimization code
    # But also to verify user input, is it valid input?
    def verify_input(self):
        assert (self.batcapacity >= 0)
        assert (self.batminsoc >= 0)
        assert (self.batsoc >= 0)
        assert (self.batsoc <= self.batcapacity)
        assert (self.batminsoc <= self.batcapacity)
        assert (self.batpmin <= self.batpmax)

        return True


    # Function to verify if the code functions correctly
    def verify_result(self, profile, planning):
        # Internal conversion to Wtau
        capacity = 1000 * (3600 / cfg_sim['timebase']) * self.batcapacity
        soc = 1000 * (3600 / cfg_sim['timebase']) * self.batsoc
        minsoc = 1000 * (3600 / cfg_sim['timebase']) * self.batminsoc

        assert (len(profile) == len(planning))
        for value in profile:
            assert (value >= self.batpmin)	# The power drawn must be at least the minimum power (maximal discharging)
            assert (value <= self.batpmax)	# The power drawn must be at most the maximum power (maximal charging)

            # determine if the SoC at the end of the interval will be in bounds
            soc += value

            assert (soc >= minsoc - 0.1)	# The SoC must remain positive. Are you discharging too much?
            assert (soc <= capacity + 0.1)	# The SoC cannot be higher than the capacity. Are you charging too much?
        return True




# Run all cases
for i in range(0, len(pmax)):
    b = Battery(pmax[i], pmin[i], bcap[i], soc[i], minsoc[i])

print('------------------------------------------------------------------------------')
print('-- Battery test finished; no problems found                                 --')
print('------------------------------------------------------------------------------')
