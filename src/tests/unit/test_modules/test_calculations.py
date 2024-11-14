from gerg_plotting.modules.calculations import *
import unittest


class TestGetCenterOfMass(unittest.TestCase):

    def test_standard_case(self):
        # Standard case with non-NaN values
        lon = np.array([10, 20, 30])
        lat = np.array([5, 15, 25])
        pressure = np.array([1000, 2000, 3000])
        result = get_center_of_mass(lon, lat, pressure)
        self.assertEqual(result, (20, 15, 2000))  # Expected average values

    def test_with_nan_values(self):
        # Case with NaN values
        lon = np.array([10, np.nan, 30])
        lat = np.array([5, 15, np.nan])
        pressure = np.array([np.nan, 2000, 3000])
        result = get_center_of_mass(lon, lat, pressure)
        # Expected averages ignoring NaN values
        self.assertEqual(result, (20, 10, 2500))

    def test_empty_arrays(self):
        # Case with empty arrays
        lon = np.array([])
        lat = np.array([])
        pressure = np.array([])
        result = get_center_of_mass(lon, lat, pressure)
        # Expected result should be (nan, nan, nan) because arrays are empty
        self.assertTrue(np.isnan(result[0]) and np.isnan(result[1]) and np.isnan(result[2]))

    def test_single_point(self):
        # Single point data
        lon = np.array([15])
        lat = np.array([10])
        pressure = np.array([1000])
        result = get_center_of_mass(lon, lat, pressure)
        # Should return the point itself
        self.assertEqual(result, (15, 10, 1000))


class TestGetSigmaTheta(unittest.TestCase):

    def test_small_data(self):
        # Test with a small number of points (less than 50,000)
        salinity = np.array([35, 34.5, 34.7])
        temperature = np.array([10, 12, 15])
        Sg, Tg, sigma_theta = get_sigma_theta(salinity, temperature)
        self.assertEqual(sigma_theta.shape, (3, 3))  # Check the output shape

    def test_large_data(self):
        # Test with large input arrays (simulate 500,000 points)
        salinity = np.linspace(30, 40, 100_000)
        temperature = np.linspace(0, 30, 100_000)
        Sg, Tg, sigma_theta = get_sigma_theta(salinity, temperature)
        self.assertEqual(sigma_theta.shape, (10_000, 10_000))  # Check the output shape, should downsample to 10,000 by 10,000

    def test_with_nan_values(self):
        # Test handling of NaN values in the data
        salinity = np.array([35, np.nan, 34.7])
        temperature = np.array([10, 12, 15])
        Sg, Tg, sigma_theta = get_sigma_theta(salinity, temperature)
        self.assertEqual(sigma_theta.shape, (3, 3))  # NaN should be included

    def test_cnt_parameter(self):
        # Test with cnt=True
        salinity = np.array([35, 34.5, 34.7])
        temperature = np.array([10, 12, 15])
        Sg, Tg, sigma_theta, sigma_theta_lin = get_sigma_theta(salinity, temperature, cnt=True)
        self.assertEqual(sigma_theta.shape, (3, 3))  # Check shape
        self.assertEqual(sigma_theta_lin.shape, (3,))  # Should return linspace

    def test_sigma_theta_range(self):
        # Test if sigma_theta values are within expected range
        salinity = np.array([35, 34.5, 34.7])
        temperature = np.array([10, 12, 15])
        Sg, Tg, sigma_theta = get_sigma_theta(salinity, temperature)
        self.assertTrue(np.min(sigma_theta) >= 0)  # Test if sigma_theta values are non-negative


class TestGetDensity(unittest.TestCase):

    def test_standard_case(self):
        # Standard test case with typical values
        salinity = np.array([35, 34, 36])
        temperature = np.array([10, 15, 20])
        result = get_density(salinity, temperature)
        # Verify output shape and type
        self.assertEqual(result.shape, salinity.shape)
        self.assertTrue(np.issubdtype(result.dtype, np.floating))

    def test_with_nan_values(self):
        # Test case with NaN values
        salinity = np.array([35, np.nan, 36])
        temperature = np.array([10, 15, np.nan])
        result = get_density(salinity, temperature)
        # Check that NaNs are in the correct locations
        self.assertTrue(np.isnan(result[1]))  # NaN in second element due to salinity or temperature NaN
        self.assertFalse(np.isnan(result[0]))  # First element should be a valid density

    def test_empty_arrays(self):
        # Case with empty arrays
        salinity = np.array([])
        temperature = np.array([])
        result = get_density(salinity, temperature)
        # Expected result is an empty array
        self.assertEqual(result.size, 0)

    def test_single_point(self):
        # Single-point input
        salinity = np.array([35])
        temperature = np.array([10])
        result = get_density(salinity, temperature)
        # Should return a single value in an array
        self.assertEqual(result.shape, (1,))
        self.assertIsInstance(result[0], float)  # Check if result is a single float value


class TestRotateVector(unittest.TestCase):

    def test_standard_rotation(self):
        # Standard rotation by π/4 (45 degrees)
        u = np.array([1, 0])
        v = np.array([0, 1])
        theta_rad = np.pi / 4
        u_rot, v_rot = rotate_vector(u, v, theta_rad)
        # Expected rotated values
        self.assertAlmostEqual(u_rot[0], np.sqrt(2)/2, places=6)
        self.assertAlmostEqual(v_rot[0], np.sqrt(2)/2, places=6)
        self.assertAlmostEqual(u_rot[1], -np.sqrt(2)/2, places=6)
        self.assertAlmostEqual(v_rot[1], np.sqrt(2)/2, places=6)

    def test_rotation_zero_angle(self):
        # Rotation by 0 radians should return original values
        u = np.array([1, -1])
        v = np.array([1, 2])
        theta_rad = 0
        u_rot, v_rot = rotate_vector(u, v, theta_rad)
        np.testing.assert_array_almost_equal(u, u_rot)
        np.testing.assert_array_almost_equal(v, v_rot)

    def test_rotation_pi_half(self):
        # Rotation by π/2 radians (90 degrees)
        u = np.array([1, 0])
        v = np.array([0, 1])
        theta_rad = np.pi / 2
        u_rot, v_rot = rotate_vector(u, v, theta_rad)
        # Expected: (u_rot, v_rot) should be (0, 1) and (-1, 0)
        self.assertAlmostEqual(u_rot[0], 0, places=6)
        self.assertAlmostEqual(v_rot[0], 1, places=6)
        self.assertAlmostEqual(u_rot[1], -1, places=6)
        self.assertAlmostEqual(v_rot[1], 0, places=6)

    def test_rotation_pi(self):
        # Rotation by π radians (180 degrees)
        u = np.array([1, 2])
        v = np.array([-1, -2])
        theta_rad = np.pi
        u_rot, v_rot = rotate_vector(u, v, theta_rad)
        # Expected: (u_rot, v_rot) should be (-1, -2) and (1, 2)
        np.testing.assert_array_almost_equal(u_rot, -u)
        np.testing.assert_array_almost_equal(v_rot, -v)

    def test_with_nan_values(self):
        # Test handling of NaN values
        u = np.array([1, np.nan])
        v = np.array([1, 2])
        theta_rad = np.pi / 4
        u_rot, v_rot = rotate_vector(u, v, theta_rad)
        # First element should be valid, second should be NaN
        self.assertFalse(np.isnan(u_rot[0]) or np.isnan(v_rot[0]))
        self.assertTrue(np.isnan(u_rot[1]) and np.isnan(v_rot[1]))

    def test_empty_arrays(self):
        # Test empty array input
        u = np.array([])
        v = np.array([])
        theta_rad = np.pi / 4
        u_rot, v_rot = rotate_vector(u, v, theta_rad)
        # Should return empty arrays
        self.assertEqual(u_rot.size, 0)
        self.assertEqual(v_rot.size, 0)

