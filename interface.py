import curses

from constants import InterfaceConstants

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
    
    def draw(self, matches, command_list, state):
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

        self.draw_state(state)

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
    
    def draw_state(self, state):
        state_str = str(state)
        self.win.addstr(3, 1, state_str)