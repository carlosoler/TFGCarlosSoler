#!/bin/bash

trap 'kill $BGPID; exit' INT
python3 /home/ubuntu/TFGCarlosSoler/Proyecto/R.py &
BGPID=$!
python3 /home/ubuntu/TFGCarlosSoler/Proyecto/app.py

#python3 /Users/carlosoler/Documents/GitHub/TFGWord/TFGCarlosSoler/Proyecto/R.py &
#python3 /Users/carlosoler/Documents/GitHub/TFGWord/TFGCarlosSoler/Proyecto/app.py