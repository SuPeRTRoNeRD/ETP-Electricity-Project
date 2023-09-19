# Constant variables used for the simulation
# DO NOT CHANGE THIS FILE!

cfg_sim = {}

# General settings
cfg_sim['timebase'] 		= 900 	# Interval length in seconds
cfg_sim['intervals'] 		= 7*96 	# Discrete time intervals to simulate
cfg_sim['startInterval'] 	= 0 	# Discrete time interval to start the simulation

# Definition of Tau
cfg_sim['ivperhour']            = 3600 / cfg_sim['timebase']  # Intervals per hour
cfg_sim['tau'] = 1 / (1000*cfg_sim['ivperhour'])  # Conversion factor: Watts for one interval -> kWh for that interval

# Result folder
cfg_sim['outputfile']       = "output/results.csv"
cfg_sim['overviewfile']     = "output/overview.csv"

# Device and house specific limits
cfg_sim['bat_maxcrate']     = 1     # Maximum c-rate allowed for battery
cfg_sim['bat_maxcapacity']  = 0.5   # Maximum capacity as ratio of the average daily electricity demand
cfg_sim['wind_maxdiameter'] = 5     # Maximum wind turbine diameter
cfg_sim['res_coverage']     = 2     # Maximum ratio of supply/demand of res (pv and wind)
