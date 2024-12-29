from dialogue_box import DialogueBox

class SaveInterface(DialogueBox):
    def draw(self):
        self.win.border()
        self.win.addstr(0, 2, " Save Command ")
        self.win.addstr(2, 10, "Enter - Input and save alias & docstring for current command")
        self.win.addstr(4, 10, "Esc - Cancel")