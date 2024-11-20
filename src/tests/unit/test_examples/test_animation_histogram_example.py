from gerg_plotting.examples.animation_histogram_example import animation_histogram_example

from pathlib import Path
import os
import unittest

class TestAnimationHistogramExample(unittest.TestCase):
    def test(self):
        # output_hist_path = Path('C:/Users/alecmkrueger/Documents/GERG/gerg_plotting/src/gerg_plotting/examples/example_plots/hist.gif')
        output_hist_path = Path(__file__).parent.parent.parent.parent.joinpath('gerg_plotting/examples/example_plots/hist.gif')
        # Delete the histogram plot if it already exists
        if output_hist_path.exists():
            os.remove(output_hist_path)
        animation_histogram_example()
        # Check if the histogram is generated
        self.assertTrue(output_hist_path.exists(),msg=f'{output_hist_path}')


