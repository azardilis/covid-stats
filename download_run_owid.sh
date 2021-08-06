#!/usr/bin/env bash

rm owid-covid-data.csv
wget https://covid.ourworldindata.org/data/owid-covid-data.csv
python3 hosps.py
