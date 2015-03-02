#!/usr/bin/python
import time
import sys
import struct
import argparse
from time import gmtime, strftime

from machinekit import hal

name = "ring_0"
interval = 1.0
count = 0
minValue = 0
maxValue = 0
value = 0
valueSum = 0

parser = argparse.ArgumentParser(description='Component to log and calculate statistics from values from a ring buffer')
parser.add_argument('-n', '--name', help='Ring buffer name', default='ring_0')
parser.add_argument('-i', '--interval', help='Poll interval in seconds', default=1.0)

args = parser.parse_args()

name = args.name
interval = float(args.interval)

if name in hal.rings():
    r = hal.Ring(name)
else:
    sys.stderr.write('error: HAL ring buffer "' + name + '" not found\n')
    exit(1)

while True:
    record = r.read()
    if record is None:
        avgValue = valueSum / count
        medianValue = (maxValue - minValue) / 2
        timeString = strftime("%b %d %H:%M:%S", gmtime())
        print(timeString + " - count: " + str(count) + " min: " + str(minValue) + " max: " +
              str(maxValue) + " mean: " + str(avgValue) + " median: " + str(medianValue))
        minValue = value
        maxValue = value
        count = 0
        valueSum = 0
        time.sleep(interval)
    else:
        count += 1
        value = struct.unpack("i", record.tobytes())[0]
        if (value < minValue):
            minValue = value
        if (value > maxValue):
            maxValue = value
        valueSum += value
        r.shift()  # consume

exit(0)
