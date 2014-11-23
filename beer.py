#!/usr/bin/env python
import serial
import datetime
import sys
import time
import rrdtool
import re

RRD="beer01.rrd"

try:
	with open(RRD,"r") as file:
		pass
except IOError:
	ret = rrdtool.create(RRD, "--step", "60", "--start", '0',
	"DS:bubbles:ABSOLUTE:60:U:U",
	"DS:temp:GAUGE:60:U:U",
	"DS:light:GAUGE:60:U:U",
	"RRA:AVERAGE:0.5:1:129600",
	"RRA:AVERAGE:0.5:60:2160",
	"RRA:LAST:0.5:1:129600",
	"RRA:LAST:0.5:60:2160",
	"RRA:MIN:0.5:1:129600",
	"RRA:MIN:0.5:60:2160",
	"RRA:MAX:0.5:1:129600",
	"RRA:MAX:0.5:60:2160");
	if ret:
	 	print rrdtool.error()

with serial.Serial("/dev/rfcomm0", 57600, timeout=1) as ser:
	while True:
		ser.write("A");
		line = ser.readline().strip();

		if line:
			match = re.match(r"celsius:(?P<temp>[0-9.]+)\slux:(?P<light>[0-9.]+) bubbles:(?P<bubbles>[0-9]+)", line)
			if match:
				temp, light, bubbles = match.groups()

				ret = rrdtool.update(RRD,'N:%s:%s:%s' % (bubbles, temp, light));
				if ret:
					print rrdtool.error()
					continue

				print("%s temp:%s light:%s bubbles:%s" % (datetime.datetime.now(), temp, light, bubbles))
				sys.stdout.flush()
		time.sleep(10)
