#!/usr/bin/env python
import serial
import datetime
import sys
with serial.Serial("/dev/ttyACM0", 115200, timeout=1) as ser:
	while True:
		line = ser.readline().strip();
		if line:
			print("%s %s" % (datetime.datetime.now(), line))
			sys.stdout.flush()
