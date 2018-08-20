=============
Task Commands
=============

Ordered by their due dates and customisable with repeats, tags and Subitems(see :ref:`Subitem Commands <subitem>` for details) 
Tasks are what Task Managers... well... manage and here is a breakdown of how to do just that.

Adding
======
('a', 't', 'add', 'task')

::

   add New Task Description
   

Optional keywords of date, repeats and tags can be added using the following format:
::

   keyword=value

To set the date add the Task with the keyword 'date' or 'd':
::

   add Task date=2018-01-01

- Note that he date must be in the format detailed in the :ref:`change-date` section.

A repeat can be added with the keyword 'repeat' or 'r':
::

   add Task repeat=mon, wed, sat


- Note that the repeat must be one of the options detailed in the :ref:`add-repeat` section and spaces are optional.

A tag, or tags, can be added in the same way with the keyword 'tag' or 't':
::

   add Task tags= tag1, tag2, tag3


- Note that the list of tags, like the list of repeat days above it, can have spaces between the items or between the = and the first item or not.

All of these options can be combined into one addition by combining them:
::

   add Task with Everything d=2018-01-01 t=tag1, tag2 r=7


- Note that the keywords can be in any order but the Task title must come first


Completing
==========
(c, comp, complete)

Marking a Task as complete moves it from the active Task list to an unseen cache, unless it has a repeat in which case 
it is added back onto the Task list with the appropriate new information.
::

   complete task-number

All Tasks with due dates equal to the current date are marked as complete by writing 't' or 'today' instead of a Task number:
::

   complete today

All Tasks with due dates earlier than the current date are marked as complete by writing 'o' or 'overdue' instead of a Task number:
::

   complete overdue

Note that this completes overdue tasks with repeats until their due date is no longer overdue.  


Deleting
========
(d, del, delete)

Deleting a Task is similar to completing one in that it moves the Task from the active Task list to an unseen cache. 
However, with deletion this is done regardless of any repeat flags.
::

   delete task-number
   
All Tasks can be deleted by writing 'a' or 'all' instead of a Task number - a prompt will ask for confirmation:
::

   delete all


Undoing a Completion or Deletion
================================
As long as the program hasn't been exited since a completion or deletion was made, the items can be restored to their previous state using the commands:

undo-comp, uc - for undoing a completion

undo-del, ud -  for undoing a deletion

Both of these commands will work for the restoration of multiple items if done repeatedly


Moving
======
(m, move)

Tasks are sorted by their due dates, and whilst this cannot be changed, the order of Tasks within their date brackets 
can with the following command:
::

   move task-number move-number

Where the move number is the position to move the Task to in the list.


Editing a Description
=====================
(e, edit)

Editing a Task's description can be done through the following command:
::

   edit task-number [new Task description]


.. _change-date:

Changing a Due Date
===================
(ed, edit-date)

Changing a Task's due date can be done through the prompt that follows the following command:
::

   change-date task-number [due date]

The date must be entered as:

- A date formatted like YYYY-MM-DD e.g. 2018-01-25:


.. _add-repeat:

Adding a Repeat
===============
(r, repeat)

Repeats allow Tasks to be automatically re-added to the Task list upon completion. The repeat can be set with the following command:
::

   repeat task-number [repeat]

There are two types of repeat that can be set. The simplest of these is the number of days repeat - 
for example setting the repeat to the value 7 will result in a Task that repeats weekly.

Another way to specify a repeat is through a three letter day name or a list of day names (of any length) seperated 
by a comma:
::

   repeat task-number [mon,wed,fri]

This Task would repeat every Monday, Wednesday and Friday.

To remove a repeat, simply do the above but set the repeat to 'none':
::

   repeat task-number [none]


Adding a Tag
============
(tg, tag)

Tagging a Task with a keyword means it can be displayed with other Tasks and Goals (see the Display Command section of this guide) that share that tag. To add tag(s) to a Task, enter the following command:
::

   tag task-number [tag,tag2,tag3]


Deleting a Tag
==============
(dt, delete-tag)

A specific tag can be deleted from a Task by using it as the keyword in the command to follow, or all tags for that Task 
can be deleted by using the keyword 'all':
::

   delete-tag task-number [keyword]
