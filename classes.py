import re
import pickle
from datetime import datetime as dt
from datetime import timedelta


class Task():
    """Representation of a task."""
    
    tasks = []

    def __init__(self, title, date, repeat, tags=None, subs=None, num=None):
        """Return a new task object."""
        self.title = title
        self.date = date
        self.repeat = repeat
        self.tags = []
        self.subs = []
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
        if self.tags:
            print("    Current tags: {}".format(self.tags), end='\n\n')
        new_tag = get_input("  Enter new tag: ", one_line=True)
        self.tags.append(new_tag)

    def remove_tag(self, del_all=False):
        """Remove a tag or remove all tags."""
        if self.tags:
            print("    Current tags: {}".format(self.tags), end='\n\n')
        tag = get_input("  Enter the tag you'd like to remove or enter 'all' "
                        "to remove all tags: ", one_line=True)
        if tag == 'all':
            self.tags = []
        else:
            try:
                self.tags.remove(tag)
            except ValueError:
                print("    There is no {} tag for this item.".format(tag))

    def add_sub(self):
        """Add a subtask to a Task."""
        sub = get_input("  Enter new subtask for '{}' below:".format(self.title))
        self.subs.append(Sub(sub, len(self.subs) + 1))

    def remove_sub(self):
        """Remove a subtask or all subtasks from a Task."""
        sub_num = get_input("  Enter the subtask number or 'all' to delete all "
                            "subtasks: ", one_line=True)
        if sub_num.lower() == 'all':
            self.subs = []
        else:
            del self.subs[int(sub_num) - 1]


class Sub(Task):
    """."""
    def __init__(self, title, num, completed=False):
        """Return a new task object."""
        self.title = title
        self.num = num
        self.completed = completed

    def __str__(self):
        return "        {}".format(self.num).rjust(8) + ") {}".format(self.title)
        


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
