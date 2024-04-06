#!/bin/bash
# execute this from project dir
pip3 install --user virtualenv
python3 -m venv ./venv
source venv/bin/activate
pip3 install flask-mysqldb
pip3 install openmeteo-requests
pip3 install requests-cache retry-requests numpy pandas
pip3 install python-dotenv
