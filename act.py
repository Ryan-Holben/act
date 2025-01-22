import curses
import curses.panel
import os
import sys

from command import Command
from command_list import CommandList
import constants
from top_interface import TopInterface

# Load the command list from disk.  Since main() is wrapped by curses which expects
# main to have certain arguments, and we need to access the command list both
# inside and outside of main, this forces us to give command_list this scope.
command_list = CommandList(constants.command_list_filename)

def main(stdscr):
    # Initialize the interface
    stdscr.keypad(True)
    main_interface = TopInterface(stdscr, command_list)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    # Main execution loop
    while main_interface.running():
        # Draw the interface
        main_interface.draw_all()

        # Wait for keyboard input or special actions like terminal resizing
        c = main_interface.getch()
        main_interface.check_for_resize(c)

        # Act on the input by updating the state & interface, or quitting
        cmd = main_interface.process_input(c)
        if cmd:
            return cmd

    return None

if __name__ == "__main__":
    # Some basic command line args
    # TODO: Update this and make it more formal, these are all temporary
    #       solutions.
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "last":
            try:
                with open(constants.output_filename, "r") as infile:
                    final_cmd = infile.read()
                    print(f"shell> {final_cmd}\n")
            except:
                print("Last act command not found, try running a new command")
            exit()
        if arg == "add":
            alias = input("Enter command alias: ")
            doc = input("Enter description: ")
            code = input("Enter code: ")
            command_list.add(Command(alias, doc, code))


    # Clean up any previously existing output
    if os.path.exists(constants.output_filename):
        os.remove(constants.output_filename)

    # By default the OS inserts a delay before reading ESC.  We override this.
    os.environ.setdefault("ESCDELAY", "0")

    # Set up curses in a way that plays nicely with the terminal.  If we exit in
    # any way, including by throwing exceptions, an exit hook will restore th
    # terminal to its previous state.  Also sets some commonly used settings.
    ret = curses.wrapper(main)

    # If main() returned a command the user wants to run, we:
    # - print the user's command
    # - print command's resolved form that will be executed by the shell
    # - write resolved form to a temporary file & exit
    # - after this Python script terminates, act.sh will then look for this output
    #   file & execute the command it contains
    if ret is not None:
        print(f"\nact>   {ret}")
        final_cmd = command_list.expand_command(ret)
        print(f"shell> {final_cmd}\n")
        try:
            with open(constants.output_filename, "w") as outfile:
                outfile.write(final_cmd)
        except Exception as e:
            print(f"Error encountered while writing to {constants.output_filename}:")
            print(e)
            print("act may not function until this error is resolved! ")