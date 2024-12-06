from command import Command
from collections import OrderedDict

class CommandList2:
    def __init__(self):
        self.commands = OrderedDict([])

    def load(self):
        pass

    def save(self):
        pass

    def fuzzy_find(self, search_string):
        """Input a string, return a list of all commands containing the string as a substring, ordered by something like
        most consecutive letters, tiebreakers by normal string ordering, or most recent, or something."""

        if search_string is None or len(search_string) == 0:
            return [[cmd, {}, None] for cmd in self.commands.values()]

        output = []
        for alias, cmd in self.commands.items():
            indices, score = cmd.fuzzy_find_and_score(search_string)
            if score is not None:
                output.append([cmd, indices, score])
                
        # Order the input by consecutivity score & return it
        return sorted(output, key=lambda x: x[2])

    def add(self, command):
        """Add a new command."""
        self.commands[command.alias] = command

    def remove(self, command):
        """Removes a command from the list."""
        self.commands.popitem(command.alias)

    def __len__(self):
        return len(self.commands)