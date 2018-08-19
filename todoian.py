#!/usr/bin/env python3

from datetime import datetime as dt
from datetime import timedelta
import pickle
import re

import classes as cl


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

        elif extra.lower() in ('g', 'goals'):
            view_goals()

        elif extra.lower() in ('gs', 'goals-subs'):
            view_goals(show_subs=True)

        elif extra.lower() in ('tgs', 'tags'):
            view_tags()

        elif extra.lower().split(' ')[0] in ('tg', 'tag'):
            view_tag(extra.split(' ')[1])

    elif main in ('a', 't', 'add', 'task'):
        add_task(command_regex.group(2))
        update_order()
        save_changes()

    elif main in ('ga', 'g', 'add-goal', 'goal'):
        add_goal(command_regex.group(2))
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

    elif main in ('gd', 'goal-delete'):
        delete_goal(extra)
        update_order()
        save_changes()

    elif main in ('m', 'move'):
        move_item(extra, cl.Task.tasks)
        update_order()
        save_changes()

    elif main in ('ms', 'move-sub'):
        move_item(extra, cl.Task.tasks)
        save_changes()

    elif main in ('gm', 'goal-move'):
        move_item(extra, cl.Goal.goals)
        update_order()
        save_changes()

    elif main in ('gms', 'goal-move-sub'):
        move_item(extra, cl.Goal.goals)
        save_changes()

    elif main in ('gc', 'goal-comp', 'goal-complete'):
        complete_goal(extra)
        update_order()
        save_changes()

    elif main in ('e', 'edit'):
        task_dist(extra, 'title')

    elif main in ('ed', 'edit-date'):
        task_dist(extra, 'date')

    elif main in ('r', 'repeat'):
        task_dist(extra, 'repeat')

    elif main in ('tg', 'tag'):
        task_dist(extra, 'tag')

    elif main in ('dt', 'delete_tags'):
        task_dist(extra, 'del-tag')

    elif main in ('s', 'sub'):
        task_dist(extra, 'sub')

    elif main in ('ds', 'delete-sub'):
        task_dist(extra, 'sub-del')

    elif main in ('es', 'edit-sub'):
        task_dist(extra, 'sub-title')

    elif main in ('ts', 'toggle-sub'):
        task_dist(extra, 'sub-tog')

    elif main in ('ge', 'goal-edit'):
        goal_dist(extra, 'title')

    elif main in ('ged', 'goal-date'):
        goal_dist(extra, 'date')

    elif main in ('gp', 'goal-percentage'):
        goal_dist(extra, 'percentage')

    elif main in ('gtg', 'goal-tag'):
        goal_dist(extra, 'tag')

    elif main in ('gdt', 'goal-delete_tags'):
        goal_dist(extra, 'del-tag')

    elif main in ('gs', 'subgoal'):
        goal_dist(extra, 'subgoal')

    elif main in ('gsd', 'delete-subgoal'):
        goal_dist(extra, 'subgoal-del')

    elif main in ('ges', 'edit-subgoal'):
        goal_dist(extra, 'subgoal-title')

    elif main in ('gts', 'toggle-subgoal'):
        goal_dist(extra, 'subgoal-tog')

    elif main in ('ud', 'undo-del'):
        cache_retrival(deleted_tasks, cl.Task.tasks)
        update_order()

    elif main in ('uc', 'undo-comp'):
        cache_retrival(completed_tasks, cl.Task.tasks)
        update_order()

    elif main in ('gud', 'goal-undo-del'):
        cache_retrival(deleted_goals, cl.Goal.goals)
        update_order()

    elif main in ('guc', 'goal-undo-comp'):
        cache_retrival(completed_goals, cl.Goal.goals)
        update_order()

    elif main in ('vg', 'view-goal'):
        view_goal(int(extra) - 1, subs=True)

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
        if task.date.date() < current_date.date():
            over = (current_date - task.date).days
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
        if task.date.date() == current_date.date():
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
        if (task.date - current_date).days == 1:
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
            until = (task.date - current_date).days
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
            print("    {}| {} ({})".format(task.num, task.title, task.date.date()))
    print()

    print('  ' + FONT_DICT['magenta'] + "GOALS TAGGED WITH "
          + tag.upper() + FONT_DICT['end'], end='\n\n')
    for goal in cl.Goal.goals:
        if tag.lower() in [tag.lower() for tag in goal.tags]:
            print("    {}| {} ({})".format(goal.num, goal.title, goal.date))
    print()


def view_tags():
    """Display all Tasks and Goals with their tags."""
    print('  ' + FONT_DICT['green'] + "TASKS AND THEIR TAGS" + FONT_DICT['end'], end='\n\n')
    for task in cl.Task.tasks:
        print(task)
        print("        {}".format(tuple(sorted(task.tags))), end='\n\n')
    print()

    print('  ' + FONT_DICT['magenta'] + "GOALS AND THEIR TAGS" + FONT_DICT['end'], end='\n\n')
    for goal in cl.Goal.goals:
        print(goal)
        print("        {}".format(tuple(sorted(goal.tags))), end='\n\n')
    print()


def view_goal(goal_num, subs=False):
    """Display an individual goal with optional subtask display."""
    goal = cl.Goal.goals[goal_num]
    if goal.percentage in ('auto', 'Auto'):
        percent = goal.auto_percentage() // 5
    elif goal.percentage not in ('none', 'None'):
        percent = goal.percentage // 5

    print(goal)
    if goal.percentage not in ('none', 'None'):
        print("       {}{}{}{}{}".format(FONT_DICT['green no u'], '+' * percent,
                FONT_DICT['red no u'], '-' * (20 - percent), FONT_DICT['end']))
    # Check for Subtasks
    if subs and goal.subs:
        for sub in goal.subs:
            print(sub)
    print()


def view_goals(show_subs=False):
    """Display all goals either with or without subgoals."""
    print()
    print('  ' + FONT_DICT['magenta'] + "GOALS" + FONT_DICT['end'], end='\n\n')
    if not cl.Goal.goals:
        print("    No Goals Found")
        return
    for goal in cl.Goal.goals:
        view_goal(int(goal.num) - 1, show_subs)

    if show_subs:
        print()
    else:
        print()
        print("        Subgoals Are Hidden. Use 'ls gs' To View Them", end='\n\n')


# Task Functions

def add_task(extra):
    """Instantiate a new task with optional attributes."""
    task = extra
    opt_date = current_date
    opt_repeat = None
    opt_tags = None
    if '~~' in extra:
        task, attributes = extra.split(' ~~')
        date_regex = re.search(r'(?:d|date)=(\d{4}-\d{2}-\d{2})', attributes)
        rep_regex = re.search(r'(?:r|rep|repeat)=(\d+)', attributes)
        tag_regex = re.search(r'(?:t|tag)=(.+)((d|date|rep|repeat|r)=)?', attributes)
        if date_regex:
            opt_date = dt.strptime(date_regex.group(1), '%Y-%m-%d')
        if rep_regex:
            opt_repeat = int(rep_regex.group(1))
        if tag_regex:
            if ',' in tag_regex.group(1):
                opt_tags = [tag.strip() for tag in tag_regex.group(1).split(',')]
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


def cache_retrival(take_from, give_to):
    """Retrive item from a cache list (LIFO)."""
    give_to.append(take_from.pop())


def add_goal(extra):
    """Instantiate a new Goal with optional attributes."""
    goal = extra
    opt_date = None
    opt_tags = None
    if '~~' in extra:
        goal, attributes = extra.split(' ~~')
        date_regex = re.search(r'(?:d|date)=(.+)((t|tag)=)?', attributes)
        tag_regex = re.search(r'(?:t|tag)=(.+)((d|date)=)?', attributes)
        if date_regex:
            opt_date = date_regex.group(1)
        if tag_regex:
            if ',' in tag_regex.group(1):
                opt_tags = [tag.strip() for tag in tag_regex.group(1).split(',')]
            else:
                opt_tags = [tag_regex.group(1)]
    cl.Goal(goal, opt_date, opt_tags)


def delete_goal(extra):
    """Delete a goal, or all goals if specified."""
    if extra in ("all", 'a'):
        check = cl.get_input("  This Will Delete All Goal Data. Are You Sure "
                        "You Want to Continue? (y/n): ", one_line=True)
        if check.lower() in ('y', 'yes'):
            deleted_goals.extend(cl.Goal.goals)
            cl.Goal.goals.clear()
        else:
            print("  Removal of All Goals Aborted.")
    else:
        deleted_goals.append(cl.Goal.goals.pop(int(extra) - 1))


def complete_goal(extra):
    """Mark a goal as complete and move it to the completed_goals cache."""
    goal_num = int(extra) - 1
    completed_goals.append(cl.Goal.goals.pop(goal_num))


def task_dist(extra, key):
    """Convert a key into a task method call through a distribution dictionary."""
    parse_regex = re.search(r'^(\d+)\s?(.*)?', extra)
    num = int(parse_regex.group(1))
    new_value = parse_regex.group(2)

    key_method = {
        'title': cl.Task.tasks[num - 1].edit_title,
        'date': cl.Task.tasks[num - 1].edit_date,
        'repeat': cl.Task.tasks[num - 1].edit_repeat,
        'tag': cl.Task.tasks[num - 1].add_tag,
        'del_tag': cl.Task.tasks[num - 1].remove_tag,
        'sub': cl.Task.tasks[num - 1].add_sub,
        'sub-title': cl.Task.tasks[num - 1].edit_sub,
        'sub-del': cl.Task.tasks[num - 1].remove_sub,
        'sub-tog': cl.Task.tasks[num - 1].toggle_sub,
        }

    key_method[key](new_value)
    save_changes()


def goal_dist(extra, key):
    """Convert a key into a goal method call through a distribution dictionary."""
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
    """Move and item in data_list to a new index."""
    nums = [int(x) - 1 for x in extra.split(' ')]
    if len(nums) == 2:
        data_list.insert(nums[1], data_list.pop(nums[0]))
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


def save_changes():
    """Write changes to data file."""
    with open ('data.pickle', 'wb') as fp:
        pickle.dump(cl.Task.tasks, fp)
        pickle.dump(cl.Goal.goals, fp)




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
            cl.Goal.goals = pickle.load(fp)
    except EOFError:
        pass


    # Cache Lists
    deleted_tasks = []
    completed_tasks = []
    deleted_goals = []
    completed_goals = []

    current_date = dt.now()

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
                print("  No Item Found at That Position - Enter 'h' for Usage Instructions.")
                print()

            except ValueError:
                print()
                print("  Did You Forget A Number For The Item/Subitem in Your Command? - "
                    "Enter 'h' for Usage Instructions.")
                print()
