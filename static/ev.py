from settings.constants import *
from settings.variables import *
from helpers.helpers import *

# external classes
from ev.evsim import *
from ev.evgreedy import *
from ev.evprices import *
from ev.evco2 import *
from ev.evself import *
from ev.evflat import *


class EV():
    def __init__(self, house):
        self.name = "Electricvehicle"
        self.house = house
        self.number = self.house.housenumber
        self.type = "load"

        # Placeholder, will be loaded upon initialize()
        self.evsoc = 0
        self.evcapacity = 40
        self.evpmin = 0
        self.evpmax = 11000

        # Static Charging session duration
        self.evenergy = 5 + (self.number % 5)  # Energy demand in kWh per driving session
        self.evminsoc = self.evcapacity  # Minimum SoC to reach after each session (because of driving)
        self.evconnectiontime = self.evenergy + 2  # Hours the EV is connected
        self.evarrivalhour = 12 + (self.number % 7)  # Hour of arrival of the EV each day

        self.initialize()

        # Planning/control variable
        self.planning = []  # This list contains the control actions required

    # Simulation code
    def execute(self, objective, prices, co2, profile):
        # initialize the device
        self.initialize()

        # pre validation
        if not self.verify_input():
            print("The input parameters for device " + str(self.name) + " of house "+str(self.number) +" are invalid! Aborting! Most likely you have not added (enough) values to the profile list using profile.append(<value>).")
            exit()

        # Perform the optimization
        planning = self.optimize(objective, prices, co2, profile)
        if not self.verify_planning(planning):
            print("The optimization algorithm for device " + str(self.name) + " yields invalid results! Aborting! Most likely you have not added (enough) values to the planninglist using planning.append(<value>).")
            exit()

        # Perform the simulation
        returnprofile = self.simulate(planning)
        if not self.verify_result(returnprofile):
            print("The simulation of device " + str(self.name) + " failed! Aborting! Most likely you are violating our constraints. Carefully read the error log above and the comments in the code that caused the crash.")
            exit()

        self.profile = returnprofile
        return self.profile

    # Function to initialize the results
    def initialize(self, resetLists=True):
        if resetLists:
            # initialize with empty profile
            self.profile = [0] * cfg_sim['intervals']
            self.planning = [0] * cfg_sim['intervals']

        # ev settings
        try:
            self.evcapacity = 40    # cfg_houses[self.number]["evcapacity"]
            self.evpmax = 11000     # cfg_houses[self.number]["evpmax"]

            # Static parameters
            self.evsoc = self.evcapacity
            self.evpmin = 0

            # Static Charging session duration
            self.evenergy = 5+(self.number%5)			# Energy demand in kWh per driving session
            self.evminsoc =	self.evenergy 				# Minimum SoC to reach after each session (because of driving)
            self.evconnectiontime = self.evenergy + 2 	# Hours the EV is connected
            self.evarrivalhour = 12+(self.number%7)		# Hour of arrival of the EV each day
        except:
            print("Input for ev " + str(self.number) + " is invalid!")
            exit()

    # Optimization code
    def optimize(self, objective, prices, co2, profile):
        self.initialize(False)
        planning = [0] * cfg_sim['intervals']

        if objective == "optimize_greedy":
            return evgreedy(self, prices, co2, profile)

        elif objective == "optimize_prices":
            # Perform price optimization
            return evprices(self, prices, co2, profile)

        elif objective == "optimize_co2":
            # Perform CO2 emissions reduction
            return evco2(self, prices, co2, profile)

        elif objective == "optimize_self_consumption":
            # Perform self-consumption optimization
            return evself(self, prices, co2, profile)

        elif objective == "optimize_profile_flatness":
            # Optimize the device power profile towards a flat profile using the Euclidean distance vector norm (2-norm)
            return evflat(self, prices, co2, profile)

        else:
            # Default fallback
            return planning

    # Simulation code
    def simulate(self, planning=[]):
        self.initialize(False)
        return evsim(self, planning)

    # Function to verify the created planning by the optimization code
    # But also to verify user input, is it valid input?
    def verify_input(self):
        assert (self.evcapacity >= 0)	# The EV capacity must be positive
        assert (self.evminsoc >= 0)		# The minumum EV SoC must be positive
        assert (self.evsoc >= 0)		# The EV SoC must be positive
        assert (self.evsoc <= self.evcapacity)		# The EV SoC may not exceed the capacity
        assert (self.evminsoc <= self.evcapacity)	# The minimum EV SoC may not exceed the capacity
        assert (self.evpmin <= self.evpmax)			# The minimum power must be lower than the maximum power
        return True

    def verify_planning(self, planning):
        self.initialize(False)
        assert (len(self.planning) == cfg_sim['intervals'])	# The planning list must be as long as the number of simulation time intervals
        return True

    # Function to verify if the code functions correctly
    def verify_result(self, profile):
        # Internal conversion to Wtau
        self.initialize(False)
        assert (len(self.profile) == cfg_sim['intervals'])	# The power profile list must be as long as the number of simulation time intervals

        capacity = 1000 * (3600 / cfg_sim['timebase']) * self.evcapacity
        soc = 1000 * (3600 / cfg_sim['timebase']) * self.evsoc
        minsoc = 1000 * (3600 / cfg_sim['timebase']) * self.evminsoc

        intervals_per_day = (3600 / cfg_sim['timebase']) * 24
        intervals_per_hour = (3600 / cfg_sim['timebase'])

        for i in range(0, len(profile)):
            # check availability:
            arrival_day = math.floor(i / intervals_per_day)
            arrival_interval = int(arrival_day * intervals_per_day + self.evarrivalhour * intervals_per_hour)
            departure_interval = int(arrival_interval + self.evconnectiontime * intervals_per_hour)

            # Check for overruns:
            if self.evarrivalhour + self.evconnectiontime >= 24:
                if departure_interval - (24 * (3600 / cfg_sim['timebase'])) > i and arrival_interval - (
                        24 * (3600 / cfg_sim['timebase'])) > 0:
                    departure_interval -= int(24 * (3600 / cfg_sim['timebase']))
                    arrival_interval -= int(24 * (3600 / cfg_sim['timebase']))

            value = profile[i]

            # Reduce SOC upon arrival
            if i == arrival_interval:
                soc -= self.evenergy * 1000 * (3600 / cfg_sim['timebase'])
                assert(soc >= -0.001)	# The EV SoC must be always positive. Your simulation code resulted in a negative SoC. Are you charging enough power?

            # Ensure the SoC is full upon departure
            if i == departure_interval:
                assert(soc >= capacity-0.001)	# The EV must be fully charged upon departure. Are you charging enough power?

            if i >= arrival_interval and i < departure_interval:
                # The EV is connecteds
                assert (value >= self.evpmin)	# At any given time, you need to keep the power draw at at least the minimum power
                assert (value <= self.evpmax)	# At any given time, you need to keep the power draw at at most the maximum power

            else:
                assert(value == 0)				# If the EV is gone you cannot charge it! Apparently you try to charge it.

            soc += value
            assert (soc >= -0.001)				# The EV SoC must stay above 0. Are you charging enough?
            assert (soc <= capacity+0.001)		# THe EV SoC must stay below the SoC. Are you charging too much?

        return True

