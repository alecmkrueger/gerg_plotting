import unittest
import numpy as np
from gerg_plotting.data_classes.Data import Data
from gerg_plotting.data_classes.Variable import Variable
from gerg_plotting.data_classes.Bounds import Bounds

class TestData(unittest.TestCase):
    def setUp(self):
        """
        Set up a Data object for testing, initializing with dummy data.
        """
        self.lat_data = np.array([10, 20, 30])
        self.lon_data = np.array([100, 110, 120])
        self.u_data = np.array([1.0, 2.0, 3.0])
        self.v_data = np.array([0.5, 1.5, 2.5])
        self.w_data = np.array([0.1, 0.2, 0.3])
        
        self.data = Data(
            lat=self.lat_data,
            lon=self.lon_data,
            u=self.u_data,
            v=self.v_data,
            w=self.w_data
        )

    def test_init_variables(self):
        """
        Test the default initialization of variables.
        """
        self.assertIsInstance(self.data.u, Variable)
        self.assertIsInstance(self.data.v, Variable)
        self.assertIsInstance(self.data.w, Variable)
        self.assertIsNone(self.data.temperature)
        self.assertIsNone(self.data.salinity)

    def test_calculate_speed_without_w(self):
        """
        Test speed calculation without the vertical component (w).
        """
        self.data.w = None
        self.data.calculate_speed(include_w=False)
        self.assertIsNotNone(self.data.speed)
        expected_speed = np.sqrt(self.u_data**2 + self.v_data**2)
        np.testing.assert_array_almost_equal(self.data.speed.data, expected_speed,3,err_msg=f'{self.data.speed.data = }, {expected_speed = }')

    def test_calculate_speed_with_w(self):
        """
        Test speed calculation with the vertical component (w).
        """
        self.data.calculate_speed(include_w=True)
        self.assertIsNotNone(self.data.speed)
        expected_speed = np.sqrt(self.u_data**2 + self.v_data**2 + self.w_data**2)
        np.testing.assert_array_almost_equal(self.data.speed.data, expected_speed,2,err_msg=f'{self.data.speed.data = }, {expected_speed = }')

    def test_calculate_PSD(self):
        """
        Test the power spectral density (PSD) calculation.
        """
        sampling_freq = 10
        segment_length = 3

        # Remove w so the calculation will not use it
        self.data.w = None

        freq, psd_U, psd_V = self.data.calcluate_PSD(sampling_freq, segment_length)

        self.assertIsInstance(freq, np.ndarray)
        self.assertIsInstance(psd_U, np.ndarray)
        self.assertIsInstance(psd_V, np.ndarray)
        self.assertIn('psd_freq', self.data.custom_variables)
        self.assertIn('psd_u', self.data.custom_variables)
        self.assertIn('psd_v', self.data.custom_variables)

    def test_calculate_PSD_with_w(self):
        """
        Test the power spectral density (PSD) calculation when w is included.
        """
        sampling_freq = 10
        segment_length = 3

        freq, psd_U, psd_V, psd_W = self.data.calcluate_PSD(sampling_freq, segment_length)
        
        self.assertIsInstance(freq, np.ndarray)
        self.assertIsInstance(psd_W, np.ndarray)
        self.assertIn('psd_w', self.data.custom_variables)

    def test_calculate_PSD_with_theta_rad(self):
        theta_rad = np.deg2rad(55)
        sampling_freq = 10
        segment_length = 3

        # Remove w so the calculation will not use it
        self.data.w = None

        freq, psd_U, psd_V = self.data.calcluate_PSD(sampling_freq, segment_length,theta_rad=theta_rad)

        self.assertIsInstance(freq, np.ndarray)
        self.assertIsInstance(psd_U, np.ndarray)
        self.assertIsInstance(psd_V, np.ndarray)
        self.assertIn('psd_freq', self.data.custom_variables)
        self.assertIn('psd_u', self.data.custom_variables)
        self.assertIn('psd_v', self.data.custom_variables)

