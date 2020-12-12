# rpi-temp-logger

----

This repo is updated, from initial "dump"-versio what I done many years ago,
to complete my college open studies programmin cource.

----

DS1820 temperature sensors are emulated to locate in same folder with .py -file
*[because I dont't have sensors nor connected right now in my RaspberryPi]*
in `./sys/bus/w1/devices/yy-xxxxxxxxxxxx/` -folder, where 'yy' is sensors family code
and xxx is unique adress name. DS1820 and DS18S20 yy = 10, DS18B20 yy = 28 and DS1822 yy = 22.
*[I'm not however sure does code work other than DS1820 or 18S20*]
Each sensor folder have `w1_slave` -file that contain roughly following information:

```
0f 00 4b 46 ff ff 06 10 0c : crc=0c YES
0f 00 4b 46 ff ff 06 10 0c t=25375
```

In real scenario, folder structure are located in system root `/sys/bus/w1/devices/...`

Program is designed to run as schedule task with eg. cron.

## Enable 1-wire in RaspberryPi

```bash
# temporary
sudo modprobe w1-gpio
sudo modprobe w1-therm

# >> /etc/modules
w1-gpio pullup=1
w1-therm

sudo nano /boot/config.txt
>> dtoverlay=w1-gpio,gpiopin=4

sudo raspi-config
> 5. Interface Option
>> P7 1-Wire
>>> Enable
```

Pin 7 (GPIO4)
