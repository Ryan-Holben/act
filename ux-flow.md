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


## Example interfaces

### Natural language / freeform:
    move $0 to $1

    Pros: Looks nice, easy to use/understand
    Cons: Impossible to nest/combine/build up
    


### Defining functions:
    utils/move-file($0, $1)

    Pros: Easy to nest/combine/build up.  More familiar for coders, who are the most likely user
    Cons: A little hard to read.  But...the user can fuzzy search docstrings using natural language anyway