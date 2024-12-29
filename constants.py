import curses

command_list_filename = "commands.pkl"

class InterfaceConstants():
    def __init__(self):
        self.input_y = curses.LINES - 1
        self.input_x = 3
        self.input_prompt_str = "> "
        self.input_separator_y = self.input_y - 1
        self.input_separator_x = 2
        self.input_separator_len = curses.COLS - 4
        self.input_str_y = self.input_y
        self.input_str_x = self.input_x + len(self.input_prompt_str)
        self.input_str_w = curses.COLS - 2 * self.input_str_x
        self.list_max_num_lines = self.input_separator_y - 2 
        self.list_x = self.input_x
        self.list_last_y = self.input_separator_y - 1
        self.list_w = self.input_str_w
        self.num_cols = 3
        self.side_buf = 2
        self.col_sep = 1
        self.col_width = int((curses.COLS - 2 * self.side_buf) / self.num_cols) - self.col_sep * (self.num_cols - 1)

    def compute_dialogue_constants(self, lines, cols):
        self.dialogue_lines = lines
        self.dialogue_cols = cols
        self.topleft_x = max(0, int(curses.COLS / 2) - int(cols / 2))
        self.topleft_y = max(0, int(curses.LINES / 2) - int(lines / 2))