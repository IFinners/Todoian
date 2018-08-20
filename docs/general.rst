=========================
General Usage Information
=========================

Synonyms
========

All commands have shorter synonyms, for example 'a' can be used instead or 'add', and once a synonym is mentioned one can assume it works for any given example even if not explicitly stated.


The Two Types of Optional Arguments
===================================

Optional arguments are shown by square brackets ([]) or curly brackets ({}) throughout this command guide.
Arguments in square brackets, if not given, will be asked for through a seperate prompt before the operation can be
completed whereas ones in curly brackets will be automatically set to a default - for example:
::

   add ["New Task Description"] {Date} {Repeat}

The user will be prompted for a task description if one isn't provided but both the Date and the Repeat will be
set to their default values - today's date and no repeat respectively.
