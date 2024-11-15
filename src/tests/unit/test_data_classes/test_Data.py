from gerg_plotting.data_classes.Data import Data
from gerg_plotting.data_classes.Variable import Variable
import cmocean
import unittest

class TestData(unittest.TestCase):

    def setUp(self):
        self.data = Data()
    
    def tearDown(self):
        self.data = None

    def check_for_None(self,data,var):
        self.assertIsNone(data[var],f'{var} Should be None')

    def test_empty_data_init(self):
        assert isinstance(self.data,Data)==True,'Should be type Data'
        for var in self.data.get_vars():
            self.check_for_None(self.data,var)

