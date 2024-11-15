from gerg_plotting.data_classes.Variable import Variable
import cmocean
import numpy as np
import pandas as pd
import unittest
import collections


class TestVariable(unittest.TestCase):

    def setUp(self):
        self.variable = Variable(data=[1,2,3,4],name='temperature',cmap=cmocean.cm.thermal,units='K',vmin=0,vmax=5)
    
    def tearDown(self):
        self.variable = Variable(data=[1,2,3,4],name='temperature',cmap=cmocean.cm.thermal,units='K',vmin=0,vmax=5)

    def test_variable_init(self):
        # check that the variable data is being converted to a numpy array
        self.assertIsInstance(self.variable.data,np.ndarray)
        # Check if the content of the numpy array is correct
        self.assertTrue(np.array_equal(self.variable.data,np.array([1,2,3,4])))
        # Check if name is assigned correctly
        self.assertEqual(self.variable.name, 'temperature')
        # Check if cmap is assigned correctly
        # assert self.variable.cmap == cmocean.cm.thermal, "Should be cmocean.cm.thermal"
        self.assertEqual(self.variable.cmap, cmocean.cm.thermal)
        # Check if units is assigned correctly
        self.assertEqual(self.variable.units, 'K')
        # Check if vmin is assigned correctly
        self.assertEqual(self.variable.vmin,0)
        # Check if vmax is assigned correctly
        self.assertEqual(self.variable.vmax,5)

    def test_get_attrs(self):
        # Check if the proper attributes are returned
        self.assertEqual(collections.Counter(self.variable.get_attrs()),collections.Counter(['data','name','cmap','units','vmin','vmax','label']))

    def test_get_label(self):
        self.variable.get_vmin_vmax
        # Check if label is assigned correctly
        self.assertIsNone(self.variable.label)
        # Check if get_label returns the label
        self.assertEqual(self.variable.get_label(),"Temperature (K)")
        # Check if get_label assigns label correctly
        self.assertEqual(self.variable.label,"Temperature (K)")
        # Check if it will overwrite the user's input
        self.variable.label = 'temperature (degree C)'
        self.assertEqual(self.variable.get_label(),'temperature (degree C)')

    def test_get_vmin_vmax(self):
        # Ensure it does not overwrite user input vmin and vmax
        self.variable.get_vmin_vmax()
        self.assertEqual(self.variable.vmin,0)
        self.assertEqual(self.variable.vmax,5)
        # Set vmin and vmax to None
        self.variable.vmin = None
        self.variable.vmax = None
        self.variable.get_vmin_vmax()
        self.assertEqual(self.variable.vmin,1)
        self.assertEqual(self.variable.vmax,4)

    def test_assignments(self):
        # Check dot assignment
        self.variable.data = [2,4,6,8]
        # Check to ensure data to converted to np.ndarray
        self.assertIsInstance(self.variable.data,np.ndarray)
        # Check if the data is intact
        self.assertTrue(np.array_equal(self.variable.data,np.array([2,4,6,8])))
        # Reset the variable
        self.setUp()
        # Check key assignment
        self.variable['data'] = [2,4,6,8]
        # Check to ensure data to converted to np.ndarray
        self.assertIsInstance(self.variable.data,np.ndarray)
        # Check if the data is intact
        self.assertTrue(np.array_equal(self.variable.data,np.array([2,4,6,8])))

    def test_different_data_iterables(self):
        iterables = [[2,4,6,8],(2,4,6,8),{2,4,6,8},{'a':2,'b':4,'c':6,'d':8},np.array([2,4,6,8]),pd.Series([2,4,6,8])]
        for iter in iterables:
            self.variable.data = iter
            self.assertIsInstance(self.variable.data,np.ndarray,f'{self.variable.data} should be a np.ndarray got {type(self.variable.data)}')
            self.setUp()

