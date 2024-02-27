# Raspberry Pi Updater

A simple script to automatically resume downloading updates.

> Note: This script is needed only if the Pi has an unsteady Wi-Fi connection.

Have you ever had the following ecperience? You start your Raspberry Pi downloading updates. Then you leave the room for a while. When you return, you find that your Raspberry Pi failed to "fetch some archives."

That is precisely what this script is for.

## Prerequities

To run the script, Python 3.11 must be installed on the machine. The script uses a third-prty library called `Rich`. So, a virtual environment is needed.

To set up a Python virtual environment (in this case, `venv`), navigate to the folder in which you wish to house the script. Open a terminal window from that folder (press `F4`) and enter the following command:

```bash
# Install the virtual environment
python -m venv venv --prompt="updater"
```

Activate the virtual environment with the following command:

```bash
# Activate the virtual environment
source venv/bin/activate
```

If you are not using `bash`, replace `source` with a period (`.`):

```bash
# Alternate activation method.
. venv/bin/activate
```

Update `pip` with this command:

```bash
python -m pip install --upgrade pip
```

Now, install `Rich`:

```bash
pip install rich
```

The script `updater.py` was developed using `rich` version `13.7.0`, though other versions _should_ work, too.

## How to use the Script

With the virtual environment activated, the script can be run this way:

```powershell
python updater.py sudo apt update
```

Without the virtual environment activated, the script can also be run using the `bash` convenience script, `updater.sh`:

```bash
bash updater.sh
```

Currently, the script prompts you for the commands. This will change later to accept the commands on the same line that invokes the script.

All `updater.sh` does is activate the Python virtual environment, accept a command from the user and then run `updater.py`.

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
