=============
Goal Commands
=============

Goals have many of the commands that Tasks do and are invoked in the same way with the command slightly modified 
with either the letter 'g' or the hyphened word 'goal'.

Adding
======
('ga', 'g', 'goal', 'add-goal')

::

   goal New Goal Description
   

Optional keywords of date and tags can be added with keywords using the following format:
::

   keyword=value

To set the date add the Goal with the keyword 'date' or 'd':
::

   ga Goal date= Sometime Next Month

- Note that the date can be anything and the space between the = and the start of it is optional.


A tag, or tags, can be added in the same way with the keyword 'tag' or 't':
::

   ga Goal tags=tag1, tag2, tag3


- Note that the spaces in the list of tags, like the list of repeat days above it, are optional

All of these options can be combined into one addition simply by having a space between the keywords:
::

   add Task with Everything d=This Month t=tag1, tag2


- Note that the keywords can be in any order but the Goal title must come first.


Completing
==========
('gc', 'goal-comp', 'goal-complete')

Marking a Goal as complete moves it from the active Goal list to an unseen cache.
::

   complete goal-number


Deleting
========
('gd', 'goal-delete')

Deleting a Goal is identical to completing one in that it moves the Goal from the active Goal list to an unseen cache. 
The only real difference comes when retrieving the Goal from the cache and the lack of accomplishment one feels with a deletion.
::

   delete goal-number
   
All Goals can be deleted by writing 'a' or 'all' instead of a Goal number - a prompt will ask for confirmation:
::

   delete all


Undoing a Completion or Deletion
================================
As long as the program hasn't been exited since a completion or deletion was made, the items can be restored to their previous state using the commands:

guc, goal-undo-comp - for undoing a completion

gud, goal-undo-del -  for undoing a deletion

Both of these commands will work for the restoration of multiple items if done repeatedly


Moving
======
(gm, goal-move)

By default goals are sorted by when they were added but they can be moved at will with the following command:
::

   goal-move goal-number move-number

Where the move number is the position to move the Task to in the list.


Editing a Description
=====================
(ge, goal-edit)

Editing a Goal's description can be done through the following command:
::

   edit goal-number [new Goal description]



Changing a Due Date
===================
(ged, goal-edit-date)

Changing a Goal's date - a target for when you wish to complete it by so it can be more general than a specific day - can be done with the following command:
::

   change-date goal-number [due date]


Adding a Tag
============
(gtg, goal-tag)

Tagging a Goal with a keyword means it can be displayed with other Tasks and Goals (see the Display Command section of this guide) 
that share that tag. To add tag(s) to a Goal, enter the following command:
::

   goal-tag goal-number [tag, tag2]


Deleting a Tag
==============
(gdt, goal-delete-tag)

A specific tag can be deleted from a Goal by using it as the keyword in the command to follow, or all tags for that Goal 
can be deleted by using the keyword 'all':
::

   gdt goal-number [keyword]


Changing a Percentage
=====================
(gp, goal-percentage)
Beneath a Goal there is the option to have a progress bar indicating how close the Goal is to being complete - this is where the percentage 
comes in. By default, percentages are set to 'auto', allowing the number of Subgoals completed and still to do 
determine the percentage completion, but custom percentages can be added using the following command:
::

   goal-percentage goal-number [percentage]

Note that in order to restore the default 'auto' percentage setting one simply has to enter 'auto'(without the quotes) as the value 
either on the command line or at the prompt and to disable the progress bar simply enter 'none' as the value.
