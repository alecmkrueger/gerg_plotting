from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.tools import data_from_csv

import unittest

class testPlotter(unittest.TestCase):

    def setUp(self):
        self.data = data_from_csv('C:/Users/alecmkrueger/Documents/GERG/gerg_plotting/src/gerg_plotting/examples/example_data/sample_glider_data.csv')
        self.plotter = Plotter(data=self.data,bounds_padding=0.25)

