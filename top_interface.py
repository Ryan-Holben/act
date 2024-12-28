import curses

from interface import Interface


def match(state, *match_list):
    """Check if match_list is an initial segment of state."""
    return len(state) >= len(match_list) and state[:len(match_list)] == list(match_list)

class TopInterface():
    """Class that manages all UI panels, all state around where the user is inside the UI, etc."""
    def __init__(self, stdscr):
        # Store screen reference
        self.stdscr = stdscr

        # Set up interface subclasses to manage
        self.interface_search = Interface(self.stdscr)
        self.menu = None

        # Set up UI state to manage
        self.state = ["main"]

    def check_for_resize(self, c):
        """Check for a special key that indicates the terminal was resized, and then
            recompute interfaces."""
        if c == curses.KEY_RESIZE:
            self.resize_all()

    def resize_all(self):
        """Call this when we know the terminal has been resized.  This recomputes all UI
            dimension constants, and re-initializes all windows & panels."""
        curses.resizeterm(*self.stdscr.getmaxyx())
        self.interface_search.resize()
    
    def draw_all(self, command_list, matches):
        """Draw all windows/panels."""
        self.interface_search.draw(matches, command_list, self.state)
        curses.panel.update_panels()
        curses.doupdate()

    def process_input(self, c):
        if match(self.state, "main"):
            if c == 27:
                self.state = ["menu"]
            else:
                pass # Call main interface here
        elif match(self.state, "menu"):
            if len(self.state) == 1:
                if c == 27:
                    self.state = ["quit"]
                elif c == ord("s"):
                    self.state.append("save")
                elif c == ord("d"):
                    self.state.append("delete")
            else:
                if match(self.state, "menu", "save"):
                    if c == 27:
                        self.state.pop()
                elif match(self.state, "menu", "delete"):
                    if c == 27:
                        self.state.pop()

    def getch(self):
        # TODO: REPLACE THIS FUNCTION, it currently pulls from one specific interface
        #        this probably isn't good
        return self.interface_search.getch()
    
    def running(self):
        return len(self.state) > 0 and self.state[0] != "quit"

    