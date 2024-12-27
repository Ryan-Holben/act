import curses
import os
import subprocess

from command import Command
from command_list import CommandList
from constants import command_list_filename
from interface import Interface


command_list = CommandList()
# command_list.add(Command("list/python", "List all Python files in the current folder", "ls -lah *.py"))
# command_list.add(Command("home", "Print the home directory", "echo $HOME"))
# command_list.add(Command("Fancy echo", "See what it does!", "echo We live in $HOME and we\\\'re visiting $(pwd)"))
# command_list.add(Command("Hello world", "This is a test command", "echo Hello world!"))
# command_list.add(Command("cat", "dog", "bird"))
# command_list.add(Command("list files", "List all files in human readable format", "ls -lah"))


def draw(state, interface, matches):
    interface.draw(matches, command_list, state)
    # print(state)
    if state[0] == "main":
        pass # draw interface
    elif state[0] == "menu":
        if len(state) == 1:
            pass # display options: ESC to quit, S to save, D to delete
        elif len(state) == 2 and state[1] == "save":
            pass # display wizard to save
        elif len(state) == 2 and state[1] == "delete":
            pass # display wizard to delete

def process_inputs(c):
    return

def main(stdscr):
    command_list.load(command_list_filename)

    stdscr.keypad(True)
    interface = Interface(stdscr)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    # Draw the interface
    matches = command_list.fuzzy_find("")
    # interface.draw(matches, command_list)

    # # Main interface loop

    def match(state, *match):
        # return len(state) <= len(match) and state[:len(match)] == list(match)
        return len(state) >= len(match) and state[:len(match)] == list(match)

    state = ["main"]
    while len(state) > 0 and state[0] != "quit":
        draw(state, interface, matches)
        process_inputs(state)
        c = interface.getch()

        # if state[0] == "main":
        #     if c == 27:
        #         state[0] = "menu"
        #     else:
        #         pass # Call main interface here
        # elif state[0] == "menu":
        #     if len(state) == 1:
        #         if c == 27:
        #             state[0] = "quit"
        #         elif c == ord("s"):
        #             state.append("save")
        #         elif c == ord("d"):
        #             state.append("delete")
        #     else:
        #         if state[1] == "save":
        #             if c == 27:
        #                 state.pop()
        #         elif state[1] == "delete":
        #             if c == 27:
        #                 state.pop()
    
        if match(state, "main"):
            if c == 27:
                state = ["menu"]
            else:
                pass # Call main interface here
        elif match(state, "menu"):
            if len(state) == 1:
                if c == 27:
                    state = ["quit"]
                elif c == ord("s"):
                    state.append("save")
                elif c == ord("d"):
                    state.append("delete")
            else:
                if match(state, "menu", "save"):
                    if c == 27:
                        state.pop()
                elif match(state, "menu", "delete"):
                    if c == 27:
                        state.pop()

    return



    while True:
        # Query the possible actions
        matches = command_list.fuzzy_find(interface.input_str)

        # Read any keyboard input. Doesn't use buffering, which means we have to handle a lot of things manually,
        #   but we can also use special keys, and respond instantly to them.
        if interface_state == "main typing":
            c = interface.getch()
            if c == 27:     # ESC key to quit
                return
            
            elif c == curses.KEY_RESIZE:        # Detect when the terminal gets resized, and update the interface to match
                interface.resize()

            elif c >= 32 and c < 127:         # Standard text input
                if len(interface.input_str) < interface.const.input_str_w - 1:
                    interface.input_str += chr(c)
                    matches = command_list.fuzzy_find(interface.input_str)

            elif c == 127 and len(interface.input_str) > 0:    # Delete key
                interface.input_str = interface.input_str[:-1]
                matches = command_list.fuzzy_find(interface.input_str)
                
            elif c == 10:       # Enter key
                # command_list.add(interface.input_str)
                # interface.input_str = ""
                if interface.input_str == matches[interface.selected][0].alias:
                    # return interface.input_str
                    return matches[interface.selected][0].code
                interface.input_str = matches[interface.selected][0].alias
                matches = command_list.fuzzy_find(interface.input_str)
                interface.selected = 0

            elif c == curses.KEY_UP:
                interface.selected += 1

            elif c == curses.KEY_DOWN:
                interface.selected -= 1
                
            elif c == ord("\t"):
                # interface.input_str = "BIG CHUNGUS"
                interface_state = "esc menu"
        
            if interface.selected >= min(len(matches), interface.const.list_max_num_lines):
                interface.selected = min(len(matches), interface.const.list_max_num_lines) - 1
            elif interface.selected < 0:
                interface.selected = 0
        
        elif interface_state == "esc menu":
            if c == 27:
                return
            # elif c == 10:
            #     interface_state = "main typing"

        # Draw the interface
        interface.draw(matches, command_list)


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