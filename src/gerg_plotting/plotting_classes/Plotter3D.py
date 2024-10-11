from attrs import define
import numpy as np
import mayavi

from gerg_plotting.data_classes.SpatialInstruments import SpatialInstrument


@define
class Plotter3D:
    instrument: SpatialInstrument

    def __attrs_post_init__(self):
        self.init_figure()
        self.check_instrument()

    def init_figure(self):
        raise NotImplementedError('Need to add method for initializing the mayavi figure')
    
    def check_instrument(self):
        for var in ['lat','lon','depth']:
            # Check if the instrument contains the variable
            if self.instrument.has_var(var):
                # Check if the variable is of type np.ndarray
                if isinstance(self.instrument[var],np.ndarray):
                    # Check if there is data in the variable
                    if len(self.instrument[var]) == 0:
                        raise ValueError(f'{var} contains no data')
                    # Check if the number of dimensions of the variable is not 1
                    # Mayavi plotting requires the data to be 1-D
                    elif self.instrument[var].ndim != 1:
                        raise ValueError(f'{var} is not flat, it has shape of {np.shape(self.instrument[var])}')
                # Check if the variable is None
                elif self.instrument[var] is None:
                    raise ValueError(f'{var} contains no data')
            else:
                raise ValueError(f'Instrument does not contain {var}')
