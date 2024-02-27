# updater.py

"""
A simple CLI application to automate updating the Raspberry Pi. 

The user begins the update manually, and the updater continues the process, handling any and all interruptions, until the updates are complete.
"""


import sys
import subprocess
import shlex
import logging
import time
from datetime import datetime
from http.client import RemoteDisconnected
from urllib import request, error
from contextlib import suppress

from rich.console import Console
from rich.theme import Theme


class Updater:
    def __init__(self, console: Console) -> None:
        self.console = console

    def run(self):
        """Run the process.
        """
        commands = sys.argv[1:]
        validated_command = self.validate_command(commands)

        if not validated_command:
            self.console.print(self.rejected_input(commands), style="error")
        else:
            start_time = datetime.now()
            try:
                with suppress(KeyboardInterrupt):
                    self.run_process(validated_command, "Staring process...")

                self.console.print(
                    self._dated_message("[bold green]Process finished at")
                )
            except KeyboardInterrupt:
                self.console.print(
                    self._dated_message("[underline bold white]Process interrupted at")
                )

            end_time = datetime.now()
            total_time_on_process = end_time - start_time

            self.console.print(f"Total time spent on process: [bold white]{total_time_on_process}[/]")
    
    def _dated_message(self, message: str) -> str:
        """Combine a date to a message and return the result.
        """
        time_stamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        return f"\n\n{message}: {time_stamp}"

    
    def validate_command(self, commands: list[str]) -> None | str:
        """Validate input from the user using whitelist method.
        """
        command = " ".join([i for i in commands])
        sudo_apt = "sudo apt"
        instructions = ["update", "upgrade", "full-upgrade", "dist-upgrade",]
        accepted_commands = [sudo_apt + f" {i}" for i in instructions]

        if any(_ in command for _ in accepted_commands):
            return command
        return None
    
    def rejected_input(self, commands: list[str]) -> list[str]:
        """Remove "sudo apt" from the output if they were used.
        """
        if "install" in commands:
            return "Installing applications is not supported by " \
                "this utility at this time."
        elif "sudo" and "apt" in commands:
            return f"Unaccepted values: {' '.join([i for i in commands[2:]])}"
        else:
            return f"Unaccepted values: {' '.join([i for i in commands])}"
        
    def run_process(self, command: str, message: str) -> None:
        """Run and repeat the process until it finishes.

        This function passes "command" to subprocess and then repeats 
        the command if the download is interrupted. If anything else happens, the function does nothing.

        Progress indicator:
        Need to get 89.0 MB/213 MB of archives.

        """
        tries = 0
        delay_time = int(0.50 * 60)

        while True:
            try:
                if self._internet_is_on():
                    self.console.print(f"\n{message}", style="notice")
                    args = shlex.split(command)
                    result = subprocess.run(
                        args, capture_output=True, encoding="utf-8"
                    )

                    if result.stdout:
                        self.console.print("\nDetails:\n")
                        self.console.print(result.stdout)
                    if result.stderr:
                        self.console.print("\nErrors:\n", style="error")
                        self.console.print(result.stderr, style="error")

                    if self._execution_terminated(result):
                        self.console.print("Process interrupted.\n", 
                                           style="error")
                        self.run_process(command, 
                                    "Restarting process...")
                    else:
                        return True
            except (TimeoutError, RemoteDisconnected) as err:
                self.console.print(
                    f"{datetime.now().strftime('%H:%M:%S')} - {err}",
                    style="error"
                )
                tries = 0
            
            tries += 1
            previous_time = self._delay(tries, delay_time)
            delay_time = previous_time

            time.sleep(previous_time)

    def _internet_is_on(self) -> bool:
        """Check whether there is an active internet connection.
        """
        for timeout in [1, 5, 10, 15]:
            try:
                request.urlopen("https://google.com", timeout=timeout)
                return True
            except error.URLError as err:
                self.console.print(
                    f"[yellow]{datetime.now().strftime('%H:%M:%S')}[/] - [bold red]{err}[/]"
                )
        return False


    def _execution_terminated(self, result: str) -> bool:
        """This function takes apt's output and determines 
        whether the process was successful or ended prematurely.
        """
        update_failed = "Unable to fetch some archives" in result.stderr
        upgrade_failed = "Some index files failed to download" in result.stderr

        if (update_failed or upgrade_failed):
            return True
        return False
    
    def _delay(self, round: int, delay_time: int, 
               time: str = "minutes") -> None:
        """Delay execution for an increasing length of time acccording to 
        the number of failed tries.
        """
        if time == "minutes": 
            seconds_factor = 60 
        else: 
            # Revert to seconds
            seconds_factor = 0

        # The keys correspond to the round.
        # The values are the time in minutes.
        minutes = {1: 0.5, 2: 1, 4: 2, 
                6: 5, 10: 15}
        previous_delay_time = delay_time

        if round in minutes.keys():
            return int(minutes.get(round) * seconds_factor)  # Minutes to delay.
        return previous_delay_time


def main():
    """Run the program.
    """
    console = Console(
        theme=Theme(
            {"error": "bold red",
             "notice": "yellow",
             "success": "bold green"}
        )
    )
    app = Updater(console)
    app.run()


if __name__ == "__main__":
    main()