@echo off

call venvPrueba\Scripts\activate

start /B python R.py
start /B python app.py