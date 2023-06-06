#!/bin/bash

trap 'kill $BGPID; exit' INT
python3 /home/ubuntu/TFGCarlosSoler/Proyecto/R.py &
BGPID=$!
python3 /home/ubuntu/TFGCarlosSoler/Proyecto/app.py
