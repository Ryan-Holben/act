import curses
from constants import InterfaceConstants

class Menu():
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
            rather than working directly with the screen object.  We also initialize a panel abstraction.
            This helps with stacking windows and managing drawing in a simpler way."""
        self.win = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        self.panel = curses.panel.new_panel(self.win)
        self.win.keypad(True)

    def draw(self):
        pass