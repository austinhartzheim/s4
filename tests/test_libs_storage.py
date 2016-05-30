import unittest
import os

import libs.storage
import libs.errors


class TestS4Project(unittest.TestCase):

    @unittest.mock.patch('os.path.exists')
    def test_create_by_search_bad_path(self, mock_os_path_exists):
        '''
        Test that when a .s4 directory cannot be found, NotInS4Project
        is raised.
        '''
        BAD_PATH = '/tmp/a/b/c/d/'
        mock_os_path_exists.return_value = False
        self.assertRaises(libs.errors.NotInS4Project,
                          libs.storage.S4Project.create_by_search, BAD_PATH)

    @unittest.mock.patch('os.path.exists')
    def test_create_by_search_good_path(self, mock_os_path_exists):
        '''
        Test that when a .s4 directory is found, an instance of S4Project
        is returned.
        '''
        GOOD_PATH = '/tmp/a/b/c/d/'
        mock_os_path_exists.return_value = True
        result = libs.storage.S4Project.create_by_search(GOOD_PATH)
        self.assertIsInstance(result, libs.storage.S4Project)

    @unittest.mock.patch('os.path.exists')
    def test_create_by_search_return_object(self, mock_os_path_exists):
        '''
        Test that the data stored in the returned S4Project object is
        valid, including a string path ending in .s4.
        '''
        GOOD_PATH = '/tmp/a/b/c/d/'
        mock_os_path_exists.return_value = True
        s4proj = libs.storage.S4Project.create_by_search(GOOD_PATH)

        # Test that `s4path` is set correctly
        self.assertTrue(hasattr(s4proj, 's4path'),
                        'S4Project object is missing path attribute')
        self.assertEqual(os.path.split(s4proj.s4path)[1], '.s4')
        self.assertIn(GOOD_PATH, s4proj.s4path)

        # Test that `path` is set correctly
        self.assertTrue(hasattr(s4proj, 'path'))
        self.assertEqual(s4proj.path.rstrip('/'), GOOD_PATH.rstrip('/'))
