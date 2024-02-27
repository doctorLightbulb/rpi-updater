#!/bin/bash

# A simple wrapper for the source command.

# This script acts as a go-between. It activates the Python virtual
# environment when called by updater at launch.
. /home/Joshua/Documents/Scripts/Python/updater/venv/bin/activate

read -r -p "Enter commands: " commands
python /home/Joshua/Documents/Scripts/Python/updater/updater.py "$commands"
