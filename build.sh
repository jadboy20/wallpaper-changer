#!/bin/bash

# ONLY COMPATIBLE WITH WINDOWS BASH!!

set -e

# Enter the virtual environment
source venv/Scripts/activate

pip install -r requirements.txt

pyinstaller --onefile changer.py