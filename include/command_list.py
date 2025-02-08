from .command import Command

from collections import OrderedDict
from pathlib import Path
import pickle

class CommandList:
    def __init__(self, filename):
        self.commands = OrderedDict([])
        self.path = Path(filename)
        self.load()

    def load(self):
        print(self.path)
        if self.path.exists():
            with open(self.path, "rb") as handle:
                self.commands = pickle.load(handle)
        if len(self.commands) == 0:
            self.commands = OrderedDict([])
            self.add(Command("Fancy echo", "See what it does!", "echo We live in $HOME and we\\\'re visiting $(pwd)"))
            self.add(Command("Hello world", "This is a test command", "echo Hello world!"))
            self.add(Command("list files", "List all files in human readable format", "ls -lah"))
            self.add(Command("test", "Test expanding commands", "echo $mycmd"))
            self.add(Command("mycmd", "String for hello world", "\"hello world\""))
            self.add(Command("linecount", "Count the lines in a file", "wc -l"))
            self.add(Command("git/commits", "Succinct list of git commits", "git log --oneline --graph"))
            self.add(Command("git/stat", "Quick summary of local git changes", "git status && git diff --stat"))
            self.add(Command("size/all", "List file & folder sizes in the current folder", "du -sh -- * | $sort"))
            self.add(Command("size/folders", "List folder sizes in the current folder", "du -sh -- */ | $sort"))
            self.add(Command("sort", "Sort piped lines in decreasing order", "sort -rh"))


    def save(self):
        with open(self.path, "wb") as handle:
            pickle.dump(self.commands, handle)

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

    def add(self, command, save=True):
        """Add a new command."""
        self.commands[command.alias] = command
        if save:
            self.save()

    def remove(self, command, save=True):
        """Removes a command from the list."""
        self.commands.popitem(command.alias)
        if save:
            self.save()

    def __len__(self):
        return len(self.commands)
    
    def expand_command(self, input):
        """Process an input string by expanding any act.py commands.
        
            Ex:
            Input: $test
            Becomes: echo $mycmd
            Becomes: echo "hello world"

            And also resolves $test but not $testing, we need exact string match
        """
        idx = 0
        output = ""
        while idx < len(input):
            # Special `act` commands look like $alias or $alias(x, y, z)
            if input[idx] == "$":
                # Look for an exact alias match
                match = False
                for alias in self.commands:
                    if input[idx + 1: idx + len(alias) + 1] == alias:
                        match = True
                        break
                if match:
                    # Found a match!
                    command = self.commands[alias]
                    # Recursively expand the command, in case it contains further $alias commands
                    # TODO: Detect/prevent commands from referring to each other forever eternity!
                    output += self.expand_command(command.code)
                    idx += len(alias) + 1
                    continue
            output += input[idx]
            idx += 1
        return output