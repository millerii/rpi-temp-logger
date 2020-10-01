#!/usr/bin/python
# -*- coding: utf-8 -*-

#########################################################################################
# ToDo	Anturien automaattinen etsinta ja loydettyjen luku				#
# 23.9.14	Lisatty lampotilan tallennus vuotta/kuukautta vastaavaan tiedostoon	#
# 12.3.13	Lisatty virhekayttaytyminen jos anturitidostoa ei loydy.		#
# 9.3.13	Lisatty CRC-tarkistus ja virhetilanteesa 3 uudelleenyritysta		#
#########################################################################################

import datetime

now = datetime.datetime.now()
check_crc = "N"

# Ensimmainen anturi
# Luetaan anturintiedostoa jos CRC tarkistus on OK. Muuten yritetaan yritetaan uudestaan
reply = 0
while reply <= 3:
	try:
		# Open the file so that python can see what is in it. Replace the serial number as before.
		tfile = open("/sys/bus/w1/devices/10-000800aac8dc/w1_slave")
		# Read all of the text in the file.
		text = tfile.read()
		# Close the file now that the text has been read.
		tfile.close()
		# Kaivetaan anturin CRC tarkistus YES/NO-tulos
		check_crc = text.split("\n")[0]
		check_crc = check_crc.split(" ")[11]
		check_crc = str(check_crc[0:1])
		reply = reply + 1
		#Jos tarkistus OK jatketaan eteenpain
		if check_crc == "Y":
			reply = 0
			break
	except IOError:
		temperature1 = ""
		break
	
# Jos CRC-tarkistus ei menny 3. yrittamalla lapi, lampotila jatetaan pois.
if check_crc == "N":
	temperature1 = ""
else:
	# Split the text with new lines (\n) and select the second line.
	secondline = text.split("\n")[1]
	# Split the line into words, referring to the spaces, and select the 10th word (counting from 0).
	temperaturedata = secondline.split(" ")[9]
	# The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
	temperature1 = float(temperaturedata[2:])
	# Put the decimal point in the right place and display it.
	temperature1 = temperature1 / 1000
	temperature1 = str(round(temperature1, 2))

check_crc = "N"

# Toinen anturi
# Luetaan anturintiedostoa jos CRC tarkistus on OK. Muuten yritetaan yritetaan uudestaan
reply = 0
while reply <= 3:
	try:
		tfile = open("/sys/bus/w1/devices/10-000800e96437/w1_slave")
		text = tfile.read()
		tfile.close()
		# Kaivetaan anturin CRC tarkistus YES/NO-tulos
		check_crc = text.split("\n")[0]
		check_crc = check_crc.split(" ")[11]
		check_crc = str(check_crc[0:1])
		reply = reply + 1
		#Jos tarkistus OK jatketaan eteenpain
		if check_crc == "Y":
			reply = 0
			break
	except IOError:
		temperature2 = ""
		break

# Jos CRC-tarkistus ei menny 3. yrittamalla lapi, lampotila jatetaan pois.
if check_crc == "N":
	temperature2 = ""
else:
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature2 = float(temperaturedata[2:])
	temperature2 = temperature2 / 1000
	temperature2 = str(round(temperature2, 2))

# Tallennetaan tulokset vuotta/kuukautta vastaavaan tiedostoon
year_month = now.strftime("%Y_%m_")
tlog = open("/home/pi/" + year_month + "temp_log.xls", "a")
date = now.strftime("%d.%m.%Y")
time = now.strftime("%H:%M:%S")
tlog.write(date + "\t" + time + "\t" + temperature1.replace(".",",") + "\t" + temperature2.replace(".",",") + "\n")
tlog.close()

#print "Temp 1:", temperature1, "C"
#print "Temp 2:", temperature2, "C"
#print date, time
