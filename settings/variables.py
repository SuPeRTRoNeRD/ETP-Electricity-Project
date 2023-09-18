from groupinfo import *

# Variable settings, these may be modified

# Configuration of the objectives to be simulated by the simulator
# Select optimizations automatically based on the groupinfo.py information provided or not:

# Automatic setup of objectives:
objectives = []

if optimize_greedy:
    objectives.append("optimize_greedy")
if optimize_prices:
    objectives.append("optimize_prices")
if optimize_co2:
    objectives.append("optimize_co2")
if optimize_self:
    objectives.append("optimize_self_consumption")
if optimize_flat:
    objectives.append("optimize_profile_flatness")



# Configure the settings of the households:
cfg_houses = {
    # First house:	# NOTE THE OFF-BY-ONE COUNTING STARTING AT 0!
    0: {	# <- This is the house number
        # PV configuration
        "pvpanels":  0,  # Number of panels, integer
        "pvazimuth": "south",  # Available options: east, southeast, south, southwest, west
        "pvtilt":  30,  # Available options: 10, 15, 20, 25, 30, 35, 40, 45, 50

        # Wind turbine configuration
        "winddiameter": 0,  # Diameter in metres

        # Battery configuration
        "batminsoc":    0,  # Minimum state of charge in kWh
        "batcapacity":  2,  # Capacity in kWh
        "batsoc":       1,  # Initial State of Charge at start of simulation in kWh
        "batpmin":      -2000,  # Minumum power (discharge is negative) in W
        "batpmax":      2000,  # Maximum power in W
    },

    # Second house:	# NOTE THE OFF-BY-ONE COUNTING!
    1: {
        # PV configuration
        "pvpanels":  0,  # Number of panels, integer
        "pvazimuth": "south",  # Available options: east, southeast, south, southwest, west
        "pvtilt":  30,  # Available options: 10, 15, 20, 25, 30, 35, 40, 45, 50

        # Wind turbine configuration
        "winddiameter": 0,  # Diameter in metres

        # Battery configuration
        "batminsoc":    0,  # Minimum state of charge in kWh
        "batcapacity":  2,  # Capacity in kWh
        "batsoc":       1,  # Initial State of Charge at start of simulation in kWh
        "batpmin":      -2000,  # Minumum power (discharge is negative) in W
        "batpmax":      2000,  # Maximum power in W
    },

    # Copy the configuration for how many houses you want to have
    # Note that we have provided 80 houses (so maximum number is house index 79) in the dataset
    # Any house number can be chosen between 0 .. 79 to start with.
    # E.g. the following as next config is perfectly fine (uncomment):

    # Another house:
    # 23: {
        # # PV configuration
        # "pvpanels":  1,  # Number of panels, integer
        # "pvazimuth": "south",  # Available options: east, southeast, south, southwest, west
        # "pvtilt":  30,  # Available options: 10, 15, 20, 25, 30, 35, 40, 45, 50

        # # Wind turbine configuration
        # "winddiameter": 1,  # Diameter in metres

        # # Battery configuration
        # "batminsoc":	0,  # Minimum state of charge in kWh
        # "batcapacity":  4,  # Capacity in kWh
        # "batsoc":       0,  # Initial State of Charge at start of simulation in kWh
        # "batpmin":      -3000,  # Minumum power (discharge is negative) in W
        # "batpmax":      3000,  # Maximum power in W
    # },
}

# It is important to note that we will select random houses too to test your implementation with.
# So if you want to be sure you cover all cases, you could also run the code with all 80 households.
# For this, you can uncomment the following code:

# cfg_houses = {}
# for i in range(0, 80):
    # # Make a config for each house number i (see the for loop iterator)

    # # To do so, we make a new dictionary (called h) witht he config for a house
    # h = {
        # # PV configuration
        # "pvpanels":  1,  # Number of panels, integer
        # "pvazimuth": "south",  # Available options: east, southeast, south, southwest, west
        # "pvtilt":  30,  # Available options: 10, 15, 20, 25, 30, 35, 40, 45, 50

        # # Wind turbine configuration
        # "winddiameter": 1,  # Diameter in metres

        # # Battery configuration
        # "batminsoc":    0,  # Minimum state of charge in kWh
        # "batcapacity":  4,  # Capacity in kWh
        # "batsoc":       0,  # Initial State of Charge at start of simulation in kWh
        # "batpmin":      -3000,  # Minumum power (discharge is negative) in W
        # "batpmax":      3000,  # Maximum power in W
    # }

    # # We add now h to our dictionary with house configs
    # cfg_houses[i] = h

    # # Note that on the next iteration the h "memory" is overwritten, this is a programming trick.