.. _subitem:

================
Subitem Commands
================

Both Tasks and Goals can be broken down into smaller parts through the use of Subitems. The functionality is identical
for Tasks and Goals but the commands vary slightly as indicated beneath each section below.

Adding
======
(s, subtask) (gs, subgoal)

::

   subtask task-number [subitem description]


Completing and Undoing Completion
=================================
(ts, toggle-sub) (gts, toggle-subgoal)

Marking a Subitem as complete strikesthrough the subitem when displayed and updates a Goal's progress bar if percentage is set to 'auto'.
This is done and undone by the toggle command. 
::

   toggle-subgoal goal-number [subgoal-number]


All Subitems under a specified Task or Goal can be marked as complete ('done') or incomplete ('todo') using the toggle commands:
::

  toggle-sub task-number ['done']


Deleting
========
(ds, delete-subtask) (gds, delete-subgoal)

Unlike the deletion of a Task or Goal, the deletion of a Subitem is permanent even prior to closing Todoian.
::

   delete task-number [subtask-number]
   

Moving
======
(ms, move-sub) (gms, goal-move-sub)

Subitems can't be transferred to another item, but their order beneath the Task or Goal can be changed.
::

   move-sub task-number subtask-number new-position


Editing a Description
=====================
(es, edit-sub) (ges, edit-subgoal)

::

   edit-sub task-number subtask-number [new subtask description]
