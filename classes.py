import re
import pickle
from datetime import datetime as dt
from datetime import timedelta


class Task():
    """."""
    today = dt.strftime(dt.now(), '%Y-%m-%d')
    tasks = []

    def __init__(self, description, due_date=today, repeat=None, tags=[], subs=[]):
        """Return a new task object."""
        self.description = description
        self.due_date = due_date
        self.repeat = repeat
        self.tags = tags
        self.subs = subs
        Task.tasks.append(self)

    def __str__(self):
        return ("  {}".format(self.description))

    def edit_description(self, new_desc=None):
        """Edit a description."""
        if not new_desc:
            print("  Editing: {}".format(self.description))
            new_desc = get_input("Enter the new description below")
        self.description = new_desc

    def edit_due(self, new_due=None):
        """Edit a due date."""
        if not new_due:
            new_due = get_input("  Enter new due date (YYYY-MM-DD): ", one_line=True)
        self.due_date = new_due

    def edit_repeat(self, new_rep=None):
        """Edit a repeat."""
        if not new_rep:
            new_rep = get_input("  Enter new repeat:", one_line=True)
        self.repeat = new_rep

    def add_tag(self, new_tag=None):
        """Add a tag."""
        if not new_tag:
            new_tag = get_input("  Enter new tag: ", one_line=True)
        self.tags.append(new_tag)

    def remove_tag(self, tag=None, del_all=False):
        """Remove a tag or remove all tags."""
        if del_all:
            self.tags = []
            return
        if not tag:
            tag = get_input("  Enter the tag you'd like to remove: ", one_line=True)
        self.tags.remove(tag)

    def add_sub(self, sub=None):
        """Add a subtask to a Task."""
        if not sub:
            sub = get_input("  Enter subtask for '{}' below:".format(self.description))
        self.subs.append(sub)

    def remove_sub(self, sub_num=None, del_all=False):
        """Remove a subtask or all subtasks from a Task."""
        if del_all:
            self.subs = []
            return
        if not sub_num:
            sub_num = int(get_input(("  Enter the number of the subtask you wish "
                      "to remove from '{}' below:",format(self.description))))
        del self.subs[sub_num - 1]


# Associated functions

def get_input(prompt, one_line=False):
    """Get user input for a given prompt."""
    if one_line:
        to_return = input("  {}".format(prompt))
    else:
        print("  {}:".format(prompt))
        to_return = input(" ")
    return to_return



if __name__ == '__main__':

    try:
        with open('data.pickle', 'rb') as fp:
            Task.tasks = pickle.load(fp)
    except:
        pass

    for task in Task.tasks:
        print(task.description)
