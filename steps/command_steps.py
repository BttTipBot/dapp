
# we register the last command step in the user's session
# and we use it to call the appropriate method in the fallback_handler
# based on the previous state
# this way we can handle the user's inputs and guide them through the process

from constants.command_steps import (
    STEP_KEYWORD
)

def is_in_steps(string):
    if STEP_KEYWORD in string:
        return True
    else:
        return False

def get_step(string):
    # Return how many steps are in the string
    return string.count(STEP_KEYWORD)

def get_arguments(string):
    # Return a list of string separated by the step separator
    return string.split(STEP_KEYWORD)

def add_step(command, step_name):
    # Add a step to the string
    return command + STEP_KEYWORD + step_name