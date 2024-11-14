from gerg_plotting.data_classes.SpatialInstruments import Data,Variable
import cmocean
import unittest

class TestVariable(unittest.TestCase):

    def setUp(self):
        self.data = Data()
    
    def tearDown(self):
        self.data = None

    def test_get_vars(self):
        vars_expected = ['lat','lon','depth','time','temperature','salinity','density','u','v','w','speed','bounds']
        vars_found = self.data.get_vars()
        assert vars_found == vars_expected, f'Expected vars of {vars_expected}, received vars of {vars_found}'

    def check_for_None(self,data,var):
        self.assertIsNone(data[var],f'{var} Should be None')

    def test_empty_data_init(self):
        assert isinstance(self.data,Data)==True,'Should be type Data'
        for var in self.data.get_vars():
            self.check_for_None(self.data,var)

    def test_add_var(self):
        pH = Variable(data=[1,2,3,4],name='pH',cmap=cmocean.cm.thermal,units='K',vmin=0,vmax=5)
        self.data.add_custom_variable(variable=pH)


if __name__ == "__main__":
    unittest.main()