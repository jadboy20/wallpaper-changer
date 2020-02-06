#!/bin/bash

# ONLY COMPATIBLE WITH WINDOWS BASH!!

set -e

case "$1" in
    "clean")
        echo Cleaning build artefacts.
        echo Removing build/
        echo Removing dist/
        rm -r build
        rm -r dist
        ;;

    "build")
        echo Building project
        # Enter the virtual environment
        source venv/Scripts/activate

        pip install -r requirements.txt

        pyinstaller --onefile --noconsol changer.py
        ;;

    *)
        echo Unknown command.
        echo "usage: $0 (build|clean)"
        ;;

esac