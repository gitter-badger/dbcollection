#!/usr/bin/env python3

"""
organize_list.py unit testing.
"""


import os
import sys
import numpy as np
import h5py

import unittest
from unittest import mock
from unittest.mock import patch, mock_open

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
sys.path.append(lib_path)
from dbcollection.organize_list import create_list_store_to_hdf5
from dbcollection.utils import convert_str_to_ascii


#-----------------------
# Unit Test definitions
#-----------------------

class OrganizeTest(unittest.TestCase):
    """
    Test class.
    """

    def setUp(self):
        """
        Initialize class.
        """
        # sample data
        self.sample_test_hdf_file = 'test_organize_list__valid_field.h5'

        sample_train_filename = convert_str_to_ascii(['fname1', 'fname2', 'fname3', \
                                    'fname4', 'fname5', 'fname6', \
                                    'fname7', 'fname8', 'fname9'])
        sample_train_class = convert_str_to_ascii(['class1', 'class2', 'class3', 'class4'])
        sample_train_object_fields = convert_str_to_ascii(['filename', 'class'])
        sample_train_object_id = np.array([[1, 1], [2, 1], [3, 1], \
                                           [4, 2], [5, 2], [6, 2], \
                                           [7, 3], [8, 3], [9, 3], \
                                          ])

        # check if the file exists on disk
        if os.path.exists(self.sample_test_hdf_file):
            os.remove(self.sample_test_hdf_file)

        # create a hdf5 data file
        self.data = h5py.File(self.sample_test_hdf_file, 'w', libver='latest')
        tr = self.data.create_group('train')
        tr.create_dataset('filename', data=sample_train_filename)
        tr.create_dataset('class', data=sample_train_class)
        tr.create_dataset('object_fields', data=sample_train_object_fields)
        tr.create_dataset('object_id', data=sample_train_object_id)


    def test_organize_list__valid_field_class(self):
        """
        Test organizing a list of a valid field.
        """
        # sample data
        storage = self.data
        set_name = 'train'
        field_name = 'class'
        field_pos = 1
        field_list = 'list_' + field_name
        expected_result = np.array([[1,2,3],[4,5,6],[7,8,9],[0,0,0]])

        # create an organized list for sample_field_name
        create_list_store_to_hdf5(storage[set_name], field_name, field_pos)

        # check if the field sample_field_list exists
        self.assertTrue(field_list in self.data['train'].keys(), '{}'.format(field_list))
        self.assertEqual(self.data['train'][field_list].value.tolist(), expected_result.tolist(), \
                         'expected equal result')


    def test_organize_list__valid_field_filename(self):
        """
        Test organizing a list of a valid field.
        """
        # sample data
        storage = self.data
        set_name = 'train'
        field_name = 'filename'
        field_pos = 0
        field_list = 'list_' + field_name
        expected_result = np.array([[1],[2],[3],[4],[5],[6],[7],[8],[9]])

        # create an organized list for sample_field_name
        create_list_store_to_hdf5(storage[set_name], field_name, field_pos)

        # check if the field sample_field_list exists
        self.assertTrue(field_list in self.data['train'].keys(), '{}'.format(field_list))
        self.assertEqual(self.data['train'][field_list].value.tolist(), expected_result.tolist(), \
                         'expected result different')


    def tearDown(self):
        """
        Remove the temporary data files.
        """
        self.data.close()

        # check if the file exists on disk
        if os.path.exists(self.sample_test_hdf_file):
            os.remove(self.sample_test_hdf_file)


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
