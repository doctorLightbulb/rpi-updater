# Raspberry Pi Updater

A simple script to automatically resume downloading updates.

> Note: This script is needed only if the Pi has an unsteady Wi-Fi connection.

Have you ever had the following ecperience? You start your Raspberry Pi downloading updates. Then you leave the rooom for a while. When you return, you find that your Raspberry Pi failed to "fetch some archives."

That is precisely what this script is for.

## Prerequities

To run the script, Python 3.11 must be installed on the machine. The script uses the Python Standard Library, so no virtual environment or third-party dependencies are needed.

## How to use the Script

```powershell
python updater.py sudo apt update
```

## Supported Commands

* sudo apt update
* sudo apt upgrade
* sudo apy dist-upgrade
* sudo apt full-upgrade

Any additional flags to these commands, such as `-y`, are also supported.

## What RPI-Updater Does

* Resumes downloading updates if the download times out.
* Keeps trying to connect to the internet if the connection is lost.
* Keeps running until stopped by the user.

## What RPI-Updater Does Not Do

* Install updates or programs.
* Automate installing updates

## Disclaimer

This script was developed using Python 3.11.2 on a Raspberry Pi 4, running Bookworm OS. It has not been tested on any other machine or operating system.
