==================================
Display and Miscellaneous Commands
==================================

Todoian customises its display based upon the command it has just been given, but the various types of display can also be invoked through their own set of commands.


The List Command
================

The main display command is the list (ls, list) command which with no modifiers will print all Tasks organised by their Due Dates:
::

  list


The following modifications to the list command, and their effects are...
View all tasks with due dates of today with (t, today):
::

   list today


All overdue tasks with (o, overdue):
::

 list overdue


Task's due tomorrow with (tm, tomorrow):
::

   list tomorrow


Task's due tomorrow and beyond with (f, future):
::

   list future


All Goals with (g, goals):
::

   list goals


By default, Goals are displayed without their Subgoals. Those with Subgoals are indicated by a trailing tilde ('~').
Goals, and all of their Subgoals, can be viewed with (gs, goals-subs):
::

   list goals-subs


All Goals (without Subgoals) and Tasks can be viewied with (a, all):
::

   list all


Any Task or Goal with a specific Tag can be viewed with (tg, tag):
::
   
   list tag [tag]


All Goals and Tasks that have tags can be displayed with their tags listed beneath them with (tgs, tags):
::

  list tags


The View Command
=================

Long-term goals can often have a lot of Subgoals. A single goal with all of its Subgoals can be viewed with (vg, view_goal) 
::

   view-goal goal-number


Other Commands
==============

A link to this documentation can be displayed within the program with (h, help)
::

  help
