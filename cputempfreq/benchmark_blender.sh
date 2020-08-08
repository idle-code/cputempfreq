#!/usr/bin/env bash

./cputempfreq.py --logfile cpu_info.blender.koro.csv &
sleep 60

./benchmark-launcher-cli benchmark koro -b 2.83
sleep 60

kill %1


