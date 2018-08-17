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
    extra = command_regex.group(2)

    if main in ('ls','list'):
        if extra in ('a', 'all'):
            view_overdue()
            view_today()
            view_tomorrow()
            view_future()

        elif extra.lower() in ('o', 'overdue'):
            view_overdue()

        elif extra.lower() in ('t', 'today'):
            view_today()

        elif extra.lower() in ('tm', 'tomorrow'):
            view_tomorrow()

        elif extra.lower() in ('f', 'future'):
            view_future()

    elif main in ('a', 'add'):
        add_task(command_regex.group(2))
        update_order()
        save_changes()

    elif main in ('d', 'del', 'delete'):
        delete_task(extra)
        update_order()
        save_changes()
    
    elif main in ('c', 'comp', 'complete'):
        complete_task(extra)
        update_order()
        save_changes()

    elif main in ('e', 'edit'):
        method_dist(extra, 'title')

    elif main in ('d', 'date'):
        method_dist(extra, 'date')

    elif main in ('r', 'repeat'):
        method_dist(extra, 'repeat')

    elif main in ('t', 'tag'):
        method_dist(extra, 'tag')

    elif main in ('dt', 'delete_tags'):
        method_dist(extra, 'tag-del')

    elif main in ('s', 'sub'):
        method_dist(extra, 'sub')

    elif main in ('ds', 'delete-sub'):
        method_dist(extra, 'sub-del')

    elif main in ('es', 'edit-sub'):
        method_dist(extra, 'sub-title')

    elif main in ('ts', 'toggle-sub'):
        method_dist(extra, 'sub-tog')

    elif main in ('ud', 'undo-del'):
        cache_retrival(deleted_tasks)
        update_order()

    elif main in ('vt', 'view-tag'):
        view_tag(extra)

    elif main in ('vat', 'view-all-tags'):
        view_tags()

    elif main in ('h', 'help'):
        print("  Full Documentation can be found at: "
              "https://todoian.readthedocs.io/en/latest/")

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
                print(task, "[Due Yesterday]", end='\n\n')
            else:
                print(task, "[Due {} Days Ago]".format(over))
            # Check for Subtasks
            if task.subs:
                for sub in task.subs:
                    print(sub)
                print()
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
            print(task, end='\n\n')
            # Check for Subtasks
            if task.subs:
                for sub in task.subs:
                    print(sub)
                print()
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
            print(task, end='\n\n')
            # Check for Subtasks
            if task.subs:
                for sub in task.subs:
                    print(sub)
                print()
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
                print(task, "[Due in {} Days]".format(until), end='\n\n')
            # Check for Subtasks
            if task.subs:
                for sub in task.subs:
                    print(sub)
                print()
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_tag(tag):
    """Display all Tasks with a specified tag."""
    print('  ' + FONT_DICT['green'] + "TASKS TAGGED WITH "
          + tag.upper() + FONT_DICT['end'], end='\n\n')
    for task in cl.Task.tasks:
        if tag.lower() in [tag.lower() for tag in task.tags]:
            print("    {}| {} ({})".format(task.num, task.title, task.date))
    print()


def view_tags():
    """Display all tasks with their tags."""
    print('  ' + FONT_DICT['green'] + "TASKS AND THEIR TAGS" + FONT_DICT['end'], end='\n\n')
    for task in cl.Task.tasks:
        print(task)
        print("        {}".format(tuple(sorted(task.tags))), end='\n\n')


# Task Functions

def add_task(extra):
    """Add a new task to the task list with optional attributes."""
    task = extra
    opt_date = current_date
    opt_repeat = None
    opt_tags = None
    if '~~' in extra:
        task, attributes = extra.split(' ~~')
        date_regex = re.search(r'(?:d|date)=(\S+)', attributes)
        rep_regex = re.search(r'(?:r|rep|repeat)=(\S+)', attributes)
        tag_regex = re.search(r'(?:t|tag)=(\S+)', attributes)
        if date_regex:
            opt_date = date_regex.group(1)
        if rep_regex:
            opt_repeat = int(rep_regex.group(1))
        if tag_regex:
            if ',' in tag_regex.group(1):
                opt_tags = tag_regex.group(1).split(',')
            else:
                opt_tags = [tag_regex.group(1)]
    cl.Task(task, opt_date, opt_repeat, opt_tags)


def delete_task(extra):
    """Delete a task, or all tasks if specified."""
    if extra in ("all", 'a'):
        check = cl.get_input("  This Will Delete All Task Data. Are You Sure "
                        "You Want to Continue? (y/n): ", one_line=True)
        if check.lower() in ('y', 'yes'):
            deleted_tasks.extend(cl.Task.tasks)
            cl.Task.tasks.clear()
        else:
            print("  Removal of All Tasks Aborted.")
    else:
        deleted_tasks.append(cl.Task.tasks.pop(int(extra) - 1))


def complete_task(extra):
    """Mark a task as complete and move it to the completed_tasks cache."""
    task_num = int(extra) - 1
    repeat = cl.Task.tasks[task_num].repeat
    if repeat:
        cl.Task.tasks[task_num].do_repeat()
    else:
        completed_tasks.append(cl.Task.tasks.pop(task_num))


def cache_retrival(target):
    """Retrive item from a cache list (LIFO)."""
    data_list = target
    cl.Task.tasks.append(data_list.pop())


def method_dist(extra, key):
    """Convert a key into a function call through a distribution dictionary."""
    parse_regex = re.search(r'^(\d+)\s?(.*)?', extra)
    num = int(parse_regex.group(1))
    new_value = parse_regex.group(2)
    key_method = {
        'title': cl.Task.tasks[num - 1].edit_title,
        'date': cl.Task.tasks[num - 1].edit_date,
        'repeat': cl.Task.tasks[num - 1].edit_repeat,
        'tag': cl.Task.tasks[num - 1].add_tag,
        'tag-del': cl.Task.tasks[num - 1].remove_tag,
        'sub': cl.Task.tasks[num - 1].add_sub,
        'sub-title': cl.Task.tasks[num - 1].edit_sub,
        'sub-del': cl.Task.tasks[num - 1].remove_sub,
        'sub-tog': cl.Task.tasks[num - 1].toggle_sub,
        }

    key_method[key](new_value)
    save_changes()


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
        action = cl.get_input("ENTER COMMAND ('q' to quit): ", one_line=True)
        print()
        if action.lower() == "q":
            break

        else:
            try:
                decide_action(action)

            except IndexError:
                print()
                input("  No Item Found at That Position in the List or Cache - "
                    "Try Again or Enter 'h' for Usage Instructions.")
                print()

            except ValueError:
                print()
                input("  Did You Forget A Number For The Item/Subitem in Your Command? - "
                    "Try Again or Enter 'h' for Usage Instructions.")
                print()

else:
    # For unittest purposes - Look for better option
    current_date = dt.now().strftime('%Y-%m-%d')
    current_datetime = dt.strptime(current_date, '%Y-%m-%d')
    deleted_tasks = []
    completed_tasks = []
