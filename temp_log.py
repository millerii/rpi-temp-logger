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
	print("from: scan_sensors()", temp_sensors) # Only for development purpose, delete after release

def read_sensors():
	global temperatures
	temperatures = {}

	for sensor in temp_sensors:
		try_count = 0
		check_crc = "NO"
		temp = ""

		try:
			with open(dir_w1_bus + sensor + "/w1_slave", "r") as file:
				while check_crc == "NO" and try_count <= 2:
					temp = file.read()
					# Parse crc-check, last word in line (YES/NO)
					check_crc = temp.split("\n")[0].rsplit(" ",1)[-1]
					try_count += 1
		except Exception as e:
			print(e)

		if check_crc == "YES":
			# Parse temperature, last word in line followed by 't='
			temp = temp.split("\n")[1].rsplit('t=',1)[-1]
			temp = float(temp) / 1000
			key = sensor
			value = temp
			temperatures[key] = value 

		else:
			temp = ""
		print("from: read_sensors()", check_crc, sensor, temp) # Only for development purpose, delete after release

scan_sensors()
read_sensors()
print("from: main prog",temperatures) # Only for development purpose, delete after release
