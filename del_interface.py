from dialogue_box import DialogueBox

class DeleteInterface(DialogueBox):
    def draw(self):
        self.win.border()
        self.win.addstr(0, 2, " Delete Command ")
        self.win.addstr(2, 10, "Enter - Delete current command")
        self.win.addstr(4, 10, "Esc - Cancel")
        