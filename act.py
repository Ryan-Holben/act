import curses
import curses.panel
import os
import subprocess

from command_list import CommandList
from command import Command
import constants
from top_interface import TopInterface


# Initialize the command list & fuzzy search on an empty string
command_list = CommandList(constants.command_list_filename)

def main(stdscr):
    # Initialize the interface
    stdscr.keypad(True)
    main_interface = TopInterface(stdscr)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)

    # Main execution loop
    while main_interface.running():
        # Draw the interface
        matches = command_list.fuzzy_find(main_interface.interface_search.input_str)
        main_interface.draw_all(command_list, matches)

        # Wait for keyboard input or special actions like terminal resizing
        c = main_interface.getch()
        main_interface.check_for_resize(c)

        # Act on the input by updating the state & interface, or quitting
        cmd = main_interface.process_input(c, command_list, matches)
        if cmd:
            return cmd

    return None

if __name__ == "__main__":
    # Cleanup any previously existing output
    if os.path.exists(constants.output_filename):
        os.remove(constants.output_filename)

    # The OS by default inserts a delay before reading ESC
    os.environ.setdefault("ESCDELAY", "0")

    # Set up curses in a way that plays nicely with the terminal.  If we exit in any way, including by throwing
    #   exceptions, an exit hook will restore the terminal to its previous state.  Also sets some commonly used
    #   settings.
    ret = curses.wrapper(main)

    # If main() returned a command the user wants to run, we:
    # - print its resolved form
    # - write it to a special file & exit
    # - act.sh will then see that file & execute the command it contains
    if ret is not None:
        final_cmd = command_list.expand_command(ret)
        print("> " + final_cmd + "\n")
        with open(constants.output_filename, "w") as outfile:
            outfile.write(final_cmd)


# def test():
#     print(command_list.expand_command("echo $cat"))
#     # print(len(command_list.commands))
#     # for alias in command_list.commands:
#     #     print(alias)

# test()