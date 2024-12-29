import curses

from interface import Interface
from menu_interface import MenuInterface
from del_interface import DeleteInterface
from save_interface import SaveInterface

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
        self.menu = MenuInterface(self.stdscr)
        self.save_interface = SaveInterface(self.stdscr)
        self.delete_interface = DeleteInterface(self.stdscr)

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
        if self.state[-1] == "menu":
            self.menu.resize()
        elif self.state[-1] == "save":
            self.save_interface.resize()
        elif self.state[-1] == "delete":
            self.delete_interface.resize()

    def change_state(self, new_state):
        # If the previous state has a dialogue box, hide it
        if self.state[-1] == "menu":
            self.menu.hide()
        elif self.state[-1] == "save":
            self.save_interface.hide()
        elif self.state[-1] == "delete":
            self.delete_interface.hide()

        # Swap in the new state
        self.state = new_state

        # If the new state has a dialogue box, show it & place it on top
        if self.state[-1] == "menu":
            self.menu.show()
        elif self.state[-1] == "save":
            self.save_interface.show()
        elif self.state[-1] == "delete":
            self.delete_interface.show()
    
    def draw_all(self, command_list, matches):
        """Draw all windows/panels."""
        # Always draw the search interface as a base.  Other menus draw on top of it.
        self.interface_search.draw(matches, command_list, self.state)

        # Use our state to determine which menu class to draw
        if match(self.state, "menu"):
            if len(self.state) == 1:
                self.menu.draw()
            else:
                if match(self.state, "menu", "save"):
                    self.save_interface.draw()
                elif match(self.state, "menu", "delete"):    
                    self.delete_interface.draw()

        curses.panel.update_panels()
        curses.doupdate()

    def process_input(self, c):
        if match(self.state, "main"):
            if c == 27:
                self.change_state(["menu"])
            else:
                pass # Call main interface here
        elif match(self.state, "menu"):
            if len(self.state) == 1:
                if c == 27:
                    self.change_state(["quit"])
                elif c == ord("s"):
                    self.change_state(self.state + ["save"])
                elif c == ord("d"):
                    self.change_state(self.state + ["delete"])
            else:
                if match(self.state, "menu", "save"):
                    if c == 27:
                        self.change_state(self.state[:-1])
                elif match(self.state, "menu", "delete"):
                    if c == 27:
                        self.change_state(self.state[:-1])

    def getch(self):
        # TODO: REPLACE THIS FUNCTION, it currently pulls from one specific interface
        #        this probably isn't good
        return self.interface_search.getch()
    
    def running(self):
        return len(self.state) > 0 and self.state[0] != "quit"

    