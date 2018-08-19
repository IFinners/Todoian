#!/usr/bin/env python3

import unittest
from unittest import mock
from datetime import datetime as dt
import classes
import todoian


class TestTaskMethods(unittest.TestCase):
    """Test the functions within the Task class."""

    def setUp(self):
        date = dt.strptime('2018-01-01', '%Y-%m-%d')
        self.task = classes.Task('Title', date, None, None)


    def test_edit_title(self):
        """Changing a Task's title to argument modifies .title correctly."""
        self.task.edit_title("Title Arg Test")
        self.assertEqual(self.task.title, "Title Arg Test")


    @mock.patch('classes.get_input')
    def test_edit_title_argless(self, mock_get_input):
        """Editing a Task's title modifies the attribute correctly."""
        mock_get_input.return_value = 'Task Title Test'
        self.task.edit_title()
        self.assertEqual(self.task.title, "Task Title Test")


    def test_edit_date(self):
        """Changing a Task's date to argument modifies date correctly."""
        self.task.edit_date("2018-12-31")
        self.assertEqual(self.task.date, dt.strptime('2018-12-31', '%Y-%m-%d'))


    @mock.patch('classes.get_input')
    def test_edit_date_argless(self, mock_get_input):
        """Editing a Task's date modifies the attribute correctly."""
        mock_get_input.return_value = '2018-12-12'
        self.task.edit_date()
        self.assertEqual(self.task.date, dt.strptime('2018-12-12', '%Y-%m-%d'))


    def test_edit_repeat(self):
        """Changing a Task's repeat to argument modifies repeat correctly."""
        self.task.edit_repeat('14')
        self.assertEqual(self.task.repeat, 14)


    @mock.patch('classes.get_input')
    def test_edit_repeat_int_argless(self, mock_get_input):
        """Editing a Task's repeat to an integer modifies the attribute correctly."""
        mock_get_input.return_value = '7'
        self.task.edit_repeat()
        self.assertEqual(self.task.repeat, 7)


    def test_edit_repeat_day_list(self):
        """Changing a Task's repeat to argument day list modifies repeat correctly."""
        self.task.edit_repeat('mon, wed, fri')
        self.assertEqual(self.task.repeat, {'mon', 'wed', 'fri'})


    @mock.patch('classes.get_input')
    def test_edit_repeat_day_list_argless(self, mock_get_input):
        """Editing a Task's repeat to a day list modifies the attribute correctly."""
        mock_get_input.return_value = 'tue, thur, sat, sun'
        self.task.edit_repeat()
        self.assertEqual(self.task.repeat, {'tue', 'thur', 'sat', 'sun'})


    def test_add_tag(self):
        """Changing a Task's tag to argument modifies tags correctly."""
        self.task.add_tag("tag")
        self.assertEqual(self.task.tags, ['tag'])


    def test_add_multiple_tags(self):
        """Changing a Task's tag to listed argument modifies tags correctly."""
        self.task.add_tag("tag,tag2,tag3")
        self.assertEqual(self.task.tags, ['tag', 'tag2', 'tag3'])


    @mock.patch('classes.get_input')
    def test_add_tag_argless(self, mock_get_input):
        """Adding a new tag to a Task appends the new value correctly."""
        self.task.tags = []
        mock_get_input.return_value = 'tag2'
        self.task.add_tag()
        self.assertEqual(self.task.tags, ['tag2'])


    @mock.patch('classes.get_input')
    def test_add_multiple_tags_argless(self, mock_get_input):
        """Adding new tags to a Task appends the new values correctly."""
        self.task.tags = []
        mock_get_input.return_value = 'tag1,tag2,tag3'
        self.task.add_tag()
        self.assertEqual(self.task.tags, ['tag1', 'tag2', 'tag3'])


    def test_remove_tag(self):
        """Changing a Task's tag to argument modifies tags correctly."""
        self.task.tags = ['tag', 'tag2']
        self.task.remove_tag("tag")
        self.assertEqual(self.task.tags, ['tag2'])


    @mock.patch('classes.get_input')
    def test_remove_tag_argless(self, mock_get_input):
        """Removing a tag successfully removes the named tag from the list."""
        self.task.tags = ['tag', 'tag2']
        mock_get_input.return_value = 'tag'
        self.task.remove_tag()
        self.assertEqual(self.task.tags, ['tag2'])


    def test_add_sub(self):
        """Adding a sub to a Task via an argument modifies subs correctly."""
        self.task.subs = []
        self.task.add_sub("sub")
        self.assertIsInstance(self.task.subs[0], classes.Sub)


    @mock.patch('classes.get_input')
    def test_add_sub_argless(self, mock_get_input):
        """Adding a sub to a Task results in a new Sub object in sub list."""
        self.task.subs = []
        mock_get_input.return_value = 'sub'
        self.task.add_sub()
        self.assertIsInstance(self.task.subs[0], classes.Sub)
        self.assertTrue(len(self.task.subs) == 1)


    def test_remove_sub(self):
        """Removing a sub of a Task via an argument modifies subs correctly."""
        self.task.subs = [classes.Sub('sub', 1), classes.Sub('sub2', 2)]
        self.task.remove_sub(1)
        self.assertTrue(len(self.task.subs) == 1)
        self.assertTrue(self.task.subs[0].title == 'sub2')


    @mock.patch('classes.get_input')
    def test_remove_sub_argless(self, mock_get_input):
        """Removing a sub by index removes the correct Sub from the sub list."""
        self.task.subs = [classes.Sub('sub1', 1), classes.Sub('sub2', 2)]
        mock_get_input.return_value = 2
        self.task.remove_sub()
        self.assertTrue(len(self.task.subs) == 1)


    def test_remove_sub_all(self):
        """Removing all subs of a Task via argument modifies subs correctly."""
        self.task.subs = [classes.Sub('sub', 1), classes.Sub('sub2', 2)]
        self.task.remove_sub('all')
        self.assertFalse(self.task.subs)


    @mock.patch('classes.get_input')
    def test_remove_sub_all_argless(self, mock_get_input):
        """Removing all subs results in an empty sub list."""
        self.task.subs = [classes.Sub('sub1', 1), classes.Sub('sub2', 2)]
        mock_get_input.return_value = 'all'
        self.task.remove_sub()
        self.assertEqual(self.task.subs, [])


    def test_toggle_sub_false_true(self):
        """Removing a sub of a Task via an argument modifies subs correctly."""
        self.task.subs = [classes.Sub('sub', 1)]
        self.task.toggle_sub(1)
        self.assertTrue(self.task.subs[0].completed == True)


    @mock.patch('classes.get_input')
    def test_toggle_sub_false_true_argless(self, mock_get_input):
        """Toggling a sub changes its completed from False to True."""
        self.task.subs = [classes.Sub('sub', 1)]
        mock_get_input.return_value = 1
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, True)


    def test_toggle_sub_true_false(self):
        """Toggling a sub changes its completed from True to False."""
        self.task.subs = [classes.Sub('sub', 1, completed=True)]
        self.task.toggle_sub(1)
        self.assertTrue(self.task.subs[0].completed == False)


    @mock.patch('classes.get_input')
    def test_toggle_sub_true_false_argless(self, mock_get_input):
        """Toggling a sub changes its completed from True to False."""
        self.task.subs = [classes.Sub('sub', 1, completed=True)]
        mock_get_input.return_value = 1
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, False)


    def test_toggle_sub_done(self):
        """Toggling subs with 'done' arg changes all completed to True."""
        self.task.subs = [classes.Sub('sub', 1), classes.Sub('sub1', 2)]
        self.task.toggle_sub('done')
        self.assertEqual(self.task.subs[0].completed, True)
        self.assertEqual(self.task.subs[1].completed, True)


    @mock.patch('classes.get_input')
    def test_toggle_sub_done_argless(self, mock_get_input):
        """Toggling subs with 'done' prompt changes all completed to True."""
        self.task.subs = [classes.Sub('sub', 1), classes.Sub('sub1', 2)]
        mock_get_input.return_value = 'done'
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, True)
        self.assertEqual(self.task.subs[1].completed, True)


    def test_toggle_sub_todo(self):
        """Toggling subs with 'todo' arg changes all completed to True."""
        self.task.subs = [classes.Sub('sub', 1, completed=True), classes.Sub('sub1', 2, completed=True)]
        self.task.toggle_sub('todo')
        self.assertEqual(self.task.subs[0].completed, False)
        self.assertEqual(self.task.subs[1].completed, False)


    @mock.patch('classes.get_input')
    def test_toggle_sub_todo_argless(self, mock_get_input):
        """Toggling subs with 'todo' prompt changes all completed attributes to False."""
        self.task.subs = [classes.Sub('sub', 1, completed=True), classes.Sub('sub1', 2, completed=True)]
        mock_get_input.return_value = 'todo'
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, False)
        self.assertEqual(self.task.subs[1].completed, False)


class TestGoalMethods(unittest.TestCase):
    """Test the add_task function within the todoian module."""

    def setUp(self):
        self.goal = classes.Goal('Goal', None, None, percentage='auto')


    def test_edit_percentage_arg(self):
        """Test editing a Goal's .percentage with an argument"""
        self.goal.edit_percentage(50)
        self.assertEqual(self.goal.percentage, 50)


    @mock.patch('classes.get_input')
    def test_edit_percentage_argless(self, mock_get_input):
        """Editing a Goal's .percentage without an argument."""
        mock_get_input.return_value = 75
        self.goal.edit_percentage()
        self.assertEqual(self.goal.percentage, 75)


    def test_auto_percentage_no_subs(self):
        """Auto percentage calculation when there are no subs."""
        self.assertEqual(self.goal.auto_percentage(), 0)


    def test_auto_percentage_subs_none_done(self):
        """Auto percentage return when there are subs but non are completed."""
        self.goal.subs = [classes.Sub('Sub1', 1), classes.Sub('Sub2', 2)]
        self.assertEqual(self.goal.auto_percentage(), 0)


    def test_auto_percentage_subs_half_done(self):
        """Auto percentage return when half of the subs are completed."""
        self.goal.subs = [classes.Sub('Sub1', 1, completed=True),
                          classes.Sub('Sub2', 2)]
        self.assertEqual(self.goal.auto_percentage(), 50)


    def test_auto_percentage_subs_all_done(self):
        """Auto percentage return when all of the subs are completed."""
        self.goal.subs = [classes.Sub('Sub1', 1, completed=True),
                          classes.Sub('Sub2', 2, completed=True)]
        self.assertEqual(self.goal.auto_percentage(), 100)


class TestAddTask(unittest.TestCase):
    """Test the add_task function within the todoian module."""

    def setUp(self):
        classes.Task.tasks = []
        todoian.current_date = dt.strptime('2018-01-01', '%Y-%m-%d')


    def test_add_task_no_arguments(self):
        """Adding task with no optional args creates Task with right mocked .date."""
        todoian.add_task('Title')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, todoian.current_date)
        self.assertEqual(classes.Task.tasks[0].repeat, None)
        self.assertEqual(classes.Task.tasks[0].tags, [])


    def test_add_task_date_argument(self):
        """Adding task with Date arg creates Task with right date."""
        todoian.add_task('Title ~~ d=2018-12-31')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, dt.strptime('2018-12-31', '%Y-%m-%d'))
        self.assertEqual(classes.Task.tasks[0].repeat, None)
        self.assertEqual(classes.Task.tasks[0].tags, [])


    def test_add_task_repeat_int_argument(self):
        """Adding task with repeat arg creates Task with right repeat."""
        todoian.add_task('Title ~~ r=7')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, todoian.current_date)
        self.assertEqual(classes.Task.tasks[0].repeat, 7)
        self.assertEqual(classes.Task.tasks[0].tags, [])


    def test_add_task_repeat_day_list_argument(self):
        """Adding task with repeat arg creates Task with right repeat."""
        todoian.add_task('Title ~~ r=mon,wed,fri')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, todoian.current_date)
        self.assertEqual(classes.Task.tasks[0].repeat, {'mon', 'wed', 'fri'})
        self.assertEqual(classes.Task.tasks[0].tags, [])


    def test_add_task_tag_argument(self):
        """Adding task with tag arg creates Task with right tags."""
        todoian.add_task('Title ~~ t=Test')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, todoian.current_date)
        self.assertEqual(classes.Task.tasks[0].repeat, None)
        self.assertEqual(classes.Task.tasks[0].tags, ['Test'])


    def test_add_task_multiple_tags_argument(self):
        """Adding task with a list of tags creates Task with right tags."""
        todoian.add_task('Title ~~ t=Tag1,Tag2,Tag3')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, todoian.current_date)
        self.assertEqual(classes.Task.tasks[0].repeat, None)
        self.assertEqual(classes.Task.tasks[0].tags, ['Tag1', 'Tag2', 'Tag3'])


    def test_add_task_all_arguments(self):
        """Adding task with all arg creates Task with right attributes."""
        todoian.add_task('Title ~~ d=2018-12-31 r=7 t=Test')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, dt.strptime('2018-12-31', '%Y-%m-%d'))
        self.assertEqual(classes.Task.tasks[0].repeat, 7)
        self.assertEqual(classes.Task.tasks[0].tags, ['Test'])


class TestDeleteTask(unittest.TestCase):
    """Test the delete_task function within the todoian module."""

    def setUp(self):
        classes.Task.tasks = [classes.Task('Task1', '2018-01-01', None, None),
                              classes.Task('Task2', '2018-01-01', None, None)]
        todoian.deleted_tasks = []


    def test_delete_task_int(self):
        """Deleting task with an int arg deletes one Task at correct index."""
        todoian.delete_task(1)
        self.assertEqual(classes.Task.tasks[0].title, 'Task2')
        self.assertTrue(len(todoian.deleted_tasks) == 1)
        self.assertIsInstance(todoian.deleted_tasks[0], classes.Task)


    @mock.patch('classes.get_input')
    def test_delete_task_all(self, mock_get_input):
        """Deleting task with 'all' arg deletes all Tasks."""
        mock_get_input.return_value = 'y'
        todoian.delete_task('all')
        self.assertFalse(classes.Task.tasks)
        self.assertTrue(len(todoian.deleted_tasks) == 2)
        self.assertIsInstance(todoian.deleted_tasks[0], classes.Task)
        self.assertIsInstance(todoian.deleted_tasks[1], classes.Task)


class TestCompleteTask(unittest.TestCase):
    """Test the complete_task function within the todoian module."""

    def setUp(self):
        date = dt.strptime('2018-01-01', '%Y-%m-%d')
        classes.Task.tasks = [classes.Task('Task1', date, None, None),
                              classes.Task('Task2', date, 7, None),
                              classes.Task('Task2', dt.now(), {'mon', 'fri'}, None)]
        todoian.completed_tasks = []


    def test_complete_task_int_no_repeat(self):
        """Completing repeatless task with an int arg moves the correct Task to cache."""
        todoian.complete_task(1)
        self.assertTrue(len(classes.Task.tasks) == 2)
        self.assertEqual(classes.Task.tasks[0].title, 'Task2')
        self.assertTrue(todoian.completed_tasks)


    def test_complete_task_int_with_int_repeat(self):
        """Completing task with a repeat redates the Task correctly."""
        todoian.complete_task(2)
        self.assertTrue(len(classes.Task.tasks) == 3)
        self.assertEqual(classes.Task.tasks[1].date, dt.strptime('2018-01-08', '%Y-%m-%d'))
        self.assertFalse(todoian.completed_tasks)


    def test_complete_task_int_with_named_repeats(self):
        """Completing task with a day name(s) repeat redates Task correctly."""
        repeat_days = ['mon', 'fri']
        today = dt.strftime(classes.Task.tasks[2].date, '%a').lower()
        todoian.complete_task(3)
        next_day = dt.strftime(classes.Task.tasks[2].date, '%a').lower()
        self.assertTrue(next_day in repeat_days)
        self.assertTrue(next_day != today)
        self.assertFalse(todoian.completed_tasks)


class TestCompleteToday(unittest.TestCase):
    """Test the complete_today function within the todoian module."""

    def setUp(self):
        over = dt.strptime('2017-12-01', '%Y-%m-%d')
        date = dt.strptime('2018-01-01', '%Y-%m-%d')
        future = dt.strptime('2018-01-05', '%Y-%m-%d')
        classes.Task.tasks = [classes.Task('Task1', over, None, None, num=1),
                              classes.Task('Task2', date, None, None, num=2),
                              classes.Task('Task3', date, 7, None, num=3),
                              classes.Task('Task4', future, None, None, num=4)]
        todoian.completed_tasks = []


    def test_complete_today(self):
        """All tasks dated today are completed and repetition calculated if present."""
        todoian.complete_today()
        self.assertTrue(len(classes.Task.tasks) == 3)
        self.assertEqual(todoian.completed_tasks[0].title, 'Task2')
        self.assertEqual(classes.Task.tasks[2].title, 'Task3')
        self.assertEqual(classes.Task.tasks[0].title, 'Task1')


class TestCompleteOverdue(unittest.TestCase):
    """Test the complete_overdue function within the todoian module."""

    def setUp(self):
        over = dt.strptime('2017-12-01', '%Y-%m-%d')
        date = dt.strptime('2018-01-01', '%Y-%m-%d')
        future = dt.strptime('2018-01-05', '%Y-%m-%d')
        classes.Task.tasks = [classes.Task('Task1', over, None, None, num=1),
                              classes.Task('Task2', over, 2, None, num=2),
                              classes.Task('Task3', date, 7, None, num=3),
                              classes.Task('Task4', future, None, None, num=4)]
        todoian.completed_tasks = []


    def test_complete_overdue(self):
        """All overdue Tasks completed and ones with repeats completed until no longer overdue"""
        todoian.complete_overdue()
        self.assertTrue(len(classes.Task.tasks) == 3)
        self.assertEqual(todoian.completed_tasks[0].title, 'Task1')
        self.assertEqual(classes.Task.tasks[1].title, 'Task2')
        self.assertEqual(classes.Task.tasks[0].title, 'Task3')


class TestAddGoal(unittest.TestCase):
    """Test the add_goal function within the todoian module."""

    def setUp(self):
        classes.Goal.goals = []

    def test_add_goal_no_arguments(self):
        """Adding goal with no optional args creates Goal with right title."""
        todoian.add_goal('Goal')
        self.assertEqual(classes.Goal.goals[0].title, 'Goal')
        self.assertEqual(classes.Goal.goals[0].date, None)
        self.assertEqual(classes.Goal.goals[0].tags, [])
        self.assertTrue(len(classes.Goal.goals) == 1)


    def test_add_goal_date_argument(self):
        """Adding goal with date arg creates Goal with right date."""
        todoian.add_goal('Goal ~~ d=Next Week')
        self.assertEqual(classes.Goal.goals[0].title, 'Goal')
        self.assertEqual(classes.Goal.goals[0].date, 'Next Week')
        self.assertEqual(classes.Goal.goals[0].tags, [])
        self.assertTrue(len(classes.Goal.goals) == 1)


    def test_add_goal_tag_argument(self):
        """Adding goal with tag arg with single tag creates Goal with right tags."""
        todoian.add_goal('Goal ~~ t=Test')
        self.assertEqual(classes.Goal.goals[0].title, 'Goal')
        self.assertEqual(classes.Goal.goals[0].date, None)
        self.assertEqual(classes.Goal.goals[0].tags, ['Test'])
        self.assertTrue(len(classes.Goal.goals) == 1)


    def test_add_goal_tag_argument_multiple_tags(self):
        """Adding goal with tag arg with single tag creates Goal with right tags."""
        todoian.add_goal('Goal ~~ t=Test, Test2, Test3')
        self.assertEqual(classes.Goal.goals[0].title, 'Goal')
        self.assertEqual(classes.Goal.goals[0].date, None)
        self.assertEqual(classes.Goal.goals[0].tags, ['Test', 'Test2', 'Test3'])
        self.assertTrue(len(classes.Goal.goals) == 1)


class TestDeleteGoal(unittest.TestCase):
    """Test the delete_goal function within the todoian module."""

    def setUp(self):
        classes.Goal.goals = [classes.Goal('Goal1', None, None),
                              classes.Goal('Goal2', None, None)]
        todoian.deleted_goals = []


    def test_delete_goal_int(self):
        """Deleting Goal with an int arg deletes one Goal at correct index."""
        todoian.delete_goal(1)
        self.assertEqual(classes.Goal.goals[0].title, 'Goal2')
        self.assertTrue(len(todoian.deleted_goals) == 1)
        self.assertIsInstance(todoian.deleted_goals[0], classes.Goal)


    @mock.patch('classes.get_input')
    def test_delete_goal_all(self, mock_get_input):
        """Deleting Goal with 'all' arg deletes all Goals."""
        mock_get_input.return_value = 'y'
        todoian.delete_goal('all')
        self.assertFalse(classes.Goal.goals)
        self.assertTrue(len(todoian.deleted_goals) == 2)
        self.assertIsInstance(todoian.deleted_goals[0], classes.Goal)
        self.assertIsInstance(todoian.deleted_goals[1], classes.Goal)


class TestCompleteGoal(unittest.TestCase):
    """Test the complete_task function within the todoian module."""

    def setUp(self):
        classes.Goal.goals = [classes.Goal('Goal1', None, None),
                              classes.Goal('Goal2', None, None)]
        todoian.completed_goals = []


    def test_complete_goal_int(self):
        """Completing Goal with an int arg moves the correct Goal to cache."""
        todoian.complete_goal(1)
        self.assertTrue(len(classes.Goal.goals) == 1)
        self.assertEqual(classes.Goal.goals[0].title, 'Goal2')
        self.assertTrue(todoian.completed_goals)


class TestCacheRetrival(unittest.TestCase):
    """Test the cache_retrival function within the todoian module."""

    def setUp(self):
        classes.Task.tasks = [classes.Task('Retrieve', 'date', None, None)]
        classes.Goal.goals = [classes.Goal('Goal Retrieve', None, None)]
        todoian.deleted_tasks = []
        todoian.completed_tasks = []
        todoian.deleted_goals = []
        todoian.completed_goals = []


    def test_delete_task_retrival(self):
        """cache_retrival from deleted_tasks moves Task object back into tasks."""
        todoian.deleted_tasks.append(classes.Task.tasks.pop())
        todoian.cache_retrival(todoian.deleted_tasks, classes.Task.tasks)
        self.assertTrue(len(todoian.deleted_tasks) == 0)
        self.assertTrue(len(classes.Task.tasks) == 1)
        self.assertIsInstance(classes.Task.tasks[0], classes.Task)


    def test_complete_task_retrival(self):
        """cache_retrival from deleted_tasks moves Task object back into tasks."""
        todoian.completed_tasks.append(classes.Task.tasks.pop())
        todoian.cache_retrival(todoian.completed_tasks, classes.Task.tasks)
        self.assertTrue(len(todoian.completed_tasks) == 0)
        self.assertTrue(len(classes.Task.tasks) == 1)
        self.assertIsInstance(classes.Task.tasks[0], classes.Task)


    def test_delete_goal_retrival(self):
        """cache_retrival from deleted_goals moves Goal object back into goals."""
        todoian.deleted_goals.append(classes.Goal.goals.pop())
        todoian.cache_retrival(todoian.deleted_goals, classes.Goal.goals)
        self.assertTrue(len(todoian.deleted_goals) == 0)
        self.assertTrue(len(classes.Goal.goals) == 1)
        self.assertIsInstance(classes.Goal.goals[0], classes.Goal)


    def test_complete_goal_retrival(self):
        """cache_retrival from deleted_goals moves Goal object back into goals."""
        todoian.completed_goals.append(classes.Goal.goals.pop())
        todoian.cache_retrival(todoian.completed_goals, classes.Goal.goals)
        self.assertTrue(len(todoian.completed_goals) == 0)
        self.assertTrue(len(classes.Goal.goals) == 1)
        self.assertIsInstance(classes.Goal.goals[0], classes.Goal)


class TestMoveItem(unittest.TestCase):
    """Test the move_item function within the todoian module."""

    def setUp(self):
        classes.Task.tasks = [classes.Task('Task1', 'date', None, None),
                              classes.Task('Task2', 'date', None, None)]
        classes.Goal.goals = [classes.Goal('Goal1', None, None),
                              classes.Goal('Goal2', None, None)]


    def test_move_task(self):
        """Move given Task.tasks moves Task correctly."""
        todoian.move_item('2 1', classes.Task.tasks)
        self.assertEqual(classes.Task.tasks[0].title, 'Task2')


    def test_move_goal(self):
        """Move given Goal.goals moves Goal correctly."""
        todoian.move_item('2 1', classes.Goal.goals)
        self.assertEqual(classes.Goal.goals[0].title, 'Goal2')


    def test_move_subtask(self):
        """Move given Task.tasks with 3 spaced ints moves Subtask correctly."""
        classes.Task.tasks[0].subs = [classes.Sub('Sub1', 1), classes.Sub('Sub2', 2)]
        todoian.move_item('1 2 1', classes.Task.tasks)
        self.assertEqual(classes.Task.tasks[0].subs[0].title, 'Sub2')


    def test_move_subgoal(self):
        """Move given Goal.goals with 2 spaced ints moves Subgoal correctly."""
        classes.Goal.goals[0].subs = [classes.Sub('Sub1', 1), classes.Sub('Sub2', 2)]
        todoian.move_item('1 2 1', classes.Goal.goals)
        self.assertEqual(classes.Goal.goals[0].subs[0].title, 'Sub2')


if __name__ == '__main__':
    unittest.main(buffer=True)
