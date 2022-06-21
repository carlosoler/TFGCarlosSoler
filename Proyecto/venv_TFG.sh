#!/bin/bash

pip install virtualenv
virtualenv venv_TFG -p python3.7
source venv/bin/activate
pip install -r requirements.txt