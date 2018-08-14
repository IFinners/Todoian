import re
import pickle
from datetime import datetime as dt
from datetime import timedelta


class Task():
    """Representation of a task."""
    
    tasks = []

    def __init__(self, title, date, repeat, tags=[], subs=[], num=None):
        """Return a new task object."""
        self.title = title
        self.date = date
        self.repeat = repeat
        self.tags = tags
        self.subs = subs
        self.num = num
        Task.tasks.append(self)

    def __str__(self):
        return "    {}".format(self.num).rjust(6) + "| {}".format(self.title)

    def edit_title(self):
        """Edit the tasks title."""
        print("  Editing: {}".format(self.title))
        new_desc = get_input("Enter the new description below")
        self.title = new_desc

    def edit_date(self):
        """Edit a due date."""
        new_due = get_input("  Enter new due date (YYYY-MM-DD): ", one_line=True)
        self.date = new_due

    def edit_repeat(self):
        """Edit a repeat."""
        new_rep = get_input("  Enter new repeat:", one_line=True)
        self.repeat = new_rep

    def add_tag(self):
        """Add a tag."""
        new_tag = get_input("  Enter new tag: ", one_line=True)
        self.tags.append(new_tag)

    def remove_tag(self, del_all=False):
        """Remove a tag or remove all tags."""
        if del_all:
            self.tags = []
            return
        tag = get_input("  Enter the tag you'd like to remove: ", one_line=True)
        self.tags.remove(tag)

    def add_sub(self, sub=None):
        """Add a subtask to a Task."""
        if not sub:
            sub = get_input("  Enter subtask for '{}' below:".format(self.title))
        self.subs.append(sub)

    def remove_sub(self, sub_num=None, del_all=False):
        """Remove a subtask or all subtasks from a Task."""
        if del_all:
            self.subs = []
            return
        if not sub_num:
            sub_num = int(get_input(("  Enter the number of the subtask you wish "
                      "to remove from '{}' below:",format(self.title))))
        del self.subs[sub_num - 1]


# Associated functions

def get_input(prompt, one_line=False):
    """Get user input for a given prompt."""
    if one_line:
        to_return = input("  {}".format(prompt))
    else:
        print("  {}".format(prompt))
        to_return = input("   ")
    return to_return



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
