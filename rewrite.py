#!/usr/bin/env python3

import classes as cl

import re
import pickle
from datetime import datetime as dt
from datetime import timedelta


def decide_action(command):
    """Decide on the actions and function calls the command requires."""
    command_regex = re.search(r'^([-\w]*)\s?(.*)', command)
    main = command_regex.group(1).lower()
    extra = command_regex.group(2).lower()


    if main in ('a', 't' 'add'):
        add_task(extra)

    elif main in ('d', 'del', 'delete'):
        delete_task(extra)

    elif main in ('h', 'help'):
        print("  HELP HERE")

    elif main in ('s', 'save'):
        save_changes()

    else:
        print("  Command Not Recognised - Try Again or "
              "Enter 'h' For Usage Instructions.")





def add_task(extra):
    """Add a new task to the task list."""
    add_regex = re.search(r'^"(.*)"\s?(\S*)?\s?(.*)?', extra)
    task = add_regex.group(1)
    opt_date = add_regex.group(2)
    opt_repeat = add_regex.group(3)
    cl.Task(task, opt_date, opt_repeat)


def delete_task(extra):
    """."""
    if extra in ("all", 'a'):
        check = cl.get_input("  This Will Delete All Task Data. Are You Sure "
                        "You Want to Continue? (y/n): ", one_line=True)
        if check.lower() in ('y', 'yes'):
            cl.Task.tasks.clear()
        else:
            print("  Removal of All Tasks Aborted.")
    else:
        del cl.Task.tasks[int(extra)]


def save_changes():
    """Write changes to data file."""
    with open ('data.pickle', 'wb') as fp:
        pickle.dump(cl.Task.tasks, fp)











if __name__ == '__main__':
    
    try:
        with open('data.pickle', 'rb') as fp:
            cl.Task.tasks = pickle.load(fp)
    except:
        pass

    for task in cl.Task.tasks:
        print(task.description)

    # Cache Lists
    deleted_tasks = []
    completed_tasks = []
    deleted_goals = []
    completed_goals = []

    # Formatted then stripped to set unwanted hours etc to blank for comparisons
    current_date = dt.now().strftime('%Y-%m-%d')
    current_datetime = dt.strptime(current_date, '%Y-%m-%d')


    while True:
        print()
        action = cl.get_input("  ENTER COMMAND ('q' to quit): ", one_line=True)
        print()
        if action.lower() == "q":
            break
        else:
            decide_action(action)
