from gerg_plotting.examples.custom_3d_bathy_example import custom_3d_bathy_example

import unittest
import os
from pathlib import Path

class test_custom_3d_bathy_example(unittest.TestCase):

    def test(self):
        image_path = Path('example_plots/custom_3d_bathy_example.png')
        if image_path.exists():
            os.remove(image_path)
        custom_3d_bathy_example()
        self.assertTrue(image_path.exists())

