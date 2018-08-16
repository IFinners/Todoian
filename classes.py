#!/usr/bin/env python3

import re
import pickle
from datetime import datetime as dt
from datetime import timedelta


class Task():
    """Representation of a task."""

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
            new_value = get_input("New description below")
        self.title = new_value

    def edit_date(self, new_value=False):
        """Edit a due date."""
        if not new_value:
            new_value = get_input("  New due date (YYYY-MM-DD): ", one_line=True)
        self.date = new_value

    def edit_repeat(self, new_value=False):
        """Edit a repeat."""
        if not new_value:
            new_value = get_input("  New repeat:", one_line=True)
        self.repeat = new_value

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
                print("    There is no {} tag for this item.".format(new_value))

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

    def edit_sub(self, new_value=False):
        """Edit a subtask's title."""
        if not new_value:
            new_value = get_input("  Subtask number: ", one_line=True)
        self.subs[int(new_value) - 1].edit_title()

    def toggle_sub(self, new_value=False):
        """Toggle a subtask's completed status."""
        if not new_value:
            new_value = get_input("  Subtask number|'done'|'todo': ", one_line=True)
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
        self.subs.sort(key=lambda x: x.num)
        for num, sub in enumerate(self.subs, 1):
            sub.num = num


class Sub(Task):
    """."""
    def __init__(self, title, num, completed=False):
        """Return a new task object."""
        self.title = title
        self.num = num
        self.completed = completed

    def __str__(self):
        if not self.completed:
            return "        {}".format(self.num).rjust(8) + ") {}".format(self.title)
        return "        " + strike_text("{}".format(self.num) + ") {}".format(self.title))

    def complete_toggle(self):
        """."""
        if self.completed:
            self.completed = False
        else:
            self.completed = True



# Associated functions

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


def strike_text(text):
    """Add a strikethtough effect to text."""
    striked = ''
    for char in text:
        striked = striked + char + '\u0336'
    return striked



if __name__ == '__main__':

    try:
        with open('test.pickle', 'rb') as fp:
            Task.tasks = pickle.load(fp)
    except:
        pass

    for task in Task.tasks:
        print(task.title)
        print(task.date)

    with open('test.pickle', 'wb') as fp:
            pickle.dump(Task.tasks, fp)
