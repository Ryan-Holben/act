import curses
import os
import subprocess

from command import Command
from command_list import CommandList2

class InterfaceConstants():
    def __init__(self, win):
        self.input_y = curses.LINES - 1
        self.input_x = 3
        self.input_prompt_str = "> "
        self.input_separator_y = self.input_y - 1
        self.input_separator_x = 2
        self.input_separator_len = curses.COLS - 4
        self.input_str_y = self.input_y
        self.input_str_x = self.input_x + len(self.input_prompt_str)
        self.input_str_w = curses.COLS - 2 * self.input_str_x
        self.list_max_num_lines = self.input_separator_y - 2 
        self.list_x = self.input_x
        self.list_last_y = self.input_separator_y - 1
        self.list_w = self.input_str_w
        self.num_cols = 3
        self.side_buf = 2
        self.col_sep = 1
        self.col_width = int((curses.COLS - 2 * self.side_buf) / self.num_cols) - self.col_sep * (self.num_cols - 1)


class Interface():
    def __init__(self, stdscr):
        self.screen = stdscr
        self.initialize_window()
        self.compute_constants()
        self.input_str = ""
        self.selected = 0

    def compute_constants(self):
        self.const = InterfaceConstants(self.win)

    def initialize_window(self):
        """Internal function to manage a window object.  Behavior is better using this for drawing & getch,
            rather than working directly with the screen object."""
        self.win = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        self.win.keypad(True)

    def draw_highlighted_text(self, y, x, string, indices):
        """Draws a string at the given location, highlighting the specified indices."""
        if len(string) >= self.const.col_width:
            string = string[:self.const.col_width]

        if indices == None or len(indices) == 0:
            self.win.addstr(y, x, string)
        else:
            j = 0
            for i in range(len(string)):
                if j < len(indices) and i == indices[j]:
                    self.win.addstr(y, x + i, string[i], curses.color_pair(1) | curses.A_UNDERLINE | curses.A_BOLD)
                    j += 1
                else:
                    self.win.addstr(y, x + i, string[i])
    
    def draw(self, matches, command_list):
        # Setup constants
        self.compute_constants()

        # Erase the window, draw borders
        self.win.clear()
        self.win.border(0, 0, 0, ' ', 0, 0, curses.ACS_VLINE, curses.ACS_VLINE)
        self.win.hline(self.const.input_separator_y, self.const.input_separator_x, curses.ACS_HLINE, self.const.input_separator_len)

        # Add contents
        self.display_terminal_size()
        self.display_num_commands(matches, command_list)
        self.win.addstr(self.const.input_y, self.const.input_x, self.const.input_prompt_str)
        self.win.addstr(self.const.input_str_y, self.const.input_str_x, self.input_str)

        if matches:                                             # Fuzzy find search results
            if len(matches) > 0 and self.input_str == matches[self.selected][0].alias:
                run_str = "Press enter to run"
                self.win.addstr(self.const.input_str_y, curses.COLS - len(run_str) - 10, run_str, curses.A_STANDOUT)
            
            filtered = matches[:self.const.list_max_num_lines]
            for match_idx in range(len(filtered)):
                cmd, indices, _ = filtered[match_idx]
                idx_str = str(match_idx) + ": " if match_idx < 10 else ""
                if match_idx == self.selected:
                    self.win.addstr(self.const.list_last_y - match_idx, self.const.list_x-3, "-> " + idx_str, curses.color_pair(1))
                else:
                    self.win.addstr(self.const.list_last_y - match_idx, self.const.list_x, idx_str)

                y = self.const.list_last_y - match_idx
                x = self.const.list_x + len(idx_str)
                self.draw_highlighted_text(y,
                                           x,
                                           cmd.alias,
                                           indices["alias"] if indices != {} else [])
                self.draw_highlighted_text(y,
                                           x + self.const.col_width,
                                           cmd.doc,
                                           indices["doc"] if indices != {} else [])
                self.draw_highlighted_text(y,
                                           x + 2*self.const.col_width,
                                           cmd.code,
                                           indices["code"] if indices != {} else [])

        # Move the input cursor
        self.win.addstr(self.const.input_str_y, self.const.input_str_x + len(self.input_str), "_", curses.A_BLINK | curses.A_BOLD)
        self.win.move(self.const.input_str_y, self.const.input_str_x + len(self.input_str))

        # Render all of the above drawings that we have prepared
        self.win.refresh()

    def resize(self):
        """Call this when we detect the terminal was resized."""
        curses.resizeterm(*self.screen.getmaxyx())
        self.compute_constants()
        self.initialize_window()

    def display_terminal_size(self):
        self.win.addstr(0, 0, f"cols: {curses.COLS}, lines: {curses.LINES}")

    def display_num_commands(self, matches, command_list):
        self.win.addstr(0, 10, f"Displaying {len(matches)} / {len(command_list)} commands")
    
    def getch(self):
        return self.win.getch()
    


def main(stdscr):
    stdscr.keypad(True)
    interface = Interface(stdscr)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    command_list = CommandList2()
    command_list.add(Command("list/python", "List all Python files in the current folder", "ls -lah *.py"))
    command_list.add(Command("home", "Print the home directory", "echo $HOME"))
    command_list.add(Command("Fancy echo", "See what it does!", "echo We live in $HOME and we\\\'re visiting $(pwd)"))
    command_list.add(Command("Hello world", "This is a test command", "echo Hello world!"))
    command_list.add(Command("cat", "dog", "bird"))

    # Draw the interface
    matches = command_list.fuzzy_find("")
    interface.draw(matches, command_list)
    # Main interface loop
    while True:
        # Query the possible actions
        matches = command_list.fuzzy_find(interface.input_str)


        # Read any keyboard input. Doesn't use buffering, which means we have to handle a lot of things manually,
        #   but we can also use special keys, and respond instantly to them.
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
        elif c == curses.KEY_UP:
            interface.selected += 1
        elif c == curses.KEY_DOWN:
            interface.selected -= 1
       
        if interface.selected >= min(len(matches), interface.const.list_max_num_lines):
            interface.selected = min(len(matches), interface.const.list_max_num_lines) - 1
        elif interface.selected < 0:
            interface.selected = 0

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


example_interfaces="""
    Natural language / freeform:
        move $0 to $1
    
        Pros: Looks nice, easy to use/understand
        Cons: Impossible to nest/combine/build up
    
    Defining functions:
        utils/move-file($0, $1)

        Pros: Easy to nest/combine/build up.  More familiar for coders, who are the most likely user
        Cons: A little hard to read.  But...the user can fuzzy search docstrings using natural language anyway

"""