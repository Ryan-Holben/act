#!/bin/bash

# TODO:  Add an installation script to run "act" from anywhere:
# - Makes this script have executable permissions (not necessary, but people like that)
# - Export to ~/.zshrc and whatever else people use:
# act() {
#    /Users/ryan/Documents/dev/act/act.sh $* <-- Some install location
# }
# - Run:  source ~/.zshrc


# Note where the user called the command from, and where this script is installed
CALLING_PATH=$(pwd)
SCRIPT_PATH=$(dirname $0)
ACT_OUTPUT_PATH="${SCRIPT_PATH}/data/act_output.txt"

# cd to script location to make Python imports and file IO work correctly
# then cd back to the calling location.  (The user will expect to run commands
# at the calling location, not the script location.)
cd $SCRIPT_PATH
python3 act.py $*
exit_code=$?
cd $CALLING_PATH

# If the user chose a command to run in act.py, the final resolved command
# will be in the following temporary file.  If that file exists, run the 
# command and then clean up the temporary file.
if [ "$exit_code" -eq 255 ]; then
    if [ -f $ACT_OUTPUT_PATH ]; then
        bash $ACT_OUTPUT_PATH
    fi
fi