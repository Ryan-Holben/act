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
    1. Fuzzy search always searches after the last $, no matter what
        1. Pros:  Much simpler interface.  No weird casing for act and non-act $'s.
            1. Make it easier to understand by highlighting the user input text segment that's being fuzzy searched.
            1. Also: Highlight segments that will be replaced.  And/or, show the live view of the resolved result.
        2. Cons:  ??
3. If user types multiple $'s, we remove the first one, and then don't substitute any of it for an act command.  In this way, we prevent collisions with environmental variables.  For example:  if we define $USER in act, and the OS environment also has defined $USER, then an act command would include $$USER to access the OS's version of this environmental variable.  (Also, this is only necessary to do if that command happens to be defined within act.  Anything that doesn't resolve to an act command will be executed as-is.)


## Example interfaces

### Natural language / freeform:
    move $0 to $1

    Pros: Looks nice, easy to use/understand
    Cons: Impossible to nest/combine/build up
    


### Defining functions:
    utils/move-file($0, $1)

    Pros: Easy to nest/combine/build up.  More familiar for coders, who are the most likely user
    Cons: A little hard to read.  But...the user can fuzzy search docstrings using natural language anyway


# Example function arguments

$myfunc(filename, cat) <-- This is what it will look like in the alias only

In the actual code it would look like ---> doing some $0 stuff $1 with $0
So, the alias definition has the rules:
- Parens and commas let you put in variable names that are helpful to the user
- The actual code should just have $0, $1, $2 etc, to let the code refer to any other aliases