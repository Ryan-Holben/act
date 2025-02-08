from .dialogue_box import DialogueBox
import curses

class MenuInterface(DialogueBox):
    def draw_internal(self):
        self.win.addstr(2, 10, "S - Save current command", curses.A_BOLD)
        self.win.addstr(4, 10, "D - Delete current command", curses.A_BOLD)
        self.win.addstr(6, 10, "Q - Quit", curses.A_BOLD)