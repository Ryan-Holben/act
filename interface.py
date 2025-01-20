import curses
import curses.panel

from command_list import CommandList
import constants

class Interface():
    def __init__(self, stdscr, command_list):
        self.screen = stdscr
        self.initialize_window()
        self.compute_constants()
        self.input_str = ""
        self.search_str = ""
        self.search_str_idx = len(self.search_str)
        self.selected = 0

        # Initialize the command list & fuzzy search on an empty string
        self.command_list = command_list
        self.matches = self.command_list.fuzzy_find("")
        

    def compute_constants(self):
        self.const = constants.InterfaceConstants()

    def initialize_window(self):
        """Internal function to manage a window object.  Behavior is better using this for drawing & getch,
            rather than working directly with the screen object.  We also initialize a panel abstraction.
            This helps with stacking windows and managing drawing in a simpler way."""
        self.win = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        self.panel = curses.panel.new_panel(self.win)
        self.win.keypad(True)
    
    def get_search_string_and_idx(self):
        for i in range(len(self.input_str)-1, -1, -1):
            if self.input_str[i] == "$":
                return self.input_str[i+1:], i + 1
        return "", len(self.input_str)

    def process_input(self, c):
        if c >= 32 and c < 127:                       # Standard text input
            if len(self.input_str) < self.const.input_str_w - 1:
                self.input_str += chr(c)
        elif c == 127 and len(self.input_str) > 0:    # Delete key
            self.input_str = self.input_str[:-1]
        elif c == ord("\t"):                          # Tab autocompletes using the selected command
            self.input_str = self.input_str[:self.search_str_idx] + self.matches[self.selected][0].alias
            self.selected = 0
        elif c == curses.KEY_UP:
            self.selected += 1
        elif c == curses.KEY_DOWN:
            self.selected -= 1

        # Ensure we are fuzzy searching the correct part of the input string
        self.search_str, self.search_str_idx = self.get_search_string_and_idx()
        
        # Update the matches
        self.matches = self.command_list.fuzzy_find(self.search_str)

        # Ensure the selected command remains in the set of displayed matches
        if self.selected >= min(len(self.matches), self.const.list_max_num_lines):
            self.selected = min(len(self.matches), self.const.list_max_num_lines) - 1
        elif self.selected < 0:
            self.selected = 0

        

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
    
    def draw(self):
        # Setup constants
        self.compute_constants()

        # Erase the window, draw borders
        self.win.clear()
        self.win.border(0, 0, 0, ' ', 0, 0, curses.ACS_VLINE, curses.ACS_VLINE)
        self.win.hline(self.const.input_separator_y, self.const.input_separator_x, curses.ACS_HLINE, self.const.input_separator_len)

        # Various bits of information shown on the border
        self.display_version()
        self.display_num_commands()

        # Display the prompt string
        self.win.addstr(self.const.input_y, self.const.input_x, self.const.input_prompt_str)
        self.win.addstr(self.const.input_str_y, self.const.input_str_x, self.input_str[:self.search_str_idx])
        self.win.addstr(self.const.input_str_y,
                        self.const.input_str_x + self.search_str_idx,
                        self.input_str[self.search_str_idx:],
                        curses.A_UNDERLINE | curses.color_pair(2))

        # Display commands that fuzzy-match the $search command
        if self.matches:
            if len(self.matches) > 0 and self.input_str == self.matches[self.selected][0].alias:
                run_str = "Press enter to run"
                self.win.addstr(self.const.input_str_y, curses.COLS - len(run_str) - 10, run_str, curses.A_STANDOUT)
            
            filtered = self.matches[:self.const.list_max_num_lines]
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

    def resize(self):
        """Call this when we detect the terminal was resized."""
        self.compute_constants()
        self.initialize_window()

    # def display_terminal_size(self):
    #     self.win.addstr(0, 0, f"cols: {curses.COLS}, lines: {curses.LINES}")

    def display_num_commands(self):
        self.win.addstr(0, 20, f" Displaying {len(self.matches)} / {len(self.command_list)} commands ")

    def display_version(self):
        self.win.addstr(0, 2, " act v.0.1 ", curses.color_pair(1) | curses.A_BOLD)
    
    def getch(self):
        return self.win.getch()