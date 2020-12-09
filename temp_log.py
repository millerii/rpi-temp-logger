#!/usr/bin/env python3

# DS1820 and DS18S20 have the Family Code 10
# DS18B20 has Code 28 
# DS1822 the 22.
# Don't know will this work with 'B' or x22 -sensors

import os
import sys


# Remove first comma from path if using with real sensors
dir_w1_bus = "./sys/bus/w1/devices/"

def scan_sensors():
	temp_sensors = []

	try:
		temp_sensors = os.listdir(dir_w1_bus)
	except Exception as e:
		print("*** Temperature sensor not found, check sensor connection or One-Wire settings. ***")
		raise SystemExit(e)
	else:
		# Pick only valid sensor-folders, folder starts with correct family code
		temp_sensors = [i for i in temp_sensors if i.startswith("10-")]
		if temp_sensors == []:
			raise FileNotFoundError
	
	return temp_sensors # List of temp-sensors id's
	print("from: scan_sensors()", temp_sensors) # Only for development purpose, delete after release


def read_sensors(temp_sensors):
	# Take list of temp-sensors id's as argument
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
			value = round(temp, 1)
			temperatures[key] = value 
		else:
			temp = ""
		
		print("from: read_sensors()", check_crc, sensor, temp) # Only for development purpose, delete after release
	
	return temperatures # Dictionary of sensor-id combined with temperature


launch_argv = []
launch_argv = sys.argv

if "-show" in launch_argv:
	temps = read_sensors(scan_sensors())
	for addres, temp in temps.items():
		print(addres + ":", str(temp) + "\N{DEGREE SIGN}C")
	sys.exit()

print("from: main prog", read_sensors(scan_sensors())) # Only for development purpose, delete after release
