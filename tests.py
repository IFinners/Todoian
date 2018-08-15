import unittest
from unittest import mock
import classes


class TestTaskFunctions(unittest.TestCase):
    """Test the functions within the Task class."""

    task = classes.Task('Initial Description', '2018-01-01', None)

    @mock.patch('classes.get_input')
    def test_edit_desc(self, mock_get_input):
        """Test editing a task description modifies the attribute correctly."""
        mock_get_input.return_value = 'Task Description Test'
        self.task.edit_title()
        self.assertEqual(self.task.title, "Task Description Test")


    @mock.patch('classes.get_input')
    def test_edit_date(self, mock_get_input):
        """Test editing a task date modifies the attribute correctly."""
        mock_get_input.return_value = '2018-12-12'
        self.task.edit_date()
        self.assertEqual(self.task.date, '2018-12-12')


    @mock.patch('classes.get_input')
    def test_edit_repeat_int(self, mock_get_input):
        """Test editing a task repeat to an integer modifies the attribute correctly."""
        mock_get_input.return_value = 7
        self.task.edit_repeat()
        self.assertEqual(self.task.repeat, 7)


    @mock.patch('classes.get_input')
    def test_add_tag(self, mock_get_input):
        """Test adding a new tag to a task appends the new value correctly."""
        self.task.tags = []
        mock_get_input.return_value = 'tag2'
        self.task.add_tag()
        self.assertEqual(self.task.tags, ['tag2'])


    @mock.patch('classes.get_input')
    def test_remove_tag(self, mock_get_input):
        """Test removing a tag successfully removes the named tag from the list."""
        self.task.tags = ['tag', 'tag2']
        mock_get_input.return_value = 'tag'
        self.task.remove_tag()
        self.assertEqual(self.task.tags, ['tag2'])


    @mock.patch('classes.get_input')
    def test_add_sub(self, mock_get_input):
        """Test adding a sub to a task results in a new Sub object in sub list."""
        self.task.subs = []
        mock_get_input.return_value = 'sub2'
        self.task.add_sub()
        self.assertIsInstance(self.task.subs[0], classes.Sub)


    @mock.patch('classes.get_input')
    def test_remove_sub(self, mock_get_input):
        """Test removing a sub by index removes the correct Sub from the sub list."""
        self.task.subs = [classes.Sub('sub1', 1), classes.Sub('sub2', 2)]
        mock_get_input.return_value = 2
        self.task.remove_sub()
        self.assertTrue(len(self.task.subs) == 1)


    @mock.patch('classes.get_input')
    def test_remove_sub_all(self, mock_get_input):
        """Test removing all subs results in an empty sub list."""
        self.task.subs = [classes.Sub('sub1', 1), classes.Sub('sub2', 2)]
        mock_get_input.return_value = 'all'
        self.task.remove_sub()
        self.assertEqual(self.task.subs, [])


    @mock.patch('classes.get_input')
    def test_toggle_sub_False_True(self, mock_get_input):
        """Test toggling a sub changes its completed attribute from False to True."""
        self.task.subs = [classes.Sub('sub', 1)]
        mock_get_input.return_value = 1
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, True)


    @mock.patch('classes.get_input')
    def test_toggle_sub_True_False(self, mock_get_input):
        """Test toggling a sub changes its completed attribute from True to False."""
        self.task.subs = [classes.Sub('sub', 1, completed=True)]
        mock_get_input.return_value = 1
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, False)


    @mock.patch('classes.get_input')
    def test_toggle_sub_done(self, mock_get_input):
        """Test toggling subs with done prompt changes all completed attributes to True."""
        self.task.subs = [classes.Sub('sub', 1), classes.Sub('sub1', 2)]
        mock_get_input.return_value = 'done'
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, True)
        self.assertEqual(self.task.subs[1].completed, True)


    @mock.patch('classes.get_input')
    def test_toggle_sub_not(self, mock_get_input):
        """Test toggling subs with 'not' prompt changes all completed attributes to False."""
        self.task.subs = [classes.Sub('sub', 1, completed=True), classes.Sub('sub1', 2, completed=True)]
        mock_get_input.return_value = 'not'
        self.task.toggle_sub()
        self.assertEqual(self.task.subs[0].completed, False)
        self.assertEqual(self.task.subs[1].completed, False)







if __name__ == '__main__':
    unittest.main()
