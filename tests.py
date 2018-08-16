#!/usr/bin/env python3

import unittest
from unittest import mock
import classes
import todoian


class TestTaskFunctions(unittest.TestCase):
    """Test the functions within the Task class."""

    def setUp(self):
        self.task = classes.Task('Title', '2018-01-01', None, None)

    def test_edit_title(self):
        """Test changing a Task's title to argument modifies .title correctly."""
        self.task.edit_title("Title Arg Test")
        self.assertEqual(self.task.title, "Title Arg Test")


    @mock.patch('classes.get_input')
    def test_edit_title_argless(self, mock_get_input):
        """Test editing a Task's title modifies the attribute correctly."""
        mock_get_input.return_value = 'Task Title Test'
        self.task.edit_title()
        self.assertEqual(self.task.title, "Task Title Test")


    def test_edit_date(self):
        """Test changing a Task's date to argument modifies .date correctly."""
        self.task.edit_date("2018-12-31")
        self.assertEqual(self.task.date, "2018-12-31")


    @mock.patch('classes.get_input')
    def test_edit_date_argless(self, mock_get_input):
        """Test editing a Task's date modifies the attribute correctly."""
        mock_get_input.return_value = '2018-12-12'
        self.task.edit_date()
        self.assertEqual(self.task.date, '2018-12-12')


    def test_edit_repeat(self):
        """Test changing a Task's repeat to argument modifies .repeat correctly."""
        self.task.edit_repeat("14")
        self.assertEqual(self.task.repeat, "14")


    @mock.patch('classes.get_input')
    def test_edit_repeat_int_argless(self, mock_get_input):
        """Test editing a Task's repeat to an integer modifies the attribute correctly."""
        mock_get_input.return_value = 7
        self.task.edit_repeat()
        self.assertEqual(self.task.repeat, 7)


    def test_add_tag(self):
        """Test changing a Task's tag to argument modifies .tags correctly."""
        self.task.add_tag("tag")
        self.assertEqual(self.task.tags, ['tag'])


    @mock.patch('classes.get_input')
    def test_add_tag_argless(self, mock_get_input):
        """Test adding a new tag to a Task appends the new value correctly."""
        self.task.tags = []
        mock_get_input.return_value = 'tag2'
        self.task.add_tag()
        self.assertEqual(self.task.tags, ['tag2'])


    def test_remove_tag(self):
        """Test changing a Task's tag to argument modifies .tags correctly."""
        self.task.tags = ['tag', 'tag2']
        self.task.remove_tag("tag")
        self.assertEqual(self.task.tags, ['tag2'])


    @mock.patch('classes.get_input')
    def test_remove_tag_argless(self, mock_get_input):
        """Test removing a tag successfully removes the named tag from the list."""
        self.task.tags = ['tag', 'tag2']
        mock_get_input.return_value = 'tag'
        self.task.remove_tag()
        self.assertEqual(self.task.tags, ['tag2'])


    def test_add_sub(self):
        """Test adding a sub to a Task via an argument modifies .subs correctly."""
        self.task.subs = []
        self.task.add_sub("sub")
        self.assertIsInstance(self.task.subs[0], classes.Sub)


    @mock.patch('classes.get_input')
    def test_add_sub_argless(self, mock_get_input):
        """Test adding a sub to a Task results in a new Sub object in sub list."""
        self.task.subs = []
        mock_get_input.return_value = 'sub'
        self.task.add_sub()
        self.assertIsInstance(self.task.subs[0], classes.Sub)
        self.assertTrue(len(self.task.subs) == 1)


    def test_remove_sub(self):
        """Test removing a sub of a Task via an argument modifies .subs correctly."""
        self.task.subs = [classes.Sub('sub', 1), classes.Sub('sub2', 2)]
        self.task.remove_sub(1)
        self.assertTrue(len(self.task.subs) == 1)
        self.assertTrue(self.task.subs[0].title == 'sub2')


    @mock.patch('classes.get_input')
    def test_remove_sub_argless(self, mock_get_input):
        """Test removing a sub by index removes the correct Sub from the sub list."""
        self.task.subs = [classes.Sub('sub1', 1), classes.Sub('sub2', 2)]
        mock_get_input.return_value = 2
        self.task.remove_sub()
        self.assertTrue(len(self.task.subs) == 1)


    def test_remove_sub_all(self):
        """Test removing all subs of a Task via argument modifies .subs correctly."""
        self.task.subs = [classes.Sub('sub', 1), classes.Sub('sub2', 2)]
        self.task.remove_sub('all')
        self.assertFalse(self.task.subs)


    @mock.patch('classes.get_input')
    def test_remove_sub_all_argless(self, mock_get_input):
        """Test removing all subs results in an empty sub list."""
        self.task.subs = [classes.Sub('sub1', 1), classes.Sub('sub2', 2)]
        mock_get_input.return_value = 'all'
        self.task.remove_sub()
        self.assertEqual(self.task.subs, [])


    def test_toggle_sub_false_true(self):
        """Test removing a sub of a Task via an argument modifies .subs correctly."""
        self.task.subs = [classes.Sub('sub', 1)]
        self.task.toggle_sub(1)
        self.assertTrue(self.task.subs[0].completed == True)


    @mock.patch('classes.get_input')
    def test_toggle_sub_false_true_argless(self, mock_get_input):
        """Test toggling a sub changes its .completed from False to True."""
        self.task.subs = [classes.Sub('sub', 1)]
        mock_get_input.return_value = 1
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, True)


    def test_toggle_sub_true_false(self):
        """Test removing a sub of a Task via an argument modifies .subs correctly."""
        self.task.subs = [classes.Sub('sub', 1, completed=True)]
        self.task.toggle_sub(1)
        self.assertTrue(self.task.subs[0].completed == False)


    @mock.patch('classes.get_input')
    def test_toggle_sub_true_false_argless(self, mock_get_input):
        """Test toggling a sub changes its .completed from True to False."""
        self.task.subs = [classes.Sub('sub', 1, completed=True)]
        mock_get_input.return_value = 1
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, False)


    def test_toggle_sub_done(self):
        """Test toggling subs with 'done' arg changes all .completed to True."""
        self.task.subs = [classes.Sub('sub', 1), classes.Sub('sub1', 2)]
        self.task.toggle_sub('done')
        self.assertEqual(self.task.subs[0].completed, True)
        self.assertEqual(self.task.subs[1].completed, True)


    @mock.patch('classes.get_input')
    def test_toggle_sub_done_argless(self, mock_get_input):
        """Test toggling subs with 'done' prompt changes all .completed to True."""
        self.task.subs = [classes.Sub('sub', 1), classes.Sub('sub1', 2)]
        mock_get_input.return_value = 'done'
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, True)
        self.assertEqual(self.task.subs[1].completed, True)


    def test_toggle_sub_todo(self):
        """Test toggling subs with 'todo' arg changes all .completed to True."""
        self.task.subs = [classes.Sub('sub', 1, completed=True), classes.Sub('sub1', 2, completed=True)]
        self.task.toggle_sub('todo')
        self.assertEqual(self.task.subs[0].completed, False)
        self.assertEqual(self.task.subs[1].completed, False)


    @mock.patch('classes.get_input')
    def test_toggle_sub_todo_argless(self, mock_get_input):
        """Test toggling subs with 'todo' prompt changes all completed attributes to False."""
        self.task.subs = [classes.Sub('sub', 1, completed=True), classes.Sub('sub1', 2, completed=True)]
        mock_get_input.return_value = 'todo'
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, False)
        self.assertEqual(self.task.subs[1].completed, False)



class TestAddTask(unittest.TestCase):
    """Test the add_task function within the todoian module."""

    def setUp(self):
        classes.Task.tasks = []

    @mock.patch('todoian.current_date')
    def test_add_task_no_arguments(self, mock_current_date):
        """Test adding task with no optional args creates Task with right .title and mocked .date."""
        mock_current_date.return_value = '2018-01-01'
        todoian.add_task('Title')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, mock_current_date)
        self.assertEqual(classes.Task.tasks[0].repeat, None)
        self.assertEqual(classes.Task.tasks[0].tags, [])

    def test_add_task_date_argument(self):
        """Test adding task with Date arg creates Task with right .title and .date."""
        todoian.add_task('Title ~~ d=2018-12-31')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, '2018-12-31')
        self.assertEqual(classes.Task.tasks[0].repeat, None)
        self.assertEqual(classes.Task.tasks[0].tags, [])

    @mock.patch('todoian.current_date')
    def test_add_task_repeat_argument(self, mock_current_date):
        """Test adding task with repeat arg creates Task with right .title and .repeat."""
        mock_current_date.return_value = '2018-01-01'
        todoian.add_task('Title ~~ r=7')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, mock_current_date)
        self.assertEqual(classes.Task.tasks[0].repeat, '7')
        self.assertEqual(classes.Task.tasks[0].tags, [])

    @mock.patch('todoian.current_date')
    def test_add_task_tag_argument(self, mock_current_date):
        """Test adding task with tag arg creates Task with right .title and .tag."""
        mock_current_date.return_value = '2018-01-01'
        todoian.add_task('Title ~~ t=Test')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, mock_current_date)
        self.assertEqual(classes.Task.tasks[0].repeat, None)
        self.assertEqual(classes.Task.tasks[0].tags, ['Test'])

    def test_add_task_all_arguments(self):
        """Test adding task with all arg creates Task with right attributes."""
        todoian.add_task('Title ~~ d=2018-12-31 r=7 t=Test')
        self.assertEqual(classes.Task.tasks[0].title, 'Title')
        self.assertEqual(classes.Task.tasks[0].date, '2018-12-31')
        self.assertEqual(classes.Task.tasks[0].repeat, '7')
        self.assertEqual(classes.Task.tasks[0].tags, ['Test'])


class TestDeleteTask(unittest.TestCase):
    """Test the delete_task function within the todoian module."""

    def setUp(self):
        classes.Task.tasks = [classes.Task('Task1', '2018-01-01', None, None),
                              classes.Task('Task2', '2018-01-01', None, None)]
        todoian.deleted_tasks = []

    def test_delete_task_int(self):
        """Test deleting task with an int arg deletes one Task at correct index."""
        todoian.delete_task(1)
        self.assertEqual(classes.Task.tasks[0].title, 'Task2')
        self.assertTrue(len(todoian.deleted_tasks) == 1)
        self.assertIsInstance(todoian.deleted_tasks[0], classes.Task)

    @mock.patch('classes.get_input')
    def test_delete_task_all(self, mock_get_input):
        """Test deleting task with 'all' arg deletes all Tasks."""
        mock_get_input.return_value = 'y'
        todoian.delete_task('all')
        self.assertEqual(classes.Task.tasks, [])
        self.assertTrue(len(todoian.deleted_tasks) == 2)
        self.assertIsInstance(todoian.deleted_tasks[0], classes.Task)
        self.assertIsInstance(todoian.deleted_tasks[1], classes.Task)

    def test_delete_task_retrival(self):
        """Test cache_retrical from deleted_tasks moves Task object back into tasks."""
        todoian.delete_task(1)
        todoian.cache_retrival(todoian.deleted_tasks)
        self.assertTrue(len(todoian.deleted_tasks) == 0)
        self.assertTrue(len(classes.Task.tasks) == 2)
        self.assertIsInstance(classes.Task.tasks[1], classes.Task)
    


# class TestCompleteTask(unittest.TestCase):
#     """Test the complete_task function within the todoian module."""

#     def setUp(self):
#         classes.Task.tasks = [classes.Task('Task1', '2018-01-01', None, None),
#                               classes.Task('Task2', '2018-01-01', None, None),
#                               classes.Task('Task3', '2018-01-01', 7, None),
#                               classes.Task('Task4', '2018-01-01', None, None)]
#         todoian.completed_tasks = []

#     def test_complete_task_int(self):
#         """Test completing task with an int arg moves the correct Task to cache."""
#         todoian.complete_task(1)
#         self.assertTrue(len(classes.Task.tasks) == 3)
#         self.assertEqual(classes.Task.tasks[0].title, 'Task2')
#         self.assertEqual(todoian.completed_tasks[0].title, 'Task1')
    
#     @mock.patch('classes.get_input')
#     def test_complete_task_all(self, mock_get_input):
#         """Test complete task with 'all' arg deletes all Tasks."""
#         mock_get_input.return_value = 'y'
#         todoian.complete_task('all')
#         self.assertEqual(classes.Task.tasks, [])
#         self.assertTrue(len(todoian.completed_tasks) == 4)

    



if __name__ == '__main__':
    unittest.main()
