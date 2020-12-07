#!/usr/bin/env python3

# DS1820 and DS18S20 have the Family Code 10
# DS18B20 has Code 28 
# DS1822 the 22.
# Don't know will this work with 'B' or x22 -sensors
#./sys/bus/w1/devices/10-000800aac8dc/w1_slave

import os

# Remove first comma from path if using with real sensors
dir_w1_bus = "./sys/bus/w1/devices/"

def scan_sensors():
	global temp_sensors
	temp_sensors = []
	try:
		temp_sensors = os.listdir(dir_w1_bus)
	except Exception as e:
		raise
	else:
		# Pick only valid sensor-folders
		temp_sensors = [i for i in temp_sensors if i.startswith("10-")]
		if temp_sensors == []: raise FileNotFoundError
	print("from: scan_sensors()", temp_sensors) # Only for develope purpose, delete after release

scan_sensors()

