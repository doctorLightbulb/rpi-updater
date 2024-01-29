# updater.py

"""
A simple CLI application to automate updating the Raspberry Pi. 

The user begins the update manually, and the updater continues the process, handling any and all interruptions, until the updates are complete.
"""

import sys
import subprocess
import time
import shlex
import logging
from datetime import datetime
from urllib import request, error


def main():
    commands = sys.argv[1:]
    validated_command = validate_command(commands)

    if not validated_command:
        print(rejected_input(commands))
    else:
        start_time = datetime.now()
        run_process(validated_command, "Staring process...")

        end_time = datetime.now()
        total_time_on_process = end_time - start_time
        print(f"\n\nTotal time spent on process: {total_time_on_process}")


def validate_command(commands: list[str]) -> None | str:
    """Validate input from the user.
    """
    command = " ".join([i for i in commands])
    sudo_apt = "sudo apt"
    instructions = ["update", "upgrade", "full-upgrade", "dist-upgrade",]
    accepted_commands = [sudo_apt + f" {i}" for i in instructions]

    if any(_ in command for _ in accepted_commands):
        return command
    return None


def rejected_input(commands: list[str]) -> list[str]:
    """Remove "sudo apt" from the output if they were used.
    """
    if "install" in commands:
        return "Installing applications is not supported by " \
               "this utility at this time."
    elif "sudo" and "apt" in commands:
        return f"Unaccepted values: {' '.join([i for i in commands[2:]])}"
    else:
        return f"Unaccepted values: {' '.join([i for i in commands])}"


def run_process(command: str, message: str) -> None:
    """Run and repeat the process until it finishes.

    This function passes "command" to subprocess and then repeats the command 
    if the download is interrupted. If anything else happens, the function does 
    nothing.

    Progress indicator:
    Need to get 89.0 MB/213 MB of archives.

    """
    tries = 0
    delay_time = int(0.50 * 60)

    while True:
        try:
            if internet_is_on():
                print(f"\n{message}")
                args = shlex.split(command)
                result = subprocess.run(
                    args, capture_output=True, encoding="utf-8"
                )

                if result.stdout:
                    print("\nDetails:\n")
                    print(result.stdout)
                if result.stderr:
                    print("\nErrors:\n")
                    print(result.stderr)

                if execution_terminated(command, result):
                    print("Process interrupted.\n")
                    run_process(command, 
                                "Restarting process...")
                else:
                    return True
        except TimeoutError as err: print(err)
        
        tries += 1
        previous_time = delay(tries, delay_time)
        delay_time = previous_time
        time.sleep(previous_time)


def delay(round: int, delay_time: int, time: str = "minutes") -> None:
    """Delay execution for an increasing length of time acccording to 
    the number of failed tries.
    """
    if time == "minutes": 
        convert_to_seconds = 60 
    else: 
        # Revert to seconds
        convert_to_seconds = 0
    minutes = {
        1: 0.5,
        2: 1,
        4: 2,
        6: 5,
        10: 15,
    }
    previous_delay_time = delay_time

    if round in minutes.keys():
        minutes_to_delay = int(minutes.get(round) * convert_to_seconds)
        return minutes_to_delay
    return previous_delay_time


def internet_is_on() -> bool:
    """Check whether there is an active internet connection.
    """
    for timeout in [1, 5, 10, 15]:
        try:
            request.urlopen("https://google.com", timeout=timeout)
            return True
        except error.URLError as err: print(err)
    return False


def execution_terminated(command: str, result: str) -> bool:
    """This function takes apt's output and determines 
    whether the process was successful or ended prematurely.

    This is necessary becuase apt does not exit with an error code 
    even though the process it began was interrupted.
    """
    if "Unable to fetch some archives" in result.stderr:
        return True
    return False


if __name__ == "__main__":
    main()