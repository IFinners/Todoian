#!/usr/bin/env python3

"""Classes and related functions for todoian.py."""

from datetime import datetime as dt
from datetime import timedelta
import re


class Task():
    """Representation of a Task."""

    tasks = []

    def __init__(self, title, date, repeat, tags, subs=None, num=None):
        """Return a new task object."""
        self.title = title
        self.date = date
        self.repeat = repeat
        self.tags = []
        self.subs = []
        self.num = num

        if tags:
            self.tags.extend(tags)
        Task.tasks.append(self)

    def __str__(self):
        return "    {}".format(self.num).rjust(6) + "| {}".format(self.title)

    def edit_title(self, new_value=False):
        """Edit the tasks title."""
        if not new_value:
            print("  Editing: {}".format(self.title))
            new_value = get_input("New description below: ")
        self.title = new_value

    def edit_date(self, new_value=False):
        """Edit a due date."""
        if not new_value:
            new_value = get_input("  New date (YYYY-MM-DD): ", one_line=True)
        try:
            self.date = dt.strptime(new_value, '%Y-%m-%d')
        except ValueError:
            print("  Date given is not valid")

    def edit_repeat(self, new_value=False):
        """Edit a repeat."""
        if not new_value:
            new_value = get_input("  New repeat: ", one_line=True)
        if new_value.isnumeric():
            self.repeat = int(new_value)
        elif new_value in ('none', 'None'):
            self.repeat = None

        else:
            self.repeat = set([day.strip() for day in new_value.split(',')])

    def do_repeat(self):
        """Process repeat and change date accordingly."""
        if type(self.repeat) == int:
            self.date += timedelta(self.repeat)
        else:
            day = dt.now()
            while True:
                test_date = day + timedelta(1)
                if dt.strftime(test_date, '%a').lower() in self.repeat:
                    self.date = test_date
                    break
                day = test_date

        for sub in self.subs:
            sub.completed = False

    def add_tag(self, new_value=False):
        """Add a tag."""
        if not new_value:
            if self.tags:
                print("    Current tags: {}".format(self.tags), end='\n\n')
            new_value = get_input("  New Tag: ", one_line=True)
        if ',' in new_value:
            tags = new_value.split(',')
        else:
            tags = [new_value]
        self.tags.extend(tags)

    def remove_tag(self, new_value=False):
        """Remove a tag or remove all tags."""
        if not new_value:
            if self.tags:
                print("    Current tags: {}".format(self.tags), end='\n\n')
            new_value = get_input("  Tag|'all': ", one_line=True)
        if new_value.lower() == 'all':
            self.tags = []
        else:
            try:
                self.tags.remove(new_value)
            except ValueError:
                print("    No {} tag for this item.".format(new_value))

    def add_sub(self, new_value=False):
        """Add a subtask to a Task."""
        if not new_value:
            new_value = get_input("  New Subtask for '{}':".format(self.title))
        self.subs.append(Sub(new_value, len(self.subs) + 1))

    def remove_sub(self, new_value=False):
        """Remove a subtask or all subtasks from a Task."""
        if not new_value:
            new_value = get_input("  Subtask number|'all': ", one_line=True)
        try:
            del self.subs[int(new_value) - 1]
        except ValueError:
            if new_value.lower() == 'all':
                self.subs = []
        self.sub_order()

    def edit_sub(self, values):
        """Edit a subtask's title."""
        edit_regex = re.search(r'(\d+)\s?(.*)?', values)
        sub_num = int(edit_regex.group(1)) - 1
        if not edit_regex.group(2):
            print("  Editing: {}".format(self.subs[sub_num].title), end='\n\n')
            new_title = get_input("  New title: ", one_line=True)
        else:
            new_title = edit_regex.group(2)

        self.subs[sub_num].edit_title(new_title)

    def toggle_sub(self, new_value=False):
        """Toggle a subtask's completed status."""
        if not new_value:
            new_value = get_input("  Enter the Subtask(s) you want to toggle "
                                  "number|'done'|'todo': ", one_line=True)
        try:
            self.subs[int(new_value) - 1].complete_toggle()
        except ValueError:
            if new_value.lower() == 'done':
                for sub in self.subs:
                    sub.completed = True
            elif new_value.lower() == 'todo':
                for sub in self.subs:
                    sub.completed = False

    def sub_order(self):
        """Update the numbering of the subtasks."""
        for num, sub in enumerate(self.subs, 1):
            sub.num = num


class Goal(Task):
    """Representation of a Goal."""

    goals = []

    def __init__(self, title, date, tags, subs=None, percent='auto', num=None):
        """Return a new Goal object."""
        self.title = title
        self.date = date
        self.tags = []
        self.subs = []
        self.percent = percent
        self.num = len(Goal.goals) + 1

        if tags:
            self.tags.extend(tags)
        Goal.goals.append(self)

    def __str__(self):
        to_ret = "    {}| ".format(self.num).rjust(6) + self.title.upper()
        if self.date:
            to_ret += " [Target: {}]".format(self.date)
        if self.subs:
            to_ret += ' ~'
        return to_ret

    def edit_date(self, new_value=False):
        """Edit a target date."""
        if not new_value:
            new_value = get_input("  New target date: ", one_line=True)
        self.date = new_value

    def edit_percentage(self, new_value=False):
        """Edit a Goal's percentage."""
        if not new_value:
            new_value = get_input("  Completion percentage: ", one_line=True)
        if new_value in('auto', 'Auto', 'None', 'none'):
            self.percent = new_value
        else:
            self.percent = int(new_value)

    def auto_percentage(self):
        """Calculate percentage completion from subgoal completion."""
        if not self.subs:
            return 0
        complete = 0
        for sub in self.subs:
            if sub.completed:
                complete += 1
        return int((complete / len(self.subs)) * 100)


class Sub(Task):
    """Representation of a Subitem."""
    def __init__(self, title, num, completed=False):
        """Return a new task object."""
        self.title = title
        self.num = num
        self.completed = completed

    def __str__(self):
        if not self.completed:
            return ("        {}".format(self.num).rjust(8)
                    + ") {}".format(self.title))

        return ("        " + self.strike_text("{}".format(self.num)
                + ") {}".format(self.title)))

    def complete_toggle(self):
        """Toggle a Subitems completed status."""
        if self.completed:
            self.completed = False
        else:
            self.completed = True

    def strike_text(self, text):
        """Add a strikethtough effect to text."""
        striked = ''
        for char in text:
            striked = striked + char + '\u0336'
        return striked


# Shared functions
def get_input(prompt, one_line=False):
    """Get user input for a given prompt."""
    if one_line:
        to_return = input("   {}".format(prompt))
        print()
    else:
        print("  {}".format(prompt), end='\n\n')
        to_return = input("    ")
        print()
    return to_return
