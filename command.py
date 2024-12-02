def fuzzy_find(substring, string):
    """Do a fuzzy find for substring inside string.  Returns all indices corresponding
        to where inside string we first found substring.  If the entire substring isn't found,
        return an empty list of indices.
    """
    i = 0  # Index in substring
    j = 0  # Index in string
    indices = []

    while i < len(substring) and j < len(string):
        if substring[i].lower() == string[j].lower():
            indices.append(j)
            i += 1  # Move to the next character in substring
        j += 1  # Always move to the next character in string

    if i == len(substring):  # If all characters in substring were found
        return indices
    return []

class Command:
    def __init__(self, alias, doc, code):
        self.alias = alias
        self.doc = doc
        self.code = code

    def execute(self, **kwargs):
        # Need to recursively resolve any subcommands
        # Return error/success code, and/or text/stream output
        pass

    def test(self, **kwargs):
        """Do a dry run with some inputs and verify the output."""
        pass

    def fuzzy_find_and_score(self, substring):
        """Returns indices of matches in each field, as well as a total score to use for ordering.
            That score is None if no matches are found.
        """
        # Search all fields for substring
        searches = {}
        searches["alias"] = fuzzy_find(substring, self.alias)
        searches["doc"] = fuzzy_find(substring, self.doc)
        searches["code"] = fuzzy_find(substring, self.code)

        # For each, if the substring was found, produce a consecutivity score, otherwise score is None
        scores = []
        for key, val in searches:
            scores[key] = val[-1] - val[0] - len(substring) if len(val) == len(substring) else None
        
        # Pick the minimum score for the fields where we found a match.  Reasoning:  if we get a perfect match as an alias, but a bad
        #   match in the code for that item, this should still be a top recommended match.
        valid_scores = [s for s in scores if s is not None]
        total_score = min(valid_scores) if len(valid_scores) > 0 else None
        
        return searches, total_score
        