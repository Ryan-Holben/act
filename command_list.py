from command import Command

class CommandList:
    def __init__(self):
        self.lines = []

    def load(self):
        pass

    def save(self):
        pass

    def fuzzy_find(self, string):
        """Input a string, return a list of all commands containing the string as a substring, ordered by something like
        most consecutive letters, tiebreakers by normal string ordering, or most recent, or something."""

        # Algorithm idea:
        # - Search for string (disjointed is allowed)
        # - Add a score equalling (max_idx - min_idx) - strlen <-- 0 = exact match, higher = spread out
            # - To be thorough, would have to do this for ALL submatches and pick the best
        # - Add a score for total command string length (favor shorter commands)
        # - Add a score for most recently used

        output = []
        for item in self.lines:
            i = 0  # Index for 'string'
            j = 0  # Index for 'item'
            indices = []

            while i < len(string) and j < len(item):
                if string[i].lower() == item[j].lower():
                    indices.append(j)
                    i += 1  # Move to the next character in 'sub'
                j += 1  # Always move to the next character in 'string'

            if i == len(string):  # If all characters in 'sub' were found
                output.append([item, indices])
                
        # Order the input by consecutivity score & return it
        return sorted(output, key=lambda x: x[1][-1]-x[1][0]-len(string) if len(x[1]) > 1 else 0)

    def add(self, command):
        """Add a new command."""
        self.lines.append(command)

    def remove(self, command):
        """Removes a command from the list."""

    def __len__(self):
        return len(self.lines)