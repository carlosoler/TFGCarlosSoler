#!/bin/bash

trap 'kill $BGPID; exit' INT
python3 R.py &
BGPID=$!
python3 app.py