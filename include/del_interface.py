from .dialogue_box import DialogueBox
import curses

class DeleteInterface(DialogueBox):
    def set_command_str(self, command_str):
        self.command_str = command_str

    def draw_internal(self):
        self.addstr(2, 10, "Press Enter to delete the following command:")
        self.addstr(4, 15, self.command_str, curses.A_BOLD)
        