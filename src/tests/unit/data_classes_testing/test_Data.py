from gerg_plotting import Data,Variable,cmocean
variable = Variable(data=[1,2,3,4],name='temperature',cmap=cmocean.cm.thermal,units='K',vmin=0,vmax=5)

variable.data = [1,2,3,4]

# def test_get_vars():
#     data = Data()
#     vars_expected = ['lat','lon','depth','time','temperature','salinity','density','u','v','w','speed','bounds']
#     vars_found = data.get_vars()
#     assert vars_found == vars_expected, f'Expected vars of {vars_expected}, received vars of {vars_found}'

# def test_for_None(data,var):
#     assert data[var] is None, f'{var} Should be None'

# def test_empty_data_init():
#     data = Data()
#     assert isinstance(data,Data)==True,'Should be type Data'
#     for var in data.get_vars():
#         test_for_None(data,var)

# def test_add_var():
#     data = Data()
#     data.add_custom_variable()


# if __name__ == "__main__":
#     test_get_vars()
#     test_empty_data_init()
#     print('Everything passed')