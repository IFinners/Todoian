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

    if main in ('ls','list'):
        if extra in ('a', 'all'):
            view_overdue()
            view_today()
            view_tomorrow()
            view_future()

        elif extra in ('o', 'overdue'):
            view_overdue()

        elif extra in ('t', 'today'):
            view_today()

        elif extra in ('tm', 'tomorrow'):
            view_tomorrow()

        elif extra in ('f', 'future'):
            view_future()

    elif main in ('a', 't', 'add'):
        add_task(command_regex.group(2))
        update_order()
        save_changes()

    elif main in ('d', 'del', 'delete'):
        delete_task(extra)
        update_order()
        save_changes()

    elif main in ('e', 'edit'):
        edit_attribute(extra, 'title')
    
    elif main in ('ed', 'edit-date'):
        edit_attribute(extra, 'date')

    elif main in ('er', 'edit-repeat'):
        edit_attribute(extra, 'repeat')

    elif main in ('et', 'edit_tags'):
        edit_attribute(extra, 'tags')

    elif main in ('h', 'help'):
        print("  HELP HERE")

    else:
        print("  Command Not Recognised - Try Again or "
              "Enter 'h' For Usage Instructions.")


# DISPLAY FUNCTIONS

def view_overdue():
    """Print all tasks that are overdue."""
    print()
    print('  ' + FONT_DICT['red'] + "OVERDUE TASKS" + FONT_DICT['end'], end='\n\n')
    empty = True
    for task in cl.Task.tasks:
        if task.date < current_date:
            over = ((current_datetime
                     - dt.strptime(task.date, '%Y-%m-%d')).days)
            if over == 1:
                print(task, "[Due Yesterday]")
            else:
                print(task, "[Due {} Days Ago]".format(over))
            # Check for Subtasks
            if task.subs:
                # print_sub(int(task[0] - 1), cl.Task.tasks)
                pass
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_today():
    """Print all tasks due today."""
    print()
    print('  ' + FONT_DICT['green'] + "TODAY'S TASKS" + FONT_DICT['end'], end='\n\n')
    empty = True

    for task in cl.Task.tasks:
        if task.date == current_date:
            print(task)
            # Check for Subtasks
            if task.subs:
                # print_sub(int(task[0] - 1), cl.Task.tasks)
                pass
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_tomorrow():
    """Print all tasks that are due tomorrow."""
    print()
    print('  ' + FONT_DICT['orange'] + "TOMORROW'S TASKS" + FONT_DICT['end'], end='\n\n')
    empty = True
    for task in cl.Task.tasks:
        if ((dt.strptime(task.date, '%Y-%m-%d') - current_datetime).days) == 1:
            print(task)
            # Check for Subtasks
            if task.subs:
                pass
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_future():
    """Print all tasks with due dates beyond tomorrow"""
    print()
    print('  ' + FONT_DICT['blue'] + "FUTURE TASKS" + FONT_DICT['end'], end='\n\n')
    empty = True
    for task in cl.Task.tasks:
        if task.date > current_date:
            until = ((dt.strptime(task.date, '%Y-%m-%d')
                          - current_datetime).days)
            if until > 1:
                print(task, "[Due in {} Days]".format(until))
            # Check for Subtasks
                if task.subs:
                    # print_sub(int(task[0] - 1), task_data)
                    pass
                empty = False
    if empty:
        print("    No Tasks Found")
    print()

# Task Functions

def add_task(extra):
    """Add a new task to the task list."""
    add_regex = re.search(r'^"(.*)"\s?(\S*)?\s?(.*)?', extra)
    task = add_regex.group(1)
    opt_date = add_regex.group(2)
    opt_repeat = add_regex.group(3)
    if not opt_date:
        opt_date = current_date
    if not opt_repeat:
        opt_repeat = None
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
        del cl.Task.tasks[int(extra) - 1]


def edit_attribute(extra, attr):
    """."""
    attr_method = {
        'title': cl.Task.tasks[int(extra) - 1].edit_title,
        'date': cl.Task.tasks[int(extra) - 1].edit_date,
        'repeat': cl.Task.tasks[int(extra) - 1].edit_repeat,
        'tags': cl.Task.tasks[int(extra) - 1].add_tag,
        }
    attr_method[attr]()


def update_order():
    """Update the numbering of the Tasks."""
    cl.Task.tasks.sort(key=lambda x: x.date)
    for num, task in enumerate(cl.Task.tasks, 1):
        task.num = num


def save_changes():
    """Write changes to data file."""
    with open ('data.pickle', 'wb') as fp:
        pickle.dump(cl.Task.tasks, fp)











if __name__ == '__main__':

    # A dictionary of ANSI escapse sequences for font effects.
    FONT_DICT = {
   'blue':  '\033[4;94m',
   'green':  '\033[4;92m',
   'green no u':  '\033[1;92m',
   'orange': '\033[4;93m',
   'red':  '\033[4;91m',
   'red no u':  '\033[1;91m',
   'magenta':  '\033[4;95m',
   'end':  '\033[0m',
}

    try:
        with open('data.pickle', 'rb') as fp:
            cl.Task.tasks = pickle.load(fp)
    except:
        pass


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
