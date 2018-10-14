#!/usr/bin/env python3

"""A command based todo list that displays in the terminal."""

from datetime import datetime as dt
from datetime import timedelta
import pickle
import re

import classes as cl


def decide_action(command):
    """Decide on the actions and function calls command requires."""
    current_date = dt.now()

    command_regex = re.search(r'^([-\w]*)\s?(.*)', command)
    main = command_regex.group(1).lower()
    extra = command_regex.group(2)

    if main in ('ls', 'list'):
        list_displays(extra, current_date)

    elif main in ('a', 't', 'add', 'task'):
        add_task(command_regex.group(2), current_date)
        update_order()
        save_changes()
        decide_action('ls a')

    elif main in ('ga', 'g', 'add-goal', 'goal'):
        add_goal(command_regex.group(2))
        update_order()
        save_changes()
        decide_action('ls g')

    elif main in ('d', 'del', 'delete'):
        delete_task(extra, deleted['tasks'])
        update_order()
        save_changes()
        decide_action('ls a')

    elif main in ('c', 'comp', 'complete'):
        if extra in ('o', 'over', 'overdue'):
            complete_overdue(current_date, completed['tasks'])
        elif extra in ('t', 'today'):
            complete_today(current_date, completed['tasks'])
        else:
            complete_task(extra, completed['tasks'])
            update_order()
        save_changes()
        decide_action('ls a')

    elif main in ('gd', 'goal-delete'):
        delete_goal(extra, deleted['goals'])
        update_order()
        save_changes()
        decide_action('ls g')

    elif main in ('m', 'move'):
        move_item(extra, cl.Task.tasks)
        update_order()
        save_changes()
        decide_action('ls a')

    elif main in ('ms', 'move-sub'):
        move_item(extra, cl.Task.tasks)
        save_changes()
        decide_action('ls a')

    elif main in ('gm', 'goal-move'):
        move_item(extra, cl.Goal.goals)
        update_order()
        save_changes()
        decide_action('ls g')

    elif main in ('gms', 'goal-move-sub'):
        move_item(extra, cl.Goal.goals)
        save_changes()
        decide_action('ls gs')

    elif main in ('gc', 'goal-comp', 'goal-complete'):
        complete_goal(extra, completed['goals'])
        update_order()
        save_changes()
        decide_action('ls g')

    elif main in ('e', 'edit'):
        task_dist(extra, 'title')
        decide_action('ls a')

    elif main in ('ed', 'edit-date'):
        task_dist(extra, 'date')
        update_order()
        decide_action('ls a')

    elif main in ('r', 'repeat'):
        task_dist(extra, 'repeat')

    elif main in ('tg', 'tag'):
        task_dist(extra, 'tag')

    elif main in ('dt', 'delete_tag'):
        task_dist(extra, 'del-tag')

    elif main in ('s', 'sub'):
        task_dist(extra, 'sub')
        decide_action('ls a')

    elif main in ('ds', 'delete-sub'):
        task_dist(extra, 'sub-del')
        decide_action('ls a')

    elif main in ('es', 'edit-sub'):
        task_dist(extra, 'sub-title')
        decide_action('ls a')

    elif main in ('ts', 'toggle-sub'):
        task_dist(extra, 'sub-tog')
        decide_action('ls a')

    elif main in ('ge', 'goal-edit'):
        goal_dist(extra, 'title')
        decide_action('ls g')

    elif main in ('ged', 'goal-date'):
        goal_dist(extra, 'date')
        update_order()
        decide_action('ls g')

    elif main in ('gp', 'goal-percentage'):
        goal_dist(extra, 'percentage')
        decide_action('ls g')

    elif main in ('gtg', 'goal-tag'):
        goal_dist(extra, 'tag')

    elif main in ('gdt', 'goal-delete_tags'):
        goal_dist(extra, 'del-tag')

    elif main in ('gs', 'subgoal'):
        goal_dist(extra, 'subgoal')
        decide_action('ls gs')

    elif main in ('gsd', 'delete-subgoal'):
        goal_dist(extra, 'subgoal-del')
        decide_action('ls gs')

    elif main in ('ges', 'edit-subgoal'):
        goal_dist(extra, 'subgoal-title')
        decide_action('ls gs')

    elif main in ('gts', 'toggle-subgoal'):
        goal_dist(extra, 'subgoal-tog')
        decide_action('ls gs')

    elif main in ('ud', 'undo-del'):
        cache_retrival(deleted['tasks'], cl.Task.tasks)
        update_order()
        decide_action('ls a')

    elif main in ('uc', 'undo-comp'):
        cache_retrival(completed['tasks'], cl.Task.tasks)
        update_order()
        decide_action('ls a')

    elif main in ('gud', 'goal-undo-del'):
        cache_retrival(deleted['goals'], cl.Goal.goals)
        update_order()
        decide_action('ls g')

    elif main in ('guc', 'goal-undo-comp'):
        cache_retrival(completed['goals'], cl.Goal.goals)
        update_order()
        decide_action('ls g')

    elif main in ('vg', 'view-goal'):
        view_goal(int(extra) - 1, subs=True)

    elif main in ('bkup', 'backup'):
        save_changes(backup=True)

    elif main in ('h', 'help'):
        print("  Full Documentation can be found at: "
              "https://todoian.readthedocs.io/en/latest/")

    else:
        print("  Command Not Recognised - Try Again or "
              "Enter 'h' For Usage Instructions.")


# DISPLAY FUNCTIONS

def list_displays(key, current_date):
    """Coordinate which list command to call based upon key argument."""
    if key in ('a', 'all'):
        view_goals(current_date)
        view_overdue(current_date)
        view_today(current_date)
        view_future(current_date)

    elif key.lower() in ('o', 'overdue'):
        view_overdue(current_date)

    elif key.lower() in ('t', 'today'):
        view_today(current_date)

    elif key.lower() in ('tm', 'tomorrow'):
        view_tomorrow(current_date)

    elif key.lower() in ('f', 'future'):
        view_future(current_date)

    elif key.lower() in ('g', 'goals'):
        view_goals()

    elif key.lower() in ('gs', 'goals-subs'):
        view_goals(show_subs=True)

    elif key.lower() in ('tgs', 'tags'):
        view_tags()

    elif key.lower().split(' ')[0] in ('tg', 'tag'):
        view_tag(key.split(' ')[1])

    else:
        view_overdue(current_date)
        view_today(current_date)
        view_future(current_date)


def view_overdue(current_date):
    """Print all tasks that are overdue."""
    print()
    print('  ' + font_dict['red'] + "OVERDUE TASKS"
          + font_dict['end'], end='\n\n')

    empty = True
    for task in cl.Task.tasks:
        if task.date.date() < current_date.date():
            over = (current_date.date() - task.date.date()).days
            if over in (0, 1):
                print(task, "[Due Yesterday]")
            else:
                print(task, "[Due {} Days Ago]".format(over))
            # Check for Subtasks
            if task.subs:
                [print(sub) for sub in task.subs]
                print()
                pass
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_today(current_date):
    """Print all tasks due today."""
    print()
    print('  ' + font_dict['green'] + "TODAY'S TASKS"
          + font_dict['end'], end='\n\n')

    empty = True

    for task in cl.Task.tasks:
        if task.date.date() == current_date.date():
            print(task)
            # Check for Subtasks
            if task.subs:
                [print(sub) for sub in task.subs]
                print()
                pass
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_tomorrow(current_date):
    """Print all tasks that are due tomorrow."""
    print()
    print('  ' + font_dict['orange'] + "TOMORROW'S TASKS"
          + font_dict['end'], end='\n\n')

    empty = True
    for task in cl.Task.tasks:
        until = (task.date.date() - current_date.date()).days
        if until == 1:
            print(task)
            # Check for Subtasks
            if task.subs:
                [print(sub) for sub in task.subs]
                print()
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_future(current_date):
    """Print all tasks with due dates beyond tomorrow"""
    print()
    print('  ' + font_dict['blue'] + "FUTURE TASKS"
          + font_dict['end'], end='\n\n')

    empty = True
    for task in cl.Task.tasks:
        if task.date.date() > current_date.date():
            until = (task.date.date() - current_date.date()).days
            if until == 1:
                print(task, "[Due Tomorrow]")
            else:
                print(task, "[Due in {} Days]".format(until))
            # Check for Subtasks
            if task.subs:
                [print(sub) for sub in task.subs]
                print()
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_tag(tag):
    """Display all Tasks with a tag matching the tag argument."""
    print('  ' + font_dict['green'] + "TASKS TAGGED WITH "
          + tag.upper() + font_dict['end'], end='\n\n')

    for task in cl.Task.tasks:
        if tag.lower() in [tag.lower() for tag in task.tags]:
            print("    {}| {} ({})".format(task.num, task.title,
                                           task.date.date()))
    print()

    print('  ' + font_dict['magenta'] + "GOALS TAGGED WITH "
          + tag.upper() + font_dict['end'], end='\n\n')
    for goal in cl.Goal.goals:
        if tag.lower() in [tag.lower() for tag in goal.tags]:
            print("    {}| {} ({})".format(goal.num, goal.title, goal.date))
    print()


def view_tags():
    """Display all Goals and Tasks with tags alongside their tags."""
    print('  ' + font_dict['magenta'] + "GOALS AND THEIR TAGS"
          + font_dict['end'], end='\n\n')

    for goal in cl.Goal.goals:
        if not goal.tags:
            continue
        print(goal)
        print("        {}".format(tuple(sorted(goal.tags))), end='\n\n')
    print()

    print('  ' + font_dict['green'] + "TASKS AND THEIR TAGS"
          + font_dict['end'], end='\n\n')

    for task in cl.Task.tasks:
        if not task.tags:
            continue
        print(task)
        print("        {}".format(tuple(sorted(task.tags))), end='\n\n')
    print()


def view_goal(goal_num, subs=False):
    """Display an individual goal with optional subtask display."""
    goal = cl.Goal.goals[goal_num]
    if goal.percent in ('auto', 'Auto'):
        percent = goal.auto_percentage() // 5
    elif goal.percent not in ('none', 'None'):
        percent = goal.percent // 5

    print(goal)
    if goal.percent in ('none', 'None'):
        pass
    elif goal.percent in ('auto', 'Auto') and not goal.subs:
        pass
    else:
        print("       {}{}{}{}{}".format(font_dict['green-nu'], '+' * percent,
              font_dict['red-nu'], '-' * (20 - percent), font_dict['end']))
    # Check for Subtasks
    if subs and goal.subs:
        [print(sub) for sub in goal.subs]
    print()


def view_goals(show_subs=False):
    """Display all goals either with or without subgoals."""
    print()
    print('  ' + font_dict['magenta'] + "GOALS" + font_dict['end'], end='\n\n')
    if not cl.Goal.goals:
        print("    No Goals Found")
        return
    [view_goal(int(goal.num) - 1, show_subs) for goal in cl.Goal.goals]

    if show_subs:
        print()
    else:
        print()
        print("        Subgoals Are Hidden. Use 'ls gs' To View", end='\n\n')


# Task Functions

def add_task(extra, current_date):
    """Instantiate a new task with optional attributes."""
    opt_date = current_date
    opt_repeat = None
    opt_tags = None

    keyword_order = re.findall(r'\s(\w+)=', extra)
    keyword_values = re.split(r'\s\w+=', extra)
    task = keyword_values.pop(0)
    values = zip(keyword_order, keyword_values)

    for value in values:
        if value[0] in ('date', 'd'):
            opt_date = dt.strptime(value[1], '%Y-%m-%d')

        elif value[0] in ('repeat', 'r'):
            if value[1].isnumeric():
                opt_repeat = int(value[1])
            else:
                value_list = value[1].split(',')
                to_check = set([day.strip().lower() for day in value_list])
                for day in to_check:
                    if day not in ('mon', 'tue', 'wed', 'thu',
                                   'fri', 'sat', 'sun'):
                        print("  Repeat days not in three letter format")
                    else:
                        opt_repeat = to_check

        elif value[0] in ('tag', 't'):
            if ',' in value[1]:
                opt_tags = [tag.strip() for tag in value[1].split(',')]
            else:
                opt_tags = [value[1]]

    cl.Task(task, opt_date, opt_repeat, opt_tags)


def delete_task(extra, del_tasks):
    """Delete a task, or all tasks if specified."""
    if extra in ("all", 'a'):
        check = cl.get_input("  Are you sure you want to delete all Task data "
                             "(y/n): ", one_line=True)
        if check.lower() in ('y', 'yes'):
            del_tasks.extend(cl.Task.tasks)
            cl.Task.tasks.clear()
        else:
            print("  Removal of All Tasks Aborted.")
    else:
        del_tasks.append(cl.Task.tasks.pop(int(extra) - 1))


def complete_task(extra, comp_tasks):
    """Mark a task as complete and move it to the completed_tasks cache."""
    task_num = int(extra) - 1
    repeat = cl.Task.tasks[task_num].repeat
    if repeat:
        cl.Task.tasks[task_num].do_repeat()
    else:
        comp_tasks.append(cl.Task.tasks.pop(task_num))


def complete_today(current_date, comp_tasks):
    """Mark all of today's tasks as complete."""
    today = current_date.date()
    to_comp = [task.num for task in cl.Task.tasks if task.date.date() == today]
    [complete_task(task_num, comp_tasks) for task_num in to_comp[::-1]]
    update_order()
    print("  Today's Tasks marked as complete.")


def complete_overdue(current_date, comp_tasks):
    """Mark all overdue tasks as complete."""
    today = current_date.date()
    while True:
        overdue = [task for task in cl.Task.tasks if task.date.date() < today]
        to_comp = [task.num for task in overdue]
        [complete_task(task_num, comp_tasks) for task_num in to_comp[::-1]]
        update_order()

        if cl.Task.tasks[0].date.date() > (current_date - timedelta(1)).date():
            print("  Overdue Tasks marked as complete.")
            break


def cache_retrival(take_from, give_to):
    """Retrive item from a cache list (LIFO)."""
    give_to.append(take_from.pop())


def add_goal(extra):
    """Instantiate a new Goal with optional attributes."""
    goal = extra
    opt_date = None
    opt_tags = None

    keyword_order = re.findall(r'\s(\w+)=', extra)
    keyword_values = re.split(r'\s\w+=', extra)
    goal = keyword_values.pop(0)
    values = zip(keyword_order, keyword_values)

    for value in values:
        if value[0] in ('date', 'd'):
            opt_date = value[1].strip()

        elif value[0] in ('tag', 't'):
            if ',' in value[1]:
                opt_tags = [tag.strip() for tag in value[1].split(',')]
            else:
                opt_tags = [value[1]]

    cl.Goal(goal, opt_date, opt_tags)


def delete_goal(extra, del_goals):
    """Delete a goal, or all goals if specified."""
    if extra in ("all", 'a'):
        check = cl.get_input("  Are you sure you want to delete all Goal data "
                             "(y/n): ", one_line=True)
        if check.lower() in ('y', 'yes'):
            del_goals.extend(cl.Goal.goals)
            cl.Goal.goals.clear()
        else:
            print("  Removal of All Goals Aborted.")
    else:
        del_goals.append(cl.Goal.goals.pop(int(extra) - 1))


def complete_goal(extra, comp_goals):
    """Mark a goal as complete and move it to the completed_goals cache."""
    goal_num = int(extra) - 1
    comp_goals.append(cl.Goal.goals.pop(goal_num))


def task_dist(extra, key):
    """Convert key into a task method call through distribution dictionary."""
    parse_regex = re.search(r'^(\d+)\s?(.*)?', extra)
    num = int(parse_regex.group(1))
    new_value = parse_regex.group(2)

    key_method = {
        'title': cl.Task.tasks[num - 1].edit_title,
        'date': cl.Task.tasks[num - 1].edit_date,
        'repeat': cl.Task.tasks[num - 1].edit_repeat,
        'tag': cl.Task.tasks[num - 1].add_tag,
        'del-tag': cl.Task.tasks[num - 1].remove_tag,
        'sub': cl.Task.tasks[num - 1].add_sub,
        'sub-title': cl.Task.tasks[num - 1].edit_sub,
        'sub-del': cl.Task.tasks[num - 1].remove_sub,
        'sub-tog': cl.Task.tasks[num - 1].toggle_sub,
    }

    key_method[key](new_value)
    save_changes()


def goal_dist(extra, key):
    """Convert key into a goal method call through distribution dictionary."""
    parse_regex = re.search(r'^(\d+)\s?(.*)?', extra)
    num = int(parse_regex.group(1))
    new_value = parse_regex.group(2)

    key_method = {
        'title': cl.Goal.goals[num - 1].edit_title,
        'date': cl.Goal.goals[num - 1].edit_date,
        'percentage': cl.Goal.goals[num - 1].edit_percentage,
        'tag': cl.Goal.goals[num - 1].add_tag,
        'del-tag': cl.Goal.goals[num - 1].remove_tag,
        'subgoal': cl.Goal.goals[num - 1].add_sub,
        'subgoal-title': cl.Goal.goals[num - 1].edit_sub,
        'subgoal-del': cl.Goal.goals[num - 1].remove_sub,
        'subgoal-tog': cl.Goal.goals[num - 1].toggle_sub,
    }

    key_method[key](new_value)
    save_changes()


def move_item(extra, data_list):
    """Move an item in data_list to a given or prompted for index."""
    nums = [int(x) - 1 for x in extra.split(' ')]
    if len(nums) == 2:
        data_list.insert(nums[1], data_list.pop(nums[0]))
    # Three numbers in extra indicates movement of a subitem
    else:
        sub_list = data_list[nums[0]].subs
        sub_list.insert(nums[2], sub_list.pop(nums[1]))
        data_list[nums[0]].sub_order()


def update_order():
    """Update the numbering of the Tasks and Goals."""
    cl.Task.tasks.sort(key=lambda x: x.date)
    for num, task in enumerate(cl.Task.tasks, 1):
        task.num = num

    for num, goal in enumerate(cl.Goal.goals, 1):
        goal.num = num


def save_changes(backup=False):
    """Write changes to data file."""
    if backup:
        file = 'backup.pickle'
    else:
        file = 'data.pickle'
    with open(file, 'wb') as fp:
        pickle.dump(cl.Task.tasks, fp)
        pickle.dump(cl.Goal.goals, fp)
    if backup:
        print("  Data succesfully backed up.")


def main():
    """Load data, display initial screen then prompt for commands."""
    # Populate tasks and goals
    try:
        with open('data.pickle', 'rb') as fp:
            cl.Task.tasks = pickle.load(fp)
            cl.Goal.goals = pickle.load(fp)
    except EOFError:
        pass
    except FileNotFoundError:
        pass

    # Initial display
    decide_action('ls a')

    # Prompt for commands until quit
    while True:
        print()
        action = cl.get_input("ENTER COMMAND ('q' to quit): ", one_line=True)
        print()
        if action.lower() in ('q', 'quit', 'exit'):
            break

        else:
            try:
                decide_action(action)

            except IndexError:
                print()
                print("  No Item Found at That Position - "
                      "Enter 'h' for Usage Instructions.")
                print()

            except ValueError:
                print()
                print("  Did You Forget A Number For The Item/Subitem - "
                      "Enter 'h' for Usage Instructions.")
                print()


if __name__ == '__main__':

    # A dictionary of ANSI escapse sequences for font effects.
    font_dict = {
        'blue':  '\033[4;94m',
        'green':  '\033[4;92m',
        'green-nu':  '\033[1;92m',
        'orange': '\033[4;93m',
        'red':  '\033[4;91m',
        'red-nu':  '\033[1;91m',
        'magenta':  '\033[4;95m',
        'end':  '\033[0m',
    }

    # Cache Lists
    deleted = {'tasks': [], 'goals': []}
    completed = {'tasks': [], 'goals': []}

    main()
