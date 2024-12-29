from dialogue_box import DialogueBox

class MenuInterface(DialogueBox):
    def draw(self):
        self.win.border()
        self.win.addstr(0, 2, " Command Menu ")
        self.win.addstr(2, 10, "S - Save current command")
        self.win.addstr(4, 10, "D - Delete current command")
        