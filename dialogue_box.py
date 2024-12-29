import curses
from constants import InterfaceConstants

class DialogueBox():
    """Generic dialogue box.  Intended for subclassing."""
    def __init__(self, stdscr):
        self.screen = stdscr
        self.initialize_window()
        self.compute_constants()
        self.hide()
    
    def resize(self):
        """Call this when we detect the terminal was resized."""
        self.compute_constants()        # First, compute dimensions
        self.initialize_window()        # Second, remake the window with those dimensions

    def compute_constants(self):
        """Recompute constants related to the the dialogue box's dimensions."""
        self.const = InterfaceConstants(self.win)

    def initialize_window(self):
        """Internal function to manage a window object.  Behavior is better using this for drawing & getch,
            rather than working directly with the screen object.  We also initialize a panel abstraction.
            This helps with stacking windows and managing drawing in a simpler way."""
        BUF = 10
        HBUF = int(BUF/2)
        self.win = curses.newwin(curses.LINES - BUF, curses.COLS - BUF, HBUF, HBUF)
        self.panel = curses.panel.new_panel(self.win)
        self.win.keypad(True)

    def hide(self):
        """Makes the window invisible."""
        self.panel.hide()

    def show(self):
        """Make the window visible and put it on top of the panel stack."""
        self.resize()
        self.panel.show()
        self.panel.top()
    
    def draw(self):
        """Main function to override."""
        pass