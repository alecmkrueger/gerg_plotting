from gerg_plotting import Data

def test_dataget_vars():
    data = Data()
    
    vars_found = data.get_vars()

def test_for_None(data,var):
    assert data[var] is None, f'{var} should be None'

def test_empty_data_init():
    data = Data()
    data.temperature = [1,2,3]
    assert isinstance(data,Data)==True,'Should be type Data'
    for var in data.get_vars():
        test_for_None(data,var)



if __name__ == "__main__":
    test_empty_data_init()
    print('Everything passed')