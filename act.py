import curses
import curses.panel
import os
import subprocess

from command import Command
from command_list import CommandList
from constants import command_list_filename

from top_interface import TopInterface


command_list = CommandList()

def main(stdscr):
    # Initialize the command list & fuzzy search on an empty string
    command_list.load(command_list_filename)
    matches = command_list.fuzzy_find("")

    # Initialize the interface
    stdscr.keypad(True)
    main_interface = TopInterface(stdscr)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    # Main execution loop
    while main_interface.running():
        # Draw the interface
        main_interface.draw_all(command_list, matches)

        # Wait for keyboard input & special actions like terminal resizing
        c = main_interface.getch()
        main_interface.check_for_resize(c)

        # Act on the input
        main_interface.process_input(c)

    return

    # while True:
    #     # Query the possible actions
    #     matches = command_list.fuzzy_find(interface.input_str)

    #     # Read any keyboard input. Doesn't use buffering, which means we have to handle a lot of things manually,
    #     #   but we can also use special keys, and respond instantly to them.
    #     if interface_state == "main typing":
    #         c = interface.getch()
    #         if c == 27:     # ESC key to quit
    #             return
            
    #         elif c == curses.KEY_RESIZE:        # Detect when the terminal gets resized, and update the interface to match
    #             resize(stdscr)

    #         elif c >= 32 and c < 127:         # Standard text input
    #             if len(interface.input_str) < interface.const.input_str_w - 1:
    #                 interface.input_str += chr(c)
    #                 matches = command_list.fuzzy_find(interface.input_str)

    #         elif c == 127 and len(interface.input_str) > 0:    # Delete key
    #             interface.input_str = interface.input_str[:-1]
    #             matches = command_list.fuzzy_find(interface.input_str)
                
    #         elif c == 10:       # Enter key
    #             # command_list.add(interface.input_str)
    #             # interface.input_str = ""
    #             if interface.input_str == matches[interface.selected][0].alias:
    #                 # return interface.input_str
    #                 return matches[interface.selected][0].code
    #             interface.input_str = matches[interface.selected][0].alias
    #             matches = command_list.fuzzy_find(interface.input_str)
    #             interface.selected = 0

    #         elif c == curses.KEY_UP:
    #             interface.selected += 1

    #         elif c == curses.KEY_DOWN:
    #             interface.selected -= 1
                
    #         elif c == ord("\t"):
    #             # interface.input_str = "BIG CHUNGUS"
    #             interface_state = "esc menu"
        
    #         if interface.selected >= min(len(matches), interface.const.list_max_num_lines):
    #             interface.selected = min(len(matches), interface.const.list_max_num_lines) - 1
    #         elif interface.selected < 0:
    #             interface.selected = 0
        
    #     elif interface_state == "esc menu":
    #         if c == 27:
    #             return
    #         # elif c == 10:
    #         #     interface_state = "main typing"

    #     # Draw the interface
    #     interface.draw(matches, command_list)


if __name__ == "__main__":
    # Set up curses in a way that plays nicely.  For example, if we exit in any way, including by throwing exception,
    #   an exit hook will restore the terminal to its previous state.  Also sets some commonly used settings.
    os.environ.setdefault("ESCDELAY", "0")
    ret = curses.wrapper(main)
    if ret:
        print("> " + ret + "\n")
        s = subprocess.getstatusoutput(ret)
        print(s[1])
        if s[0] != 0:
            print(f"Command returned nonzero value {s[0]}")

    command_list.save(command_list_filename)