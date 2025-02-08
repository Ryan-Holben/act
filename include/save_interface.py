from .dialogue_box import DialogueBox

class SaveInterface(DialogueBox):
    def draw_internal(self):
        self.addstr(2, 10, "Enter - Input and save alias & docstring for current command")