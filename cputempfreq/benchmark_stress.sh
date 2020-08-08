#!/usr/bin/env bash

./cputempfreq.py --logfile cpu_info.stress.csv &
sleep 60

stress --cpu 8 --timeout 10m
sleep 60

kill %1
