#!/usr/bin/env python3

# DS1820 and DS18S20 have the Family Code 10
# DS18B20 has Code 28 
# DS1822 the 22.
# Don't know will this work with 'B' or x22 -sensors

import os
import sys
import openpyxl
import datetime


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

def read_sensors(temp_sensors):	# Take list of temp-sensors id's as argument
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
			# Save sensor-id and temp to dictionary
			key = sensor
			value = round(temp, 1)
			temperatures[key] = value 
		else:
			temp = ""

	return temperatures # Dictionary of sensor-id combined with temperature

def show_temp():
	temps = read_sensors(scan_sensors())
	for addres, temp in temps.items():
		print(addres + ":", str(temp) + "\N{DEGREE SIGN}C")

def excel_save():
	def add_temp_excel(ws_data, column_for_id, last_row, temp_for_id):
		ws_data["A" + last_row] = date_now
		ws_data["A" + last_row].number_format = 'dd.mm.yyyy h:mm'
		ws_data[column_for_id + last_row] = temp_for_id

	date_now = datetime.datetime.now()
	temps = read_sensors(scan_sensors())

	# Create initial excel file, if not exist
	excel_file = "temp_history.xlsx"
	if not os.path.isfile(excel_file):
		wb = openpyxl.Workbook() # One time excel-file initializing
		ws_data = wb.active
		ws_data.title = "data"
		ws_data['A1'] = "Date-Time"
		
		try:
			wb.save(excel_file)
		except Exception as e:
			print(e)

	# Load excel-workbook and save new data
	try:
		wb = openpyxl.load_workbook(excel_file)
	except Exception as e:
		print(e)
	else:
		ws_data = wb["data"]
		
		# Read excel headers for sensor-id -name compare
		row_headers = []
		for col in ws_data['1']:
			row_headers.append(col.value)

		last_row = str(ws_data.max_row + 1) # Find last row from data-worksheet

		for id in temps:
			if id in row_headers:
				column_for_id = str(chr(row_headers.index(id) + 97)) # Convert row 'number' [row_headers.index(id)] to letter [id:0 + ascii:97 = A]
				# Add new temp for sensor-id row
				add_temp_excel(ws_data, column_for_id, last_row, temps[id])
			else:
				# Add new sensor-id and save temp for that row
				column_for_id = chr(ws_data.max_column + 97) # Get last row [id:0 + ascii:97 = A]
				ws_data[column_for_id + str(1)] = id
				add_temp_excel(ws_data, column_for_id, last_row, temps[id])
		
		try:
			wb.save(excel_file)
		except Exception as e:
			print(e)


launch_argv = []
launch_argv = sys.argv

if "-show" in launch_argv:
	show_temp()
	sys.exit()

