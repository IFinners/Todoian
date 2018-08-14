import unittest
from unittest import mock
import classes


class TestTaskFunctions(unittest.TestCase):
    """Test the functions within the Task class."""
    
    task = classes.Task('Initial Description', '2018-01-01')
    
    def test_edit_desc(self):
        """."""
        description = 'Test Description'
        self.task.edit_description(new_desc=description)
        self.assertEqual(self.task.description, description)
    
    
    @mock.patch('classes.get_input')
    def test_edit_desc_argless(self, mock_get_input):
        """."""
        mock_get_input.return_value = 'Input Description Test'
        self.task.edit_description()
        self.assertEqual(self.task.description, "Input Description Test")
        
    
    def test_edit_due(self):
        """."""
        new_date = '2018-12-25'
        self.task.edit_due(new_due=new_date)
        self.assertEqual(self.task.due_date, new_date)
    
    
    @mock.patch('classes.get_input')
    def test_edit_due_argless(self, mock_get_input):
        """."""
        mock_get_input.return_value = '2018-12-12'
        self.task.edit_due()
        self.assertEqual(self.task.due_date, '2018-12-12')


    def test_edit_repeat(self):
        """."""
        new_repeat = 3
        self.task.edit_repeat(new_rep=new_repeat)
        self.assertEqual(self.task.repeat, new_repeat)
    
    
    @mock.patch('classes.get_input')
    def test_edit_repeat_argless(self, mock_get_input):
        """."""
        mock_get_input.return_value = 7
        self.task.edit_repeat()
        self.assertEqual(self.task.repeat, 7)

    
    def test_add_tag(self):
        """."""
        new_tag = 'tag'
        self.task.add_tag(new_tag=new_tag)
        self.assertEqual(self.task.tags, [new_tag])

    
    @mock.patch('classes.get_input')
    def test_add_tag_argless(self, mock_get_input):
        """."""
        self.task.tags = []
        mock_get_input.return_value = 'tag2'
        self.task.add_tag()
        self.assertEqual(self.task.tags, ['tag2'])


    def test_remove_tag(self):
        """."""
        self.task.tags = ['tag', 'tag2']
        to_remove = 'tag2'
        self.task.remove_tag(tag=to_remove)
        self.assertEqual(self.task.tags, ['tag'])
    
    
    def test_remove_tag_all(self):
        """."""
        self.task.tags = ['tag', 'tag2']
        self.task.remove_tag(del_all=True)
        self.assertEqual(self.task.tags, [])
    
    
    @mock.patch('classes.get_input')
    def test_remove_tag_argless(self, mock_get_input):
        """."""
        self.task.tags = ['tag', 'tag2']
        mock_get_input.return_value = 'tag'
        self.task.remove_tag()
        self.assertEqual(self.task.tags, ['tag2'])
        

    def test_add_sub(self):
        """."""
        new_sub = 'sub'
        self.task.add_sub(sub=new_sub)
        self.assertEqual(self.task.subs, [new_sub])


    @mock.patch('classes.get_input')
    def test_add_sub_argless(self, mock_get_input):
        """."""
        self.task.subs = []
        mock_get_input.return_value = 'sub2'
        self.task.add_sub()
        self.assertEqual(self.task.subs, ['sub2'])


    def test_remove_sub(self):
        """."""
        self.task.subs = ['sub', 'sub1']
        num = 1
        self.task.remove_sub(sub_num=num)
        self.assertEqual(self.task.subs, ['sub1'])

    
    def test_remove_sub_all(self):
        """."""
        self.task.subs = ['sub', 'sub2']
        self.task.remove_sub(del_all=True)
        self.assertEqual(self.task.subs, [])


    @mock.patch('classes.get_input')
    def test_remove_sub_argless(self, mock_get_input):
        """."""
        self.task.subs = ['sub', 'sub2']
        mock_get_input.return_value = 2
        self.task.remove_sub()
        self.assertEqual(self.task.subs, ['sub'])

     



if __name__ == '__main__':
    unittest.main()
