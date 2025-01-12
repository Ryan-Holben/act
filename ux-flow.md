# UX Flow

Just start typing.

Whenever you type $, it opens a search bar.  Typing focus moves to that.
    When you press TAB/ESC it completes the search or cancels it.
    If it's one of our functions, it will remain colored, indicating the $command will be expanded

Press ENTER to quit & run the command

Press ESC to bring up menu
- ESC again to quit
- S to save the command (brings up prompts to name it and write a docstring)
- D to delete the selected command

## Example user stories
1. "Type $ to find a command"
2. User types $, which brings up command list
3. As user continues to type, what they type after the most recent $ gets fuzzy searched
    1. If they press up or down, the text doesn't change, but highlight does.
    2. If they press TAB, replace text after the last $ with the highlighted item's alias and (
    3. It now exits fuzzy search mode.  So they can now insert variables or whatever.  Up to them to close the ).
    4. => So this means we're in fuzzy search mode whenever we're between $ and (
    5. But then how do they input non-act $'s?
4. Alternative design:
    1. Fuzzy search always searches after the last $, no matter what
        1. Pros:  Much simpler interface.  No weird casing for act and non-act $'s.
            1. Make it easier to understand by highlighting the user input text segment that's being fuzzy searched.
            1. Also: Highlight segments that will be replaced.  And/or, show the live view of the resolved result.
        2. Cons:  ??


## Example interfaces

### Natural language / freeform:
    move $0 to $1

    Pros: Looks nice, easy to use/understand
    Cons: Impossible to nest/combine/build up
    


### Defining functions:
    utils/move-file($0, $1)

    Pros: Easy to nest/combine/build up.  More familiar for coders, who are the most likely user
    Cons: A little hard to read.  But...the user can fuzzy search docstrings using natural language anyway