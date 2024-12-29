import curses
from constants import InterfaceConstants

class DialogueBox():
    """Generic dialogue box.  Intended for subclassing."""
    def __init__(self, stdscr, title, lines=None, cols=None):
        self.screen = stdscr
        self.title = title
        self.lines = lines if lines else curses.LINES
        self.cols = cols if cols else curses.COLS
        self.compute_constants()
        self.initialize_window()
        
        self.hide()
    
    def resize(self):
        """Call this when we detect the terminal was resized."""
        self.compute_constants()        # First, compute dimensions
        self.initialize_window()        # Second, remake the window with those dimensions

    def compute_constants(self):
        """Recompute constants related to the the dialogue box's dimensions."""
        self.const = InterfaceConstants()
        self.const.compute_dialogue_constants(self.lines, self.cols)

    def initialize_window(self):
        """Internal function to manage a window object.  Behavior is better using this for drawing & getch,
            rather than working directly with the screen object.  We also initialize a panel abstraction.
            This helps with stacking windows and managing drawing in a simpler way."""
        self.win = curses.newwin(self.lines, self.cols, self.const.topleft_y, self.const.topleft_x)
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
    
    def addstr(self, line, col, string, attrs=None):
        """Writes text, ensuring it stays clipped and doesn't exceed the window borders."""
        if line < 0 or col < 0 or line >= self.lines or col >= self.cols:
            return
        limit = max(0, self.cols - col - 1)
        if attrs:
            self.win.addstr(line, col, string[:limit], attrs)
        else:
            self.win.addstr(line, col, string[:limit])
        
    def draw(self):
        """User should call this function to draw the window."""
        self.win.attron(curses.color_pair(1))
        self.win.border()
        self.win.attroff(curses.color_pair(1))
        self.win.addstr(0, 2, "[" + self.title + "]", curses.A_BOLD)
        self.win.addstr(self.const.dialogue_lines - 1, 2, " ESC to go back ", curses.A_REVERSE)
        self.draw_internal()
    
    def draw_internal(self):
        """Main function to override."""
        pass
