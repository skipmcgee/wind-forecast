#!/bin/bash
# execute this from project dir
pip3 install --user virtualenv
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r ../requirements.txt
